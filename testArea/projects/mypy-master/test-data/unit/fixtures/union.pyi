# Builtins stub used in tuple-related test cases.

from typing import TypeVar, Generic
T = TypeVar('T')

class object:
    def __init__(self): pass

class type: pass
class function: pass

class tuple(Generic[T]): pass

# We need int for indexing tuples.
class int: pass
class str: pass # For convenience
