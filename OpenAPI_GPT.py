import openai
import time

# key 추가

messages = [] 
predefined_messages = [] 

for msg in predefined_messages:
    messages.append({"role": "user", "content": msg})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    assistant_content = completion.choices[0].message["content"].strip()
    messages.append({"role": "assistant", "content": assistant_content})

while True:
    user_content = input("user : ")
    messages.append({"role": "user", "content": f"잘못된 발음을 옮긴 텍스트를 알려줄 거야 이걸 문맥에 맞게 고쳐줘, {user_content}"})
    # messages.append({"role": "user", "content": f"{user_content} + 를 문맥에 맞게 고쳐줘"})
    # messages.append({"role": "user", "content": f"{user_content} + 를 자연스럽게 수정해줘"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    assistant_content = completion.choices[0].message["content"].strip()

    messages.append({"role": "assistant", "content": f"{assistant_content}"})

    print(f"GPT : {assistant_content}")
    time.sleep(5)