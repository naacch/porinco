from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Node:
    name: str
    operation: Callable[..., Any]
    dependencies: tuple[str, ...]
    provides: str
