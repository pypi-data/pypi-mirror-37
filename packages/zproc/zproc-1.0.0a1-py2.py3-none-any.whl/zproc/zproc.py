import atexit
import functools
import itertools
import multiprocessing
import os
import pickle
import signal
from typing import Tuple, Callable, Union, Hashable

import zmq

from zproc import util
from zproc.zproc_server import ZProcServer


def ping(
    server_address: Tuple[str, str],
    *,
    timeout: Union[None, float, int] = None,
    payload: Union[None, bytes] = None,
) -> Union[int, None]:
    """
    Ping the zproc server

    :param server_address:
        The zproc server's address.
        (See :ref:`zproc-server-address-spec`)

    :param timeout:
        The timeout in seconds.

        If this is set to ``None``, then it will block forever, until the zproc server replies.

        For all other values, it will wait for a reply,
        for that amount of time before returning with a ``TimeoutError``.

        By default it is set to ``None``.

    :param payload:
        payload that will be sent to the server.

        If it is set to None, then ``os.urandom(56)`` (56 random bytes) will be used.

    :return:
        The zproc server's **PID** if the ping was successful, else ``None``
    """

    if payload is None:
        payload = os.urandom(56)

    ctx = zmq.Context()
    ctx.setsockopt(zmq.LINGER, 0)
    sock = ctx.socket(zmq.DEALER)
    sock.connect(server_address[0])

    if timeout is not None:
        sock.setsockopt(zmq.RCVTIMEO, int(timeout * 1000))

    ping_msg = {
        util.Message.server_method: ZProcServer.ping.__name__,
        util.Message.payload: payload,
    }

    sock.send_pyobj(ping_msg, protocol=pickle.HIGHEST_PROTOCOL)

    try:
        response = sock.recv_pyobj()
    except zmq.error.Again:
        raise TimeoutError("Connection to zproc server timed out!")
    else:
        if response[util.Message.payload] == payload:
            return response["pid"]
        else:
            return None
    finally:
        sock.close()


def _server_process(*args, **kwargs):
    server = ZProcServer(*args, **kwargs)

    def signal_handler(*args):
        server.close()
        util.cleanup_current_process_tree(*args)

    signal.signal(signal.SIGTERM, signal_handler)
    server.mainloop()


def start_server(
    server_address: Union[None, Tuple[str, str]] = None,
    *,
    backend: Callable = multiprocessing.Process,
):
    """
    Start a new zproc server.

    :param server_address:
        The zproc server's address.
        (See :ref:`zproc-server-address-spec`)

        If set to ``None``, then a random address will be used.

    :param backend:
        The backend to use for launching the server process.

        For example, you may use ``threading.Thread`` as the backend.

        .. warning::

            Not guaranteed to work well with anything other than ``multiprocessing.Process``.

    :return: ``tuple``, containing a ``multiprocessing.Process`` object for server and the server address.
    """

    address_queue = multiprocessing.Queue()

    server_process = backend(
        target=_server_process, args=(server_address, address_queue)
    )
    server_process.start()

    return server_process, address_queue.get()


def atomic(fn: Callable):
    """
    Wraps a function, to create an atomic operation out of it.

    No Process shall access the state while ``fn`` is running.

    .. note::
        The first argument to the wrapped function must be a :py:class:`State` object.

    Read :ref:`atomicity`.

    :return: wrapped function

    .. code-block:: py
        :caption: Example

        import zproc

        @zproc.atomic
        def increment(state):
            return state['count'] += 1

        ctx = zproc.Context()
        ctx.state['count'] = 0

        print(increment(ctx.state))  # 1

    """

    serialized_fn = util.serialize_func(fn)

    @functools.wraps(fn)
    def atomic_wrapper(state, *args, **kwargs):
        return state._req_rep(
            {
                util.Message.server_method: ZProcServer.exec_atomic_func.__name__,
                util.Message.func: serialized_fn,
                util.Message.args: args,
                util.Message.kwargs: kwargs,
            }
        )

    return atomic_wrapper


