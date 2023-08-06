from abc import ABCMeta, abstractmethod

from shortesttrack_tools.functional import cached_property

from shortesttrack.library import Library


class BaseBatchSolver(metaclass=ABCMeta):
    """
    An abstract class that the user needs to implement to run the code in ShortestTrack Company API.
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @cached_property
    def library(self) -> Library:
        return Library()
