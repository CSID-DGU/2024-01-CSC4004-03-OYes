import openai

from speechcorrection.correction.correction_base import CorrectionBase


class ScriptCorrection(CorrectionBase):
    def __init__(self, origin_script=None):
        self.__origin_script = origin_script
        self.__corrected_script = str()
        self.__base_prompt = """나는 앞으로 부정확한 한국어 발음을 들리는 대로 받아 적은 텍스트를 입력할 건데, 하기된 조건을 지키면서 내가 입력한 한국어 텍스트를 문맥에 맞게 수정을 해.
        조건 1. 맞춤법을 교정하고, 그 과정에서 단어의 원형을 알기 어려우면 가장 비슷한 단어를 선택하여 교정해. 단, 단어의 원형을 알 수 있거나 문장의 성분을 분석했을 때, 고유명사로 추정되는 경우에는 절대로 바꾸면 안 돼.
        조건 2. 완성한 문장이 한국어 문법적으로, 의미 상으로 문제가 없어야 하고, 의미 상 왜곡을 최소화해야 해.
        조건 3. 출력은 다른 말 붙이지 말고 반드시 교정된 텍스트만 나와야돼.
        조건 4. 문장이 평상시에 쓰도록 말이 되어야 해.
        이제부터 부정확한 발음을 교정한 예시를 보여줄 거야. 하기된 예시를 참고해서 교정을 진행해 줘.
        예시 1. 생가기란 생가카면 생각할쑤록 생각나능 거시 생각이므로 생가카지 않는 생가기 조흔 쌩가이라 새가칸다 는
        생각이란 생각하면 생각할수록 생각나는 것이 생각이므로 생각하지 않는 생각이 좋은 생각이라 생각한다 라고 고치는 게 정확해.
        예시 2. 여름장이란 애시댕초에 글러서 해는 아직 증천에 있건만 장판은 벌써 쓸쓸하고 더운 햇발이 벌러 놓은 전시장 밑으루 등줄기를 훅훅 봉는다는 
        여름장이란 애시당초에 글러서 해는 아직 중천에 있건만 장터는 벌써 쓸쓸하고 더운 햇볕이 벌렁놓은 전시장 밑으로 등줄기를 훅훅 볶는다 라고 고치는 게 정확해.
        예시 3. 이거 아무리 마메 업는 웃음을 팔아먹고 사는 무식쟁이라고 누구한테 지금 설교를 하라는 거야 뭐야, 건방지게. 그래 내가 지금 당신 가튼 위인의 신세 하소연이나 듣짜고 이른 델 차자온 줄 알어? 내가 그러케 한가한 사람으로 보이느냐 말야 는
        이거 아무리 마음에 없는 웃음을 팔아먹고 사는 무식쟁이라고, 누구한테 지금 설교를 하라는 거야 뭐야? 건방지게. 그래, 내가 지금 당신 같은 위인의 신세 한탄이나 듣자고 이런 데를 찾아온 줄 알아? 내가 그렇게 한가한 사람으로 보이느냐 말야 라고 고치는 게 정확해.
        """
        self._additional_prompt_list = "문장이 평상시에 쓰도록 말이 되어야 돼."
        self.__api_key = None
        # self.conversation_history = ""

    def execute(self):
        for user_input in self.__origin_script.split('\n'):
            self.__corrected_script = self.get_response(user_input)
        return self.__corrected_script

    def get_response(self, prompt):
        messages = [
            {"role": "system", "content": self.__base_prompt},
            {"role": "system", "content": self._additional_prompt_list},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]

    # def cumulative_input(self, input_str: str, conversation_history: str):
    #     conversation_history += f"{input_str}\n".get_response(conversation_history)

    #     message = self
    #     additional_prompt = (
    #     f"원본 텍스트: {input_str}\n"
    #     """위 텍스트를 교정해 줘. 그런 다음 교정된 텍스트를 다시 검토하여 추가적인 오류나 개선할 점이 있는지 확인하고 수정해 줘. 
    #     문장에 추가적인 오류나 개선할 점이 없으면 추가적인 말 덧붙이지 마."""
    #     ) # 추가 검토 진행하는 프롬프트

    #     message = self.get_response(additional_prompt)

    #     return message

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