def _create_state_watcher_decorator(self, live, timeout):
    """Generates the template for a state watcher"""

    def watcher_loop_decorator(fn):
        def watcher_loop_executor():
            if live:
                sock = self._get_subscribe_sock()
            else:
                sock = self._pub_sub_sock

            if timeout is not None:
                sock.setsockopt(zmq.RCVTIMEO, int(timeout * 1000))

            try:
                return fn(sock)
            except zmq.error.Again:
                raise TimeoutError("Timed-out waiting for an update")
            finally:
                if live:
                    sock.close()
                elif timeout is not None:
                    sock.setsockopt(zmq.RCVTIMEO, -1)

        return watcher_loop_executor

    return watcher_loop_decorator


class State:
    def __init__(self, server_address):
        """
        Allows accessing state stored on the zproc server, through a dict-like API.

        Communicates to the zproc server using the ZMQ sockets.

        Don't share a State object between Processes / Threads.
        A State object is not thread-safe.

        Boasts the following ``dict``-like members, for accessing the state:

        - Magic  methods:
            ``__contains__()``,  ``__delitem__()``, ``__eq__()``,
            ``__getitem__()``, ``__iter__()``,
            ``__len__()``, ``__ne__()``, ``__setitem__()``

        - Methods:
            ``clear()``, ``copy()``, ``fromkeys()``, ``get()``,
            ``items()``,  ``keys()``, ``pop()``, ``popitem()``,
            ``setdefault()``, ``update()``, ``values()``

        :param server_address:
            The address of zproc server.
            (See :ref:`zproc-server-address-spec`)

            If you are using a :py:class:`Context`, then this is automatically provided.

        :ivar server_address: Passed on from constructor
        """

        self._zmq_ctx = zmq.Context()
        self._zmq_ctx.setsockopt(zmq.LINGER, 0)

        self.server_address = server_address
        self._req_rep_address, self._pub_sub_address = server_address

        self._req_rep_sock = self._zmq_ctx.socket(zmq.DEALER)
        self._identity = os.urandom(5)
        self._req_rep_sock.setsockopt(zmq.IDENTITY, self._identity)
        self._req_rep_sock.connect(self._req_rep_address)

        self._pub_sub_sock = self._get_subscribe_sock()

    def _get_subscribe_sock(self):
        sock = self._zmq_ctx.socket(zmq.SUB)
        sock.connect(self._pub_sub_address)
        sock.setsockopt(zmq.SUBSCRIBE, b"")
        return sock

    def _subscribe(self, sock):
        while True:
            identity, response = sock.recv_multipart()

            # only accept updates from other processes, not this one.
            if identity != self._identity:
                return util.handle_server_response(pickle.loads(response))

    def _req_rep(self, request):
        self._req_rep_sock.send_pyobj(request, protocol=pickle.HIGHEST_PROTOCOL)
        response = self._req_rep_sock.recv_pyobj()
        return util.handle_server_response(response)

    def atomic(self):
        """
        Run a function atomically.

        Follows the same

        :return:
        """

    def get_when_change(
        self,
        *keys: Hashable,
        exclude: bool = False,
        live: bool = True,
        timeout: Union[None, float, int] = None,
    ):
        """
        | Block until a change is observed.

        :param \*keys:
            Observe for changes in these ``dict`` key(s).

            If no key is provided, any change in the ``state`` is respected.
        :param exclude:
            Reverse the lookup logic i.e.,

            Watch for changes in all ``dict`` keys *except* \*keys.

            If \*keys is not provided, then this has no effect.
        :param live:
            Whether to get "live" updates. (See :ref:`live-events`)
        :param timeout:
            Sets the timeout in seconds. By default it is set to ``None``.

            If the value is 0, it will return immediately, with a ``TimeoutError``,
            if no update is available.

            If the value is ``None``, it will block until an update is available.

            For all other values, it will wait for and update,
            for that amount of time before returning with a ``TimeoutError``.

        :return: Roughly,

        ::

            if exclude:
                return state.copy()

            if len(keys) == 0:
                return state.copy()

            if len(keys) == 1:
                return state.get(key)

            if len(keys) > 1:
                return [state.get(key) for key in keys]
        """

        num_keys = len(keys)

        if num_keys:
            if exclude:

                def select_keys(old_state, new_state):
                    return (
                        key
                        for key in itertools.chain(old_state.keys(), new_state.keys())
                        if key not in keys
                    )

            else:

                def select_keys(old, new_state):
                    return (
                        key
                        for key in itertools.chain(old.keys(), new_state.keys())
                        if key in keys
                    )

            @_create_state_watcher_decorator(self, live, timeout)
            def _get_state(sock):
                while True:
                    old_state, new_state = self._subscribe(sock)

                    for key in select_keys(old_state, new_state):
                        try:
                            old_val, new_val = old_state[key], new_state[key]
                        except KeyError:  # In a way, this implies something changed
                            return new_state
                        else:
                            if new_val != old_val:
                                return new_state

        else:

            @_create_state_watcher_decorator(self, live, timeout)
            def _get_state(sock):
                return self._subscribe(sock)[1]

        new_state = _get_state()

        if exclude or num_keys == 0:
            return new_state
        elif num_keys == 1:
            return new_state.get(keys[0])
        else:
            return [new_state.get(key) for key in keys]

    def get_when(self, test_fn, *, live=True, timeout=None):
        """
         Block until ``test_fn(state)`` returns a True-like value.

         Where, ``state`` is a :py:class:`State` instance.

         Roughly, ``if test_fn(state): return state.copy()``

        :param test_fn: A ``function``, which is called on each state-change.
        :param live: Whether to get "live" updates. (See :ref:`live-events`)
        :param timeout: Sets the timeout in seconds. By default it is set to ``None``.

                        If the value is 0, it will return immediately, with a ``TimeoutError``,
                        if no update is available.

                        If the value is ``None``, it will block until an update is available.

                        For all other values, it will wait for and update,
                        for that amount of time before returning with a ``TimeoutError``.

        :return: state
        :rtype: ``dict``
        """

        @_create_state_watcher_decorator(self, live, timeout)
        def mainloop(sock):
            latest_state = self.copy()

            while True:
                if test_fn(latest_state):
                    return latest_state

                latest_state = self._subscribe(sock)[-1]

        return mainloop()

    def get_when_equal(self, key, value, *, live=True, timeout=None):
        """
        Block until ``state.get(key) == value``.

        :param key: ``dict`` key
        :param value: ``dict`` value.
        :param live: Whether to get "live" updates. (See :ref:`live-events`)
        :param timeout: Sets the timeout in seconds. By default it is set to ``None``.

                        If the value is 0, it will return immediately, with a ``TimeoutError``,
                        if no update is available.

                        If the value is ``None``, it will block until an update is available.

                        For all other values, it will wait for and update,
                        for that amount of time before returning with a ``TimeoutError``.

        :return: ``state.get(key)``
        """

        @_create_state_watcher_decorator(self, live, timeout)
        def mainloop(sock):
            latest_key = self.get(key)

            while True:
                if latest_key == value:
                    return latest_key

                latest_key = self._subscribe(sock)[-1].get(key)

        return mainloop()

    def get_when_not_equal(self, key, value, *, live=True, timeout=None):
        """
        Block until ``state.get(key) != value``.

        :param key: ``dict`` key.
        :param value: ``dict`` value.
        :param live: Whether to get "live" updates. (See :ref:`live-events`)
        :param timeout: Sets the timeout in seconds. By default it is set to ``None``.

                        If the value is 0, it will return immediately, with a ``TimeoutError``,
                        if no update is available.

                        If the value is ``None``, it will block until an update is available.

                        For all other values, it will wait for and update,
                        for that amount of time before returning with a ``TimeoutError``.

        :return: ``state.get(key)``
        """

        @_create_state_watcher_decorator(self, live, timeout)
        def mainloop(sock):
            latest_key = self.get(key)

            while True:
                if latest_key != value:
                    return latest_key

                latest_key = self._subscribe(sock)[-1].get(key)

        return mainloop()

    def go_live(self):
        """
        Clear the events buffer, thus removing past events that were stored.

        (See :ref:`live-events`)
        """

        self._pub_sub_sock.close()
        self._pub_sub_sock = self._get_subscribe_sock()

    def ping(self, **kwargs):
        """
        Ping the zproc server corresponding to this State's Context

        :param kwargs: Keyword arguments that :py:func:`ping` takes, except ``server_address``.
        :return: Same as :py:func:`ping`
        """

        return ping(self.server_address, **kwargs)

    def close(self):
        """
        Close this State and disconnect with the Server
        """

        self._req_rep_sock.close()
        self._pub_sub_sock.close()
        self._zmq_ctx.destroy()
        self._zmq_ctx.term()

    def copy(self):
        return self._req_rep(
            {util.Message.server_method: ZProcServer.reply_state.__name__}
        )

    def keys(self):
        return self.copy().keys()

    def items(self):
        return self.copy().items()

    def values(self):
        return self.copy().values()

    def __repr__(self):
        return "<{} value: {}>".format(State.__qualname__, self.copy())


