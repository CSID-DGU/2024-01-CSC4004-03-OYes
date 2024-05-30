import sys
import os

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

rvc_path = os.path.abspath(os.path.join('../Retrieval-based-Voice-Conversion-WebUI-main'))
if rvc_path not in sys.path:
    sys.path.append(rvc_path)

origin_path = os.getcwd()

os.chdir(rvc_path)

from dotenv import load_dotenv
load_dotenv()

from speechcorrection import voice

voice_changer = voice.VoiceChanger()
voice_changer.basic_voice_path = "origin/voice/path"
voice_changer.changed_voice_path = os.path.join(rvc_path, "assets", "vc_output", "vc_output.wav")
voice_changer.load_vc_model = "trained_model_name"

voice_changer.execute(index_rate = 0.75)

os.chdir(origin_path)