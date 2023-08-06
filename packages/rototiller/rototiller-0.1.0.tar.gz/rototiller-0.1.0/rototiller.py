"""
Rototiller: Coroutine Utilities.

* single-call init with `Coro.init(*args, **kwargs)` (no `coro.send(None)` needed)
* recording, inspection, loading, and playback of coroutine inputs and outputs with Recordable.
* assertion helpers for validating coroutines do the expected thing.
"""


# [ Imports:Python ]
import types
import typing

# [ Imports:Third Party ]
import din  # type: ignore


# [ Exports ]
__all__ = (
    'Coro',
    'Restorable',
    'assert_init_yields',
    'assert_init_raises',
    'assert_send_yields',
    'assert_send_raises',
    'assert_throw_yields',
    'assert_throw_raises',
)


def __dir__() -> typing.Tuple[str, ...]:
    return __all__


# [ Types ]
SendType = typing.TypeVar('SendType')
YieldType = typing.TypeVar('YieldType')
CoroType = typing.Coroutine[YieldType, typing.Optional[SendType], None]
CoroFuncType = typing.Callable[..., CoroType[YieldType, SendType]]
Throwable = typing.Union[
    BaseException,
    typing.Tuple[
        typing.Optional[typing.Type[BaseException]],
        typing.Optional[BaseException],
        typing.Optional[types.TracebackType],
    ],
]


# [ Classes ]
# pylint is wrong about 'Generic' being unsubscriptable:
# https://docs.python.org/3/library/typing.html#user-defined-generic-types
# pylint: disable=unsubscriptable-object
class Coro(din.ReprMixin, typing.Generic[YieldType, SendType]):  # type: ignore
    """
    Provides an init method on coroutines.

    `coro = Coro(func)` creates an object with an interface consistent with coroutines
    (send, throw) and adds an init.  The init is equivalent to calling the function
    to get the coroutine, then sending the initial None to that coroutine.

    `yielded = Coro(func).init(*args, **kwargs)`:
    * `coro = func(*args, **kwargs)`
    * `yielded = coro.send(None)`
    """

    def __init__(self, func: CoroFuncType[YieldType, SendType]) -> None:
        super().__init__()
        self.func = func
        self.coro: CoroType[YieldType, SendType]

    def init(self, *args: typing.Any, **kwargs: typing.Any) -> YieldType:
        """Initialize the coroutine and return the first yielded value."""
        self.coro = self.func(*args, **kwargs)
        return self.coro.send(None)

    def send(self, value: SendType) -> YieldType:
        """Send the value into the coroutine and return the value it yields."""
        return self.coro.send(value)

    def throw(
            self,
            error_or_type: typing.Optional[typing.Union[BaseException, typing.Type[BaseException]]],
            error: typing.Optional[BaseException] = None,
            backtrace: typing.Optional[types.TracebackType] = None,
    ) -> YieldType:
        """Throw the exception into the coroutine and return the value it yields."""
        # mypy says the first arg hast to be this type, which is wrong...
        return self.coro.throw(error_or_type, error, backtrace)  # type: ignore
# pylint: enable=unsubscriptable-object