def create_remote_method(method_name: str):
    def remote_method(self, *args, **kwargs):
        return self._req_rep(
            {
                util.Message.server_method: ZProcServer.exec_state_method.__name__,
                util.Message.dict_method: method_name,
                util.Message.args: args,
                util.Message.kwargs: kwargs,
            }
        )

    return remote_method


for method_name in util.STATE_INJECTED_METHODS:
    setattr(State, method_name, create_remote_method(method_name))


def _child_process(
    *,
    process: "Process",
    target_args: tuple = (),
    target_kwargs: dict = {},
    retry_for: tuple = (),
    retry_delay: Union[int, float] = 5,
    max_retries: Union[None, bool] = None,
    retry_args: Union[None, tuple] = None,
    retry_kwargs: Union[None, dict] = None,
):
    state = State(process.server_address)

    exceptions = [util.SignalException]
    for i in retry_for:
        if type(i) == signal.Signals:
            util.signal_to_exception(i)
        elif issubclass(i, BaseException):
            exceptions.append(i)
        else:
            raise ValueError(
                '"retry_for" must contain a `signals.Signal` or `Exception`, not `{}`'.format(
                    repr(type(i))
                )
            )
    exceptions = tuple(exceptions)

    tries = 0
    while True:
        try:
            tries += 1
            process.target(state, *target_args, **target_kwargs)
        except exceptions as e:
            if (max_retries is not None) and (tries > max_retries):
                raise e
            else:
                util.handle_crash(
                    process=process,
                    exc=e,
                    retry_delay=retry_delay,
                    tries=tries,
                    max_tries=max_retries,
                )

                if retry_args is not None:
                    target_args = retry_args
                if retry_kwargs is not None:
                    target_kwargs = retry_kwargs
        else:
            break


