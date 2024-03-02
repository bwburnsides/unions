import typing as t
import dataclasses as dc

from util import panic, AlwaysTrue, AlwaysFalse, Func

type Result[T, E] = Ok[T] | Err[E]


@dc.dataclass
class Ok[T]:
    ok: T

    def unwrap(self) -> T:
        return self.ok

    def unwrap_err(self) -> t.NoReturn:
        panic(f"Attempted to unwrap error from Ok variant of Result: {self!r}")

    def expect(self, _expectation: str) -> T:
        return self.ok

    def expect_err(self, expectation: str) -> t.NoReturn:
        panic(f"Expectation failed: '{expectation}' for Ok variant of Result: {self!r}")

    def is_ok(self) -> AlwaysTrue:
        return True

    def is_err(self) -> AlwaysFalse:
        return not self.is_ok()

    def also[U, E](self, res: Result[U, E]) -> Result[U, E]:
        return res

    def __and__[U, E](self, res: Result[U, E]) -> Result[U, E]:
        return self.also(res)

    def otherwise[F](self, res: Result[T, F]) -> Result[T, F]:
        return self

    def __or__[F](self, res: Result[T, F]) -> Result[T, F]:
        return self.otherwise(res)

    def and_then[U, E](self, op: Func[T, Result[U, E]]) -> Result[U, E]:
        return op(self.ok)

    def or_else[E, F](self, op: Func[E, Result[T, F]]) -> Result[T, F]:
        return self


@dc.dataclass
class Err[E]:
    err: E

    def unwrap(self) -> t.NoReturn:
        panic(f"Attempted to unwrap ok from Err variant of Result: {self!r}")

    def unwrap_err(self) -> E:
        return self.err

    def expect(self, expectation: str) -> t.NoReturn:
        panic(
            f"Expectation failed: '{expectation}' for Err variant of Result: {self!r}"
        )

    def expect_err(self, _expectation: str) -> E:
        return self.err

    def is_ok(self) -> AlwaysFalse:
        return False

    def is_err(self) -> AlwaysTrue:
        return not self.is_ok()

    def also[U](self, res: Result[U, E]) -> Result[U, E]:
        return self

    def __and__[U](self, res: Result[U, E]) -> Result[U, E]:
        return self.also(res)

    def otherwise[T, F](self, res: Result[T, F]) -> Result[T, F]:
        return res

    def __or__[T, F](self, res: Result[T, F]) -> Result[T, F]:
        return self.otherwise(res)

    def and_then[T, U](self, op: Func[T, Result[U, E]]) -> Result[U, E]:
        return self

    def or_else[T, F](self, op: Func[E, Result[T, F]]) -> Result[T, F]:
        return op(self.err)


def function() -> Result[int, Exception]:
    return Ok(5)
