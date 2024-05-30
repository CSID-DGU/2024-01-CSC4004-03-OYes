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

from speechcorrection import train

voice_trainer = train.TrainVoice()
voice_trainer.set_total_epoch = 2
voice_trainer.set_save_epoch = 2
voice_trainer.dataset_path = os.path.join(rvc_path, "assets", "dataset")

model_name = input("enter new model name:")

voice_trainer.execute(model_name)

os.chdir(origin_path)