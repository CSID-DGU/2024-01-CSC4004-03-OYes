import os
import sys

argument_input_list = input().strip().split()

BASIC_VOICE_PATH = str(argument_input_list[0])
CHANGED_VOICE_PATH = str(argument_input_list[1])
MODEL_NAME = str(argument_input_list[2])
INDEX_RATE = float(argument_input_list[3])
F0_UP_KEY = int(argument_input_list[4])

print("===voice_infer_argv===")
print(BASIC_VOICE_PATH, CHANGED_VOICE_PATH, MODEL_NAME, INDEX_RATE, F0_UP_KEY)

module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

rvc_path = os.path.abspath(os.path.join('./Retrieval-based-Voice-Conversion-WebUI-main'))
if rvc_path not in sys.path:
    sys.path.append(rvc_path)

origin_path = os.getcwd()

os.chdir(rvc_path)
from dotenv import load_dotenv

load_dotenv()

from speechcorrection import voice

voice_changer = voice.VoiceChanger()
voice_changer.basic_voice_path = BASIC_VOICE_PATH
voice_changer.changed_voice_path = CHANGED_VOICE_PATH
voice_changer.load_vc_model = MODEL_NAME

voice_changer.execute(index_rate=INDEX_RATE, f0_up_key=F0_UP_KEY)

os.chdir(origin_path)
