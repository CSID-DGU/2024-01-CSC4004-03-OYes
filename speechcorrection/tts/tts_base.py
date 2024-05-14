from abc import ABCMeta, abstractmethod


class TTSBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, corrected_script=None):
        self.__corrected_script = corrected_script
        self.__basic_voice_path = None
        pass

    @abstractmethod
    def execute(self):
        pass

    @property
    @abstractmethod
    def corrected_script(self):
        pass

    @corrected_script.setter
    @abstractmethod
    def corrected_script(self, corrected_script):
        pass

    @property
    @abstractmethod
    def basic_voice_path(self):
        pass
