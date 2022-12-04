import pytest

from lyrid import StatefulActor
from lyrid.core.messaging import Address, Message


def test_should_raise_name_error_when_creating_actor_with_field_address():
    with pytest.raises(NameError) as e:
        class A(StatefulActor):
            address: str  # type: ignore

            def on_receive(self, sender: Address, message: Message):
                pass
    assert str(e.value) == "Cannot assign field named 'address'"

    with pytest.raises(NameError) as e:
        class B(StatefulActor):
            address = "here"

            def on_receive(self, sender: Address, message: Message):
                pass
    assert str(e.value) == "Cannot assign field named 'address'"


def test_should_raise_name_error_when_creating_actor_with_protected_field_address():
    with pytest.raises(NameError) as e:
        class A(StatefulActor):
            _address: str  # type: ignore

            def on_receive(self, sender: Address, message: Message):
                pass
    assert str(e.value) == "Cannot assign field named '_address'"

    with pytest.raises(NameError) as e:
        class B(StatefulActor):
            _address = "here"

            def on_receive(self, sender: Address, message: Message):
                pass
    assert str(e.value) == "Cannot assign field named '_address'"


def test_should_raise_name_error_when_creating_actor_with_field_messenger():
    with pytest.raises(NameError) as e:
        class A(StatefulActor):
            _messenger: int  # type: ignore

            def on_receive(self, sender: Address, message: Message):
                pass
    assert str(e.value) == "Cannot assign field named '_messenger'"

    with pytest.raises(NameError) as e:
        class B(StatefulActor):
            _messenger = {}

            def on_receive(self, sender: Address, message: Message):
                pass
    assert str(e.value) == "Cannot assign field named '_messenger'"
