from typing import Generic, Iterator, TypeVar

from .exceptions import (
    DuplicateRegistrationError,
    RegistryFrozenError,
    UnknownRegistrationError,
)

T = TypeVar("T")


class Registry(Generic[T]):

    def __init__(self, name: str) -> None:
        self._name = name
        self._items: dict[str, T] = {}
        self._frozen: bool = False

    def is_frozen(self) -> bool:
        return self._frozen

    def register(self, key: str, item: T) -> None:

        if self._frozen:
            raise RegistryFrozenError(
                f"Cannot register '{key}' in {self} after freezing."
            )

        if key in self._items:
            raise DuplicateRegistrationError(
                f"Key '{key}' is already registered in {self}."
            )

        self._items[key] = item

    def get(self, key: str) -> T:

        if not self.is_frozen():
            raise RegistryFrozenError(
                f"Cannot get '{key}' from {self} before freezing."
            )

        if key not in self._items:
            raise UnknownRegistrationError(
                f"Unknown key '{key}' in {self}. Available: {self.names}"
            )

        return self._items[key]

    def freeze(self) -> None:
        """
        Freeze the registry, preventing further registrations and allowing retrieval of items.
        """
        if self._frozen:
            raise RegistryFrozenError(f"{self} is already frozen.")
        self._frozen = True

    @property
    def names(self) -> list[str]:
        return list(self._items.keys())

    def __iter__(self) -> Iterator[tuple[str, T]]:
        yield from self._items.items()

    def __str__(self) -> str:
        return f"Registry<{self._name}>"
