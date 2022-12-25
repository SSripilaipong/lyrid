from typing import Type

from lyrid.core.system import PlacementPolicyMatcher


class MatchAll(PlacementPolicyMatcher):

    def match(self, type_: Type) -> bool:
        return True


class MatchType(PlacementPolicyMatcher):
    def __init__(self, type_: Type):
        self._type = type_

    def match(self, type_: Type) -> bool:
        return isinstance(type_, type) and isinstance(self._type, type) and issubclass(type_, self._type)
