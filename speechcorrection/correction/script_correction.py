from speechcorrection.correction.correction_base import CorrectionBase
import openai

class ScriptCorrection(CorrectionBase):
    def __init__(self, origin_script=None):
        self.__origin_script = origin_script
        self.__corrected_script = None
        self.__base_prompt = "당신은 오류가 있는 문장을 문맥에 맞는 올바른 단어로 바꾸어 주는 친절한 AI 비서입니다."
        self.__additional_prompt_list = []
        self.__api_key = None
        pass

    def execute(self):
        prompt = self.__origin_script
        add_prompt = "잘못된 발음을 옮긴 텍스트를 알려줄 거야. 이걸 문맥에 맞게 정확하게 고쳐줘"
        self.__additional_prompt_list.append(add_prompt)  # 추가적인 프롬프트를 리스트에 추가
        response = self.corrected_script(self.__additional_prompt_list)
        print(response)

    @property
    def origin_script(self):
        return self.__origin_script

    @origin_script.setter
    def origin_script(self, origin_script):
        self.__origin_script = origin_script

    # @property
    def corrected_script(self, additional_prompt_list): 
        messages = [
            {"role": "system", "content": self.__base_prompt},
            {"role": "user", "content": self.__origin_script + " " + " ".join(self.__additional_prompt_list)}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]

    @property
    def base_prompt(self):
        return self.__base_prompt

    @base_prompt.setter
    def base_prompt(self, base_prompt):
        self.__base_prompt = base_prompt

    @property
    def additional_prompt_list(self):
        return self.__additional_prompt_list

    @additional_prompt_list.setter
    def additional_prompt_list(self, additional_prompt_list):
        self.__additional_prompt_list = additional_prompt_list
        self.__base_prompt += ' ' + ' '.join(additional_prompt_list)
        
    
    @property
    def api_key(self):
        pass

    @api_key.setter
    def api_key(self, api_key):
        pass