import sys
from typing import ContextManager as ContextManager
from typing import Generic, TypeVar, Callable, Iterator

_T = TypeVar('_T')

class GeneratorContextManager(ContextManager[_T], Generic[_T]):
    def __call__(self, func: Callable[..., _T]) -> Callable[..., _T]: ...

def contextmanager(func: Callable[..., Iterator[_T]]) -> Callable[..., GeneratorContextManager[_T]]:
    ...

if sys.version_info >= (3, 7):
    from typing import AsyncIterator
    from typing import AsyncContextManager as AsyncContextManager
    def asynccontextmanager(func: Callable[..., AsyncIterator[_T]]) -> Callable[..., AsyncContextManager[_T]]: ...