class Process:
    def __init__(
        self,
        server_address: tuple,
        target: Callable,
        *,
        args: tuple = (),
        kwargs: dict = {},
        start: bool = True,
        retry_for: tuple = (),
        retry_delay: Union[int, float] = 5,
        max_retries: Union[None, bool] = None,
        retry_args: Union[None, tuple] = None,
        retry_kwargs: Union[None, dict] = None,
        backend: Callable = multiprocessing.Process,
    ):
        """
        Provides a high level wrapper over ``multiprocessing.Process``.

        :param server_address:
            The address of zproc server.
            (See :ref:`zproc-server-address-spec`)

            If you are using a :py:class:`Context`, then this is automatically provided.

        :param target:
            The Callable to be invoked inside a new process.

            It is run with the following signature:

            ``target(state, *args, **kwargs)``

            Where:

            - ``state`` is a :py:class:`State` instance.
            - ``args`` and ``kwargs`` are passed from the constructor.

        :param args:
            The argument tuple for ``target``.

        :param kwargs:
            A dictionary of keyword arguments for ``target``.

        :param start:
            Automatically call :py:meth:`.start()` on the process.

        :param retry_for:
            Retry whenever a particular Exception / signal is raised.

            .. code-block:: py
                :caption: Example

                import signal

                # retry if a ConnectionError, ValueError or signal.SIGTERM is received.
                ctx.process(
                    my_process,
                    retry_for=(ConnectionError, ValueError, signal.SIGTERM)
                )

            To retry for *any* Exception -  ``retry_for=(Exception, )``

        :param retry_delay:
            The delay in seconds, before retrying.

        :param max_retries:
            Give up after this many attempts.

            A value of ``None`` will result in an *infinite* number of retries.

            After "max_tries", any Exception / Signal will exhibit default behavior.

        :param retry_args:
            Used in place of ``args`` when retrying.

            If set to ``None``, then it has no effect.

        :param retry_kwargs:
            Used in place of ``kwargs`` when retrying.

            If set to ``None``, then it has no effect.

        :param backend:
            The backend to use for launching the process(s).

            For example, you may use ``threading.Thread`` as the backend.

            .. warning::

                Not guaranteed to work well with anything other than ``multiprocessing.Process``.

        :ivar server_address: Passed on from constructor.
        :ivar target: Passed on from constructor.
        :ivar child: A ``multiprocessing.Process`` instance for the child process.
        """

        assert callable(target), '"target" must be a `Callable`, not `{}`'.format(
            type(target)
        )

        self.server_address = server_address
        self.target = target

        self.child = backend(
            target=_child_process,
            kwargs=dict(
                process=self,
                retry_for=retry_for,
                retry_delay=retry_delay,
                max_retries=max_retries,
                target_args=args,
                target_kwargs=kwargs,
                retry_args=retry_args,
                retry_kwargs=retry_kwargs,
            ),
        )

        if start:
            self.child.start()

    def __repr__(self):
        try:
            pid = self.pid
        except AttributeError:
            pid = f"{os.getpid()} (Main Process)"

        return "<{} pid: {} target: {}>".format(Process.__qualname__, pid, self.target)

    def start(self):
        """
        Start this Process

        If the child has already been started once, it will return with an :py:exc:`AssertionError`.

        :return: the process PID
        """

        self.child.start()
        return self.pid

    def stop(self):
        """
        Stop this process

        :return: :py:attr:`~exitcode`.
        """

        self.child.terminate()
        return self.child.exitcode

    def wait(self, timeout: Union[None, int, float] = None):
        """
        Wait until the process finishes execution.

        :param timeout:
            The timeout in seconds.

            If the value is ``None``, it will block until the zproc server replies.

            For all other values, it will wait for a reply,
            for that amount of time before returning with a ``TimeoutError``.
        """

        self.child.join(timeout=timeout)

        if self.child.is_alive():
            raise TimeoutError("Timed-out waiting for process to finish")

    @property
    def is_alive(self):
        """
        Whether the child process is alive.

        Roughly, a process object is alive;
        from the moment the start() method returns,
        until the child process is stopped manually (using stop()) or naturally exits
        """

        return self.child and self.child.is_alive()

    @property
    def pid(self):
        """
        The process ID.

        Before the process is started, this will be None.
        """

        if self.child is not None:
            return self.child.pid

    @property
    def exitcode(self):
        """
        The child’s exit code.

        This will be None if the process has not yet terminated.
        A negative value -N indicates that the child was terminated by signal N.
        """

        if self.child is not None:
            return self.child.exitcode


