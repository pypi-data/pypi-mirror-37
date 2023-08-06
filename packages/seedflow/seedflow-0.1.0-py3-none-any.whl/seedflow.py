"""
Seedflow.

Side Effects As Data -> SEAD -> Seed.
Flow, because the library supports muliple concurrent flows of logic/side-effects.
"""


# [ Imports:Python ]
import functools
import inspect
import sys
import types
import typing

# [ Imports:Third Party ]
import din
import rototiller


# this conforms to standards for generic type names
T = typing.TypeVar('T')  # pylint: disable=invalid-name


class Task(din.ReprMixin, din.FrozenMixin, din.EqualityMixin):
    """The base task that the seedflow runner executes."""

    def __init__(self, func: typing.Callable, *args: typing.Any, **kwargs: typing.Any) -> None:
        with self._thawed():
            super().__init__()
            self.func = func
            self.args = args
            self.kwargs = kwargs


@types.coroutine
def run(func: typing.Callable, *args: typing.Any, **kwargs: typing.Any) -> typing.Generator[Task, T, T]:
    """Turn the given function and args into a task and yield it to the runner."""
    return (yield Task(func, *args, **kwargs))


class TailCall(din.EqualityMixin, Exception):
    """Tail Call Optimization helper class."""

    def __init__(self, func: typing.Callable, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs


def _run_task(task: Task) -> typing.Any:
    if inspect.iscoroutinefunction(task.func) or isinstance(task.func, rototiller.Coro):
        result = run_tasks_from(task.func, *task.args, **task.kwargs)
    else:
        result = task.func(*task.args, **task.kwargs)
    return result


def _strip_traceback(traceback: typing.Optional[types.TracebackType]) -> typing.Optional[types.TracebackType]:
    while traceback and traceback.tb_frame.f_globals['__name__'] in (__name__, 'rototiller'):
        traceback = traceback.tb_next
    if traceback:
        traceback.tb_next = _strip_traceback(traceback.tb_next)
    return traceback


def _coro_init(coro: rototiller.Coro, *, coro_input: typing.Tuple[tuple, typing.Dict[str, typing.Any]]) -> typing.Any:
    args, kwargs = coro_input
    return coro.init(*args, **kwargs)


def _coro_send(coro: rototiller.Coro, *, coro_input: typing.Any) -> typing.Any:
    return coro.send(coro_input)


def _coro_throw(coro: rototiller.Coro, *, coro_input: tuple) -> typing.Any:
    return coro.throw(*coro_input)


def run_tasks_from(coro: typing.Union[typing.Callable, rototiller.Coro], *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
    """Run the tasks yielded by the given coroutine."""
    if not isinstance(coro, rototiller.Coro):
        coro = rototiller.Coro(coro)
    coro_input: typing.Any = (args, kwargs)
    respond_to_coro = _coro_init
    while True:
        try:
            task = respond_to_coro(coro, coro_input=coro_input)
        except StopIteration as stop_signal:
            return stop_signal.value
        except TailCall as tco_call:
            if inspect.iscoroutinefunction(tco_call.func) or isinstance(tco_call.func, rototiller.Coro):
                coro = tco_call.func
                if not isinstance(coro, rototiller.Coro):
                    coro = rototiller.Coro(coro)
                coro_input = (tco_call.args, tco_call.kwargs)
                respond_to_coro = _coro_init
                continue
            else:
                result = tco_call.func(*tco_call.args, **tco_call.kwargs)
                return result
        except Exception:
            # XXX need to only clean up errors from user funcs, not from seedflow internals
            # clean up the traceback to be as readable as possible
            _, exception, traceback = sys.exc_info()
            traceback = _strip_traceback(traceback)
            # we got here, there's an exception, but mypy complains it could be none
            exception = typing.cast(Exception, exception)
            raise exception.with_traceback(traceback)
        # the coro didn't return a normal value
        # the coro didn't return via tail recursion
        # the coro didn't raise, or it woudl've bubbled up already
        # the coro just yielded a task
        try:
            coro_input = _run_task(task)
        # necessarily broad exception
        except Exception:  # pylint: disable=broad-except
            # throw the exception back to the caller (the coro)
            coro_input = sys.exc_info()
            respond_to_coro = _coro_throw
        else:
            respond_to_coro = _coro_send


def as_sync(func: typing.Callable) -> typing.Callable:
    """
    Decorate an awaitable such that it is run with seedflow when called.

    This makes a seedflow-awaitable function callable from a synchronous context.
    """
    @functools.wraps(func)
    def _wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return run_tasks_from(func, *args, **kwargs)
    return _wrapper
