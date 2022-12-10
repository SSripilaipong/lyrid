from lyrid.core.process import ProcessFactory
from lyrid.core.system import PlacementPolicyMatcher


class MatchAll(PlacementPolicyMatcher):

    def match(self, type_: ProcessFactory) -> bool:
        return True
