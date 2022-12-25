from lyrid import Address, Message, MatchType, Actor


def test_should_return_true_when_type_is_matched():
    assert MatchType(ProcessDummyA).match(ProcessDummyA) is True


def test_should_return_false_when_type_is_not_matched():
    assert MatchType(ProcessDummyA).match(ProcessDummyB) is False


def test_should_return_true_when_type_is_subclass():
    assert MatchType(ProcessDummyA).match(ProcessDummyASub) is True


class ProcessDummyA(Actor):
    def on_receive(self, sender: Address, message: Message):
        pass


class ProcessDummyB(Actor):
    def on_receive(self, sender: Address, message: Message):
        pass


class ProcessDummyASub(ProcessDummyA):
    pass
