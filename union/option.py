import typing as t
import dataclasses as dc
import enum

from util import panic, AlwaysTrue, AlwaysFalse, Func

type NothingVariant = t.Literal[NothingKind.Nothing]

type Option[T] = Just[T] | NothingVariant

type ZeroParam[R] = t.Callable[[], R]

class NothingKind(enum.Enum):
    Nothing = 0

    def unwrap(self) -> t.NoReturn:
        panic(f"Attempted to unwrap value from Nothing variant of Option")

    def expect(self, _expectation: str) -> t.NoReturn:
        panic(f"Expectation failed: '{_expectation}' for Nothing variant of Option")

    def is_just(self) -> AlwaysFalse:
        return False

    def also[U](self, opt: Option[U]) -> Option[U]:
        return self.Nothing

    def __and__[U](self, opt: Option[U]) -> Option[U]:
        return self.also(opt)

    def otherwise[T](self, opt: Option[T]) -> Option[T]:
        return opt

    def __or__[T](self, opt: Option[T]) -> Option[T]:
        return self.otherwise(opt)

    def and_then[T, U](self, op: Func[T, Option[U]]) -> Option[U]:
        return self.Nothing

    def or_else[T](self, op: ZeroParam[Option[T]]) -> Option[T]:
        return op()

Nothing: t.Final[NothingVariant] = NothingKind.Nothing


@dc.dataclass
class Just[T]:
    just: T

    def unwrap(self) -> T:
        return self.just

    def expect(self, _expectation: str) -> T:
        return self.just

    def is_just(self) -> AlwaysTrue:
        return True

    def also[U](self, opt: Option[U]) -> Option[U]:
        return opt

    def __and__[U](self, opt: Option[U]) -> Option[U]:
        return self.also(opt)

    def otherwise(self, opt: Option[T]) -> Option[T]:
        return self

    def __or__(self, opt: Option[T]) -> Option[T]:
        return self.otherwise(opt)

    def and_then[U](self, op: Func[T, Option[U]]) -> Option[U]:
        return op(self.just)

    def or_else(self, op: ZeroParam[Option[T]]) -> Option[T]:
        return self
