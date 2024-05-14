from abc import ABCMeta, abstractmethod


class CorrectionBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, origin_script=None):
        self.__origin_script = origin_script
        self.__corrected_script = None
        self.__base_prompt = None
        self.__additional_prompt_list = None
        self.__api_key = None
        pass

    @abstractmethod
    def execute(self):
        pass

    @property
    @abstractmethod
    def origin_script(self):
        pass

    @origin_script.setter
    @abstractmethod
    def origin_script(self, origin_script):
        pass

    @property
    @abstractmethod
    def corrected_script(self):
        pass

    @property
    @abstractmethod
    def base_prompt(self):
        pass

    @base_prompt.setter
    @abstractmethod
    def base_prompt(self, base_prompt):
        pass

    @property
    @abstractmethod
    def additional_prompt_list(self):
        pass

    @additional_prompt_list.setter
    @abstractmethod
    def additional_prompt_list(self, additional_prompt_list):
        pass

    @property
    @abstractmethod
    def api_key(self):
        pass

    @api_key.setter
    @abstractmethod
    def api_key(self, api_key):
        pass
