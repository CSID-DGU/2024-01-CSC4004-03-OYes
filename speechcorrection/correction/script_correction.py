from speechcorrection.correction.correction_base import CorrectionBase
import openai

class ScriptCorrection(CorrectionBase):
    def __init__(self, origin_script=None):
        self.__origin_script = origin_script
        self.__corrected_script = ""
        self.__base_prompt = """너는 오류가 있는 문장을 문맥에 맞는 올바른 단어로 바꾸어 주는 친절한 AI 비서야. 
        잘못된 발음을 옮긴 텍스트를 알려줄 거야. 이걸 문맥에 맞게 정확하게 고쳐줘. 
        밥을 짖다는 밥을 짓다를 잘못 발음할 것일 거라고 예측할 수 있어.
        봉는다는 볶는다인 것처럼 어색한 발음들도 문맥에 맞게 고쳐주면 돼.
        문장이 평상시에 쓰도록 말이 되어야 돼. 
        다른 말 붙이지 말고 반드시 교정된 텍스트만 출력해야 해."""
        self._additional_prompt_list = ""
        self.__api_key = None
        self.conversation_history = ""

    def execute(self):
        for user_input in self.__origin_script.split('\n'):
            self.__corrected_script += self.cumulative_input(user_input, self.conversation_history)
        print(self.__corrected_script)
        return self.__corrected_script
        
    def get_response(self, prompt): 
        messages = [
            {"role": "system", "content": self.__base_prompt},
            {"role": "system", "content": self._additional_prompt_list},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    def cumulative_input(self, input_str: str, conversation_history: str):
        conversation_history += f"{input_str}\n"
        message = self.get_response(conversation_history)
        
        additional_prompt = (
        f"원본 텍스트: {input_str}\n"
        """위 텍스트를 교정해 줘. 그런 다음 교정된 텍스트를 다시 검토하여 추가적인 오류나 개선할 점이 있는지 확인하고 수정해 줘. 
        문장에 추가적인 오류나 개선할 점이 없으면 추가적인 말 덧붙이지 마."""
        ) # 추가 검토 진행하는 프롬프트
        
        message = self.get_response(additional_prompt)
        
        return message

    @property
    def origin_script(self):
        return self.__origin_script

    @origin_script.setter
    def origin_script(self, origin_script):
        self.__origin_script = origin_script

    @property
    def corrected_script(self): 
        return self.__corrected_script

    @property
    def base_prompt(self):
        return self.__base_prompt

    @base_prompt.setter
    def base_prompt(self, base_prompt):
        self.__base_prompt = base_prompt

    @property
    def additional_prompt_list(self):
        return self._additional_prompt_list

    @additional_prompt_list.setter
    def additional_prompt_list(self, additional_prompt_list):
        self._additional_prompt_list = additional_prompt_list
        
    
    @property
    def api_key(self):
        pass

    @api_key.setter
    def api_key(self, api_key):
        self.__api_key = api_key
        openai.api_key = self.__api_key