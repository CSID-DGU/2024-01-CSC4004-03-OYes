import openai
import time
import os


class ScriptCorrection:
    def __init__(self):
        
    #     INITIAL_PROMPT = ('''
    #     당신은 오류가 있는 문장을 문맥에 맞는 올바른 단어로 바꾸어 주는 친절한 AI 비서입니다.
    #  ''')
    #     self.conversation_history = INITIAL_PROMPT + "\n"
        self.conversation_history = ""
        self.USERNAME = "USER"
        self.AI_NAME = "GPT"
        self.corrected_script = []
        
    
    def cumulative_input(self,
                       input_str : str,
                       conversation_history : str, 
                       USERNAME : str,
                       AI_NAME : str,):
    # Update the conversation history
        conversation_history += f"{USERNAME}: {input_str}\n"
   
    # Generate a response using GPT-3
        message = self.get_response(conversation_history)
    # Update the conversation history
        conversation_history += f"{AI_NAME}: {message}\n"

    # # Print the response
        # print(f'{AI_NAME}: {message}')
        
        return conversation_history
        # self.corrected_script.append(message)
    
    def get_response(self, prompt):
    # Returns the response for the given prompt using the OpenAI API.
        completions = openai.ChatCompletion.create(
          model = "gpt-3.5-turbo",
          messages=[
                {"role": "assistant", "content": """다른 말 붙이지 말고 바로 정답만 얘기해줘"""},
                {"role": "assistant", "content": """정답이라는 단어도 붙이지 마"""},
                {"role": "system", "content": "잘못된 발음을 옮긴 텍스트를 알려줄 거야. 이걸 문맥에 맞게 정확하게 고쳐줘"},
                {"role": "assistant", "content": """밥을 짖다는 밥을 짓다를 잘못 발음할 것일 거라고 예측할 수 있어"""},
                {"role": "assistant", "content": """여름장이란 애시댕초에 글러서 해는 아직 증천에 있건만 장판은 벌써 쓸쓸하고 더운 햇발이 벌러 놓은 전시장 밑으루 등줄기를 훅훅 봉는다.는 
                 여름장이란 애시당초에 글러서 해는 아직 증천에 있건만 장판은 벌써 쓸쓸하고 더운 햇발이 벌러 놓은 전시장 밑으로 등줄기를 훅훅 볶는다. 로 고치면 돼"""},
                {"role": "assistant", "content": """봉는다는 볶는다인 것처럼 어색한 발음들도 문맥에 맞게 고쳐주면 돼."""},
                {"role": "user", "content": prompt}
            ],
         max_tokens = 1024,
        temperature = 0.7,
    )
        return completions["choices"][0]["message"]["content"]

    
    def set_origin_script(self):
        try:
            file = open("speech_to_text.txt", "r", encoding="utf-8")
            self.get_original_script = file.readlines()
            
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        except Exception as e:
            print("오류가 발생했습니다:", e)
            
        return self.get_original_script
            
    
    
    def get_corrected_script(self, set_origin_script):
        for user_input in self.get_original_script:
            self.corrected_script.append(self.cumulative_input(user_input, self.conversation_history, self.USERNAME, self.AI_NAME))
        return self.corrected_script
    
if __name__ == '__main__':
    script_correction = ScriptCorrection()
    s = script_correction.set_origin_script()
    ss = script_correction.get_corrected_script(s)
    for item in ss:
        print(item)
    