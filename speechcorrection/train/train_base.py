from abc import ABCMeta, abstractmethod


class VoiceTrainBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, dataset_path=None):
        self.__dataset_path = dataset_path
        pass

    @abstractmethod
    def execute(self):
        pass

    @property
    @abstractmethod
    def dataset_path(self):
        pass

    @dataset_path.setter
    @abstractmethod
    def dataset_path(self, basic_voice_path):
        pass