class Restorable(Coro[YieldType, SendType]):
    """
    Provides the ability to restore coroutine states based on recorded history.

    Inputs and outputs are recorded, accessible via `get_state`, and restorable
    via `restore`.
    """

    def __init__(self, func: CoroFuncType[YieldType, SendType]) -> None:
        super().__init__(func)
        self._history: typing.List[typing.Dict] = []

    def init(self, *args: typing.Any, **kwargs: typing.Any) -> YieldType:
        """Initialize the coroutine and return the first yielded value."""
        self.coro = self.func(*args, **kwargs)
        try:
            yielded = self.coro.send(None)
        except Exception as error:
            self._history.append({'args': args, 'kwargs': kwargs, 'raised': error})
            raise
        else:
            self._history.append({'args': args, 'kwargs': kwargs, 'yielded': yielded})
            return yielded

    def send(self, value: SendType) -> YieldType:
        """Send the value into the coroutine and return the value it yields."""
        try:
            yielded = self.coro.send(value)
        except Exception as error:
            self._history.append({'sent': value, 'raised': error})
            raise
        else:
            self._history.append({'sent': value, 'yielded': yielded})
            return yielded

    def throw(
            self,
            error_or_type: typing.Optional[typing.Union[BaseException, typing.Type[BaseException]]],
            error: typing.Optional[BaseException] = None,
            backtrace: typing.Optional[types.TracebackType] = None,
    ) -> YieldType:
        """Throw the exception into the coroutine and return the value it yields."""
        if isinstance(error_or_type, BaseException):
            thrown_error = error_or_type
            try:
                yielded = super().throw(thrown_error)
            except Exception as raised_error:
                self._history.append({'thrown': thrown_error, 'raised': raised_error})
                raise
            else:
                self._history.append({'thrown': thrown_error, 'yielded': yielded})
                return yielded
        type_ = error_or_type
        try:
            yielded = super().throw(type_, error, backtrace)
        except Exception as raised_error:
            self._history.append({'thrown': (type_, error, backtrace), 'raised': raised_error})
            raise
        else:
            self._history.append({'thrown': (type_, error, backtrace), 'yielded': yielded})
            return yielded

    def get_state(self) -> typing.Tuple[typing.Dict, ...]:
        """Return a tuple of the history of inputs and outputs for this coroutine."""
        return tuple(self._history)

    def restore(self, state: typing.Tuple[typing.Dict, ...]) -> None:
        """Restore the state of the coroutine by replaying the given inputs and outputs."""
        for item in state:
            if tuple(sorted(item.keys())) == tuple(sorted(('args', 'kwargs', 'yielded'))):
                assert_init_yields(self, args=item['args'], kwargs=item['kwargs'], yields=item['yielded'])
            elif tuple(sorted(item.keys())) == tuple(sorted(('args', 'kwargs', 'raised'))):
                assert_init_raises(self, args=item['args'], kwargs=item['kwargs'], raises=item['raised'])
            elif tuple(sorted(item.keys())) == tuple(sorted(('sent', 'yielded'))):
                assert_send_yields(self, send=item['sent'], yields=item['yielded'])
            elif tuple(sorted(item.keys())) == tuple(sorted(('sent', 'raised'))):
                assert_send_raises(self, send=item['sent'], raises=item['raised'])
            elif tuple(sorted(item.keys())) == tuple(sorted(('thrown', 'yielded'))):
                assert_throw_yields(self, throw=item['thrown'], yields=item['yielded'])
            elif tuple(sorted(item.keys())) == tuple(sorted(('thrown', 'raised'))):
                assert_throw_raises(self, throw=item['thrown'], raises=item['raised'])
            else:
                raise RuntimeError(f"Cannot restore: unrecognized item in history ({item})")


def assert_init_yields(wrapped_coro: Coro[YieldType, SendType], *, args: tuple = (), kwargs: typing.Optional[dict] = None, yields: YieldType) -> None:
    """Assert that a coroutine init yields the expected value."""
    if kwargs is None:
        kwargs = {}

    def _error_lines() -> typing.Tuple[str, ...]:
        return (
            f"Coro raised an unexpected assertion!",
            f"wrapped_coro: {wrapped_coro}",
            f"args: {args}",
            f"kwargs: {kwargs}",
            f"expected yield: {yields}",
        )

    try:
        actually_yields = wrapped_coro.init(*args, **kwargs)
    except Exception as error:
        error_message = '\n'.join((
            *_error_lines(),
            f"error type: {type(error)}",
            f"error: {error}",
        ))
        raise AssertionError(error_message)
    if actually_yields != yields:
        error_message = '\n'.join((
            *_error_lines(),
            f"actual yield: {actually_yields}",
        ))
        raise AssertionError(error_message)


def assert_init_raises(
    wrapped_coro: Coro[YieldType, SendType], *,
    args: tuple = (),
    kwargs: typing.Optional[dict] = None,
    raises: BaseException,
) -> None:
    """Assert that a coroutine init raises the expected exception."""
    actually_raised: typing.Optional[BaseException]

    if kwargs is None:
        kwargs = {}
    try:
        actually_yields = wrapped_coro.init(*args, **kwargs)
    # testing the exact exception type raised - we need to catch literally everything
    except BaseException as error:  # pylint: disable=broad-except
        actually_raised = error
    else:
        actually_raised = None

    if (
        actually_raised and
        # we're looking for exact type matching
        type(actually_raised) == type(raises) and  # pylint: disable=unidiomatic-typecheck
        str(actually_raised) == str(raises)
    ):
        return
    error_lines = (
        f"Coro raised the wrong assertion!",
        f"wrapped_coro: {wrapped_coro}",
        f"args: {args}",
        f"kwargs: {kwargs}",
        f"expected error type: {type(raises)}",
        f"expected error: {raises}",
    )

    if actually_raised:
        error_message = '\n'.join((
            *error_lines,
            f"actual error type: {type(actually_raised)}",
            f"actual error: {actually_raised}",
        ))
        raise AssertionError(error_message)
    error_message = '\n'.join((
        *error_lines,
        f"actual yield: {actually_yields}",
    ))
    raise AssertionError(error_message)


