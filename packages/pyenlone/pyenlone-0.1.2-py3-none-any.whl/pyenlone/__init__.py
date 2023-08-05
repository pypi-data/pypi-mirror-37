"""
Implements enl.one APIs:
- v.enl.one
- tasks.enl.one (Soon)
- status.enl.one (Not very soon, but soon)
For more info: https://wiki.enl.one/doku.php?id=start

All methods returns Munches. That only means you access them both as:
- `some_result.some_property`
- `some_result['some_property']`
"""
from .v import V, banned
from .enloneexception import EnlOneException
__all__ = ["V", "banned", "EnlOneException"]
NAME = "pyenlone"
