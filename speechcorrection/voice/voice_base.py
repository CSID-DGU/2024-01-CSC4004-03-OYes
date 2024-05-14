from abc import ABCMeta, abstractmethod


class VoiceBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, basic_voice_path=None):
        self.__basic_voice_path = basic_voice_path
        self.__changed_voice_path = None
        self.__voice_model = None
        pass

    @abstractmethod
    def execute(self):
        pass

    @property
    @abstractmethod
    def basic_voice_path(self):
        pass

    @basic_voice_path.setter
    @abstractmethod
    def basic_voice_path(self, basic_voice_path):
        pass

    @property
    @abstractmethod
    def changed_voice_path(self):
        pass
