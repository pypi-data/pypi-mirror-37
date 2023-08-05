from abc import ABCMeta, abstractmethod


class BaseBatchSolver(metaclass=ABCMeta):
    """
    An abstract class that the user needs to implement to run the code in ShortestTrack Company API.
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