def assert_send_yields(coro: Coro[YieldType, SendType], *, send: SendType, yields: YieldType) -> None:
    """Assert that a coroutine send yields the expected value."""
    def _error_lines() -> typing.Tuple[str, ...]:
        return (
            f"Coro raised an unexpected assertion!",
            f"coro: {coro}",
            f"sent value: {send}",
            f"expected yield: {yields}",
        )

    try:
        actually_yields = coro.send(send)
    except Exception as error:
        error_message = '\n'.join((
            *_error_lines(),
            f"error type: {type(error)}",
            f"error: {error}",
        ))
        raise AssertionError(error_message)
    if actually_yields != yields:
        error_message = '\n'.join((
            *_error_lines(),
            f"actual yield: {actually_yields}",
        ))
        raise AssertionError(error_message)


def assert_throw_yields(coro: Coro[YieldType, SendType], *, throw: Throwable, yields: YieldType) -> None:
    """Assert that a coroutine throw yields the expected value."""
    def _error_lines() -> typing.Tuple[str, ...]:
        return (
            f"Coro raised an unexpected assertion!",
            f"coro: {coro}",
            f"thrown error: {throw}",
            f"expected yield: {yields}",
        )

    try:
        if isinstance(throw, BaseException):
            actually_yields = coro.throw(throw)
        else:
            actually_yields = coro.throw(*throw)
    except Exception as error:
        error_message = '\n'.join((
            *_error_lines(),
            f"error type: {type(error)}",
            f"error: {error}",
        ))
        raise AssertionError(error_message)
    if actually_yields != yields:
        error_message = '\n'.join((
            *_error_lines(),
            f"actual yield: {actually_yields}",
        ))
        raise AssertionError(error_message)


def assert_send_raises(coro: Coro[YieldType, SendType], *, send: SendType, raises: BaseException) -> None:
    """Assert that a coroutine send raises the expected exception."""
    actually_raised: typing.Optional[BaseException]
    try:
        actually_yields = coro.send(send)
    # testing the exact exception type raised - we need to catch literally everything
    except BaseException as error:  # pylint: disable=broad-except
        actually_raised = error
    else:
        actually_raised = None

    if (
        actually_raised and
        # we're looking for exact type matching
        type(actually_raised) == type(raises) and  # pylint: disable=unidiomatic-typecheck
        str(actually_raised) == str(raises)
    ):
        return
    error_lines = (
        f"Coro raised the wrong assertion!",
        f"coro: {coro}",
        f"sent value: {send}",
        f"expected error type: {type(raises)}",
        f"expected error: {raises}",
    )

    if actually_raised:
        error_message = '\n'.join((
            *error_lines,
            f"actual error type: {type(actually_raised)}",
            f"actual error: {actually_raised}",
        ))
        raise AssertionError(error_message)
    error_message = '\n'.join((
        *error_lines,
        f"actual yield: {actually_yields}",
    ))
    raise AssertionError(error_message)


def assert_throw_raises(coro: Coro[YieldType, SendType], *, throw: Throwable, raises: BaseException) -> None:
    """Assert that a coroutine throw raises the expected exception."""
    actually_raised: typing.Optional[BaseException]
    try:
        if isinstance(throw, BaseException):
            actually_yields = coro.throw(throw)
        else:
            actually_yields = coro.throw(*throw)
    # testing the exact exception type raised - we need to catch literally everything
    except BaseException as error:  # pylint: disable=broad-except
        actually_raised = error
    else:
        actually_raised = None

    if (
        actually_raised and
        # we're looking for exact type matching
        type(actually_raised) == type(raises) and  # pylint: disable=unidiomatic-typecheck
        str(actually_raised) == str(raises)
    ):
        return
    error_lines = (
        f"Coro raised the wrong assertion!",
        f"coro: {coro}",
        f"thrown error: {throw}",
        f"expected error type: {type(raises)}",
        f"expected error: {raises}",
    )

    if actually_raised:
        error_message = '\n'.join((
            *error_lines,
            f"actual error type: {type(actually_raised)}",
            f"actual error: {actually_raised}",
        ))
        raise AssertionError(error_message)
    error_message = '\n'.join((
        *error_lines,
        f"actual yield: {actually_yields}",
    ))
    raise AssertionError(error_message)
