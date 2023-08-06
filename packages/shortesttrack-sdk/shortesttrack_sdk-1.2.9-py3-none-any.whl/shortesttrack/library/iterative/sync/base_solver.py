from abc import ABCMeta, abstractmethod

from shortesttrack_tools.functional import cached_property

from shortesttrack.library import Library


class BaseSyncSolver(metaclass=ABCMeta):
    """
    An abstract class that the user needs to implement to run the code in ShortestTrack Company API.
    """

    @cached_property
    def library(self) -> Library:
        return Library()

    @abstractmethod
    def iterate(self, **kwargs):
        """
        This method will be called in a loop to process input data.
        Synchronous and asynchronous method calls are possible.

        args:
            kwargs:
                Input data for processing.
        """
        pass

    @abstractmethod
    def close(self):
        """
        This method will be guaranteed to be called when the script finishes working.
        """
        pass

    @abstractmethod
    def is_ready(self):
        """
        This method is required to determine the status of the user script (readiness to work).

        returns:
            bool: is ready
        """
        pass
