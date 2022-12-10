from lyrid import VanillaActor, Address, Message
from lyrid.system import MatchType


def test_should_return_true_when_type_is_matched():
    assert MatchType(ProcessDummyA).match(ProcessDummyA) is True


def test_should_return_false_when_type_is_not_matched():
    assert MatchType(ProcessDummyA).match(ProcessDummyB) is False


class ProcessDummyA(VanillaActor):
    def on_receive(self, sender: Address, message: Message):
        pass


class ProcessDummyB(VanillaActor):
    def on_receive(self, sender: Address, message: Message):
        pass
