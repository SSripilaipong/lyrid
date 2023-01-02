import pytest

from lyrid import use_switch, Actor, switch
from lyrid.api.actor.switch.handle_policy.error_message import invalid_argument_for_method_error


def test_should_raise_type_error_when_invalid_argument_name_is_specified():
    with pytest.raises(TypeError) as e:
        @use_switch
        class A(Actor):
            @switch.after_receive()
            def after_receive_a_message(self, a: str):
                pass

    assert str(e.value) == str(invalid_argument_for_method_error('a', 'after_receive_a_message'))
