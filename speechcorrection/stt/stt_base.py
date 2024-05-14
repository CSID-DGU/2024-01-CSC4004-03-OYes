from abc import ABCMeta, abstractmethod


class STTBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, voice_path=None):
        self.__origin_voice_path = voice_path
        self.__origin_script = None
        pass

    @abstractmethod
    def execute(self):
        pass

    @property
    @abstractmethod
    def origin_voice_path(self):
        pass

    @origin_voice_path.setter
    @abstractmethod
    def origin_voice_path(self, voice_path):
        pass

    @property
    @abstractmethod
    def origin_script(self):
        pass
