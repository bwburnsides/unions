import typing as t
from sys import stderr

type AlwaysTrue = t.Literal[True]
type AlwaysFalse = t.Literal[False]

type Func[P, R] = t.Callable[[P], R]

def panic(message: str, code: int = -1) -> t.NoReturn:
    print(message, file=stderr)
    exit(code)
