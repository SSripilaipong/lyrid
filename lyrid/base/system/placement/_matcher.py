from lyrid.core.process import ProcessFactory
from lyrid.core.system import PlacementPolicyMatcher


class MatchAll(PlacementPolicyMatcher):

    def match(self, type_: ProcessFactory) -> bool:
        return True


class MatchType(PlacementPolicyMatcher):
    def __init__(self, type_: ProcessFactory):
        self._type = type_

    def match(self, type_: ProcessFactory) -> bool:
        return isinstance(type_, type) and isinstance(self._type, type) and issubclass(type_, self._type)