class Context:
    def __init__(
        self,
        server_address: tuple = None,
        *,
        wait: bool = False,
        cleanup: bool = True,
        server_backend: Callable = multiprocessing.Process,
        **process_kwargs,
    ):
        """
        Provides a wrapper over :py:class:`State` and :py:class:`Process`.

        Used to manage and launch processes using zproc.

        All processes launched using a Context, share the same state.

        Don't share a Context object between Processes / Threads.
        A Context object is not thread-safe.

        :param server_address:
            The address of the server.
            (See :ref:`zproc-server-address-spec`)

            If set to ``None``,
            then a new server is started and a random address will be used.

            Otherwise, it will connect to an existing server with the address provided.

            .. caution::

                If you provide a "server_address", be sure to manually start the server,
                as described here - :ref:`start-server`.

        :param wait:
            Wait for all running process to finish their work before exiting.

            Avoids manually calling :py:meth:`~Context.wait_all` at exit.
        :param cleanup:
            Whether to cleanup the process tree before exiting.

            Registers a signal handler for ``SIGTERM``, and an ``atexit`` handler.

        :param server_backend:
            Passed on to :py:func:`start_server` as ``backend``.

        :param \*\*process_kwargs:
            Keyword arguments that :py:class:`~Process` takes,
            except ``server_address`` and ``target``.

            If provided, these will be used while creating
            processes using this Context.

        :ivar process_kwargs:
            Passed from constructor.
        :ivar state:
            A :py:class:`State` instance.
        :ivar process_list:
            A list of child ``Process`` (s) created under this Context.
        :ivar server_process:
            A ``multiprocessing.Process`` object for the server, or None.
        :ivar server_address:
            The server address.
        """

        self.process_list = []
        self.process_kwargs = process_kwargs

        if server_address is None:
            self.server_process, self.server_address = start_server(
                server_address, backend=server_backend
            )
        else:
            self.server_process, self.server_address = None, server_address

        self.state = State(self.server_address)

        if cleanup:
            signal.signal(signal.SIGTERM, util.cleanup_current_process_tree)
            atexit.register(util.cleanup_current_process_tree)

        if wait:
            atexit.register(self.wait_all)

    def process(
        self, target: Union[None, Callable] = None, **process_kwargs
    ) -> Union["Process", Callable]:
        """
        Produce a child process bound to this context.

        Can be used both as a function and decorator:

        .. code-block:: py

            @zproc.process()  # you may pass some arguments here
            def my_process1(state):
                print('hello')


            @zproc.process  # or not...
            def my_process2(state):
                print('hello')


            def my_process3(state):
                print('hello')

            zproc.process(my_process3)  # or just use as a good ol' function


        :param target:
            Passed on to :py:class:`Process`'s constructor.

        :param \*\*process_kwargs:
            Keyword Only arguments that :py:class:`Process` takes.

        :return: The :py:class:`Process` instance produced.
        """

        if not callable(target):

            def wrapper(func, **kwargs):
                return self.process(func, **kwargs)

            return functools.partial(wrapper, **process_kwargs)

        process_kwargs.update(self.process_kwargs)

        process = Process(self.server_address, target, **process_kwargs)
        self.process_list.append(process)
        return process

    def process_factory(self, *targets: Callable, count: int = 1, **process_kwargs):
        """
        Produce multiple child process(s) bound to this context.

        :param \*targets: Passed on to :py:class:`Process`'s constructor, one at a time.
        :param count: The number of processes to spawn, for each target.
        :param \*\*process_kwargs: Keyword arguments that :py:class:`Process` takes, except ``server_address``.
        :return: A ``list`` of :py:class:`Process` instance(s) produced.
        """

        return [
            self.process(target, **process_kwargs)
            for target in targets
            for _ in range(count)
        ]

    def _create_watcher_process_wrapper(
        self, fn_name: str, process_kwargs: dict, *args, **kwargs
    ):
        def wrapper(fn):
            def watcher_process(state, *_args, **_kwargs):
                while True:
                    getattr(state, fn_name)(*args, **kwargs)
                    fn(state, *_args, **_kwargs)

            watcher_process = self.process(watcher_process, **process_kwargs)
            functools.update_wrapper(watcher_process.target, fn)

            return watcher_process

        return wrapper

    def call_when_change(
        self,
        *keys: Hashable,
        exclude: bool = False,
        live: bool = False,
        **process_kwargs,
    ):
        """
        Decorator version of :py:meth:`~State.get_when_change()`.

        Spawns a new Process that watches the state and calls the wrapped function forever.

        :param \*\*process_kwargs: Keyword arguments that :py:class:`Process` takes, except ``server_address``.

        All other parameters have same meaning as :py:meth:`~State.get_when_change()`

        :return: A wrapper function

                The wrapper function will return the :py:class:`Process` instance created
        :rtype: function

        .. code-block:: py
            :caption: Example

            import zproc

            ctx = zproc.Context()

            @ctx.call_when_change()
            def test(state):
                print(state)
        """

        return self._create_watcher_process_wrapper(
            "get_when_change", process_kwargs, *keys, exclude, live=live
        )

    def call_when(self, test_fn, *, live=False, **process_kwargs):
        """
        Decorator version of :py:meth:`~State.get_when()`.

        Spawns a new Process that watches the state and calls the wrapped function forever.

        :param \*\*process_kwargs: Keyword arguments that :py:class:`Process` takes, except ``server_address``.

        All other parameters have same meaning as :py:meth:`~State.get_when()`

        :return: A wrapper function

                The wrapper function will return the :py:class:`Process` instance created
        :rtype: function

        .. code-block:: py
            :caption: Example

            import zproc

            ctx = zproc.Context()

            @ctx.get_state_when(lambda state: state['foo'] == 5)
            def test(state):
                print(state)
        """

        return self._create_watcher_process_wrapper(
            "get_when", process_kwargs, test_fn, live=live
        )

    def call_when_equal(self, key, value, *, live=False, **process_kwargs):
        """
        Decorator version of :py:meth:`~State.get_when_equal()`.

        Spawns a new Process that watches the state and calls the wrapped function forever.

        :param \*\*process_kwargs: Keyword arguments that :py:class:`Process` takes, except ``server_address``.

        All other parameters have same meaning as :py:meth:`~State.get_when_equal()`

        :return: A wrapper function

                The wrapper function will return the :py:class:`Process` instance created
        :rtype: function

        .. code-block:: py
            :caption: Example

            import zproc

            ctx = zproc.Context()

            @ctx.call_when_equal('foo', 5)
            def test(state):
                print(state)
        """

        return self._create_watcher_process_wrapper(
            "get_when_equal", process_kwargs, key, value, live=live
        )

    def call_when_not_equal(self, key, value, *, live=False, **process_kwargs):
        """
        Decorator version of :py:meth:`~State.get_when_not_equal()`.

        Spawns a new Process that watches the state and calls the wrapped function forever.

        :param \*\*process_kwargs: Keyword arguments that :py:class:`Process` takes, except ``server_address``.

        All other parameters have same meaning as :py:meth:`~State.get_when_not_equal()`

        :return:
            A wrapper function

            The wrapper function will return the :py:class:`Process` instance created
        :rtype: function

        .. code-block:: py
            :caption: Example

            import zproc

            ctx = zproc.Context()

            @ctx.call_when_not_equal('foo', 5)
            def test(state):
                print(state)
        """

        return self._create_watcher_process_wrapper(
            "get_when_not_equal", process_kwargs, key, value, live=live
        )

    def wait_all(self):
        """
        Call :py:meth:`~Process.wait()` on all the child processes of this Context.
        """

        for proc in self.process_list:
            proc.wait()

    def start_all(self):
        """
        Call :py:meth:`~Process.start()` on all the child processes of this Context

        Ignore if process is already started
        """

        for proc in self.process_list:
            try:
                proc.start()
            except AssertionError:
                pass

    def stop_all(self):
        """Call :py:meth:`~Process.stop()` on all the child processes of this Context"""

        for proc in self.process_list:
            proc.stop()

    def ping(self, **kwargs):
        """
        Ping the zproc server.

        :param \*\*kwargs: Keyword arguments that :py:func:`ping` takes, except ``server_address``.
        :return: Same as :py:func:`ping`
        """
        return ping(self.server_address, **kwargs)

    def close(self):
        """
        Close this context and stop all processes associated with it.

        Once closed, you shouldn't use this Context again.
        """

        self.stop_all()

        if self.server_process is not None:
            self.server_process.terminate()

        self.state.close()
