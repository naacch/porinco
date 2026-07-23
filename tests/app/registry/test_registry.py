import re

import pytest

from porinco.app.registry import Registry
from porinco.app.registry.exceptions import (
    DuplicateRegistrationError,
    RegistryFrozenError,
    UnknownRegistrationError,
)


@pytest.fixture
def registry():
    r = Registry("numbers")
    r.register("one", 1)
    r.register("two", 2)
    return r


def test_register_raises_on_duplicate_key(registry):
    with pytest.raises(
        DuplicateRegistrationError,
        match=re.escape("Key 'one' is already registered in Registry<numbers>."),
    ):
        registry.register("one", 1)


def test_register_raises_if_frozen(registry):
    registry.freeze()

    with pytest.raises(
        RegistryFrozenError,
        match=re.escape("Cannot register 'three' in Registry<numbers> after freezing."),
    ):
        registry.register("three", 3)


def test_register_makes_item_retrievable_after_freezing(registry):
    registry.freeze()
    assert registry.get("one") == 1
    assert registry.get("two") == 2


def test_get_raises_if_not_frozen(registry):
    with pytest.raises(
        RegistryFrozenError,
        match=re.escape("Cannot get 'one' from Registry<numbers> before freezing."),
    ):
        registry.get("one")


def test_get_raises_if_key_not_registered(registry):
    registry.freeze()

    with pytest.raises(
        UnknownRegistrationError,
        match=re.escape(
            "Unknown key 'three' in Registry<numbers>. Available: ['one', 'two']"
        ),
    ):
        registry.get("three")


def test_freeze_raises_if_already_frozen(registry):
    registry.freeze()

    with pytest.raises(
        RegistryFrozenError, match=re.escape("Registry<numbers> is already frozen.")
    ):
        registry.freeze()


def test_is_frozen_reflects_freeze_state(registry):
    assert registry.is_frozen() is False

    registry.freeze()

    assert registry.is_frozen() is True


def test_names_returns_registered_keys(registry):
    assert registry.names == ["one", "two"]


def test_iter_yields_key_item_pairs(registry):
    assert dict(registry) == {"one": 1, "two": 2}


def test_can_freeze_empty_registry():
    r = Registry("empty")
    r.freeze()
    assert r.is_frozen() is True
    assert r.names == []
