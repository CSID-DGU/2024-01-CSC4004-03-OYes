import openai
import time
import pandas as pd

INITIAL_PROMPT = ('''
    당신은 오류가 있는 텍스트를 문맥에 맞게 바꾸어주는 친절한 AI 비서입니다.
''')
conversation_history = INITIAL_PROMPT + "\n"

USERNAME = "USER"
AI_NAME = "GPT"


def cumulative_input(
        input_str: str,
        conversation_history: str,
        USERNAME: str,
        AI_NAME: str,
):
    # Update the conversation history
    conversation_history += f"{USERNAME}: {input_str}\n"

    # Generate a response using GPT-3
    message = get_response(conversation_history)
    # Update the conversation history
    conversation_history += f"{AI_NAME}: {message}\n"

    # Print the response
    print(f'{AI_NAME}: {message}')

    return conversation_history


def get_response(prompt):
    """Returns the response for the given prompt using the OpenAI API."""
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "잘못된 발음을 옮긴 텍스트를 알려줄 거야 이걸 문맥에 맞게 고쳐줘"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.7,
    )
    return completions["choices"][0]["message"]["content"]


# 예시
arr = ["여름장이란 애시댕초에 글러서 해는 아직 증천에 있건만 장판은 벌써 쓸쓸하고 더운 햇발이 벌러 놓은 전시장 밑으루 등줄기를 훅훅 봉는다.",
       "마울 사람들은 거이 돌아간 뒤요, 팔리지 몬한 나무꾼 패가 길거리에 궁시거리고 있었으나, 석우 병이나 받고 고깃마리나 사면 족할 컷이 언제까지든지 버티고 있을 법은 읎다."]

for user_input in arr:
    conversation_history = cumulative_input(user_input, conversation_history, USERNAME, AI_NAME)
    conversation_history

# while True:
#     user_input = input("잘못된 문장을 입력하세요: ")
#     conversation_history = cumulative_input(user_input, conversation_history, USERNAME, AI_NAME)
#     conversation_history
