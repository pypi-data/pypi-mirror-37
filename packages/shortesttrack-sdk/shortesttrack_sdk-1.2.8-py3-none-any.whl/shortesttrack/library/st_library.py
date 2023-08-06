from shortesttrack.conf.lib_conf import ULibraryConfig
from shortesttrack.conf.library import ULibrary


__all__ = ('Library',)


class Library:
    def __init__(self):
        self.__library = ULibrary.init()
        self.__config = ULibraryConfig.init()

    @property
    def script_configuration(self):
        return self.__library.script_configuration

    @property
    def iterative_script_configuration(self):
        return self.__library.iterative_script_configuration

    @property
    def analytic_script_configuration(self):
        return self.__library.analytic_script_configuration
