from abc import ABCMeta, abstractmethod

from shortesttrack_tools.functional import cached_property

from shortesttrack.library import Library


class BaseAsyncSolver(metaclass=ABCMeta):
    """
    An abstract class that the user needs to implement to run the code in ShortestTrack Company API.
    """
    # TODO: implement the required methods for async solver

    @cached_property
    def library(self) -> Library:
        return Library()
