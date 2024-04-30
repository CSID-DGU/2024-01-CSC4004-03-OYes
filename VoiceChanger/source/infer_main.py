import os
import sys

from dotenv import load_dotenv
load_dotenv()

now_dir = os.getcwd()
sys.path.append(now_dir)

from infer.modules.vc.modules import VC
from configs.config import Config

config = Config()
vc = VC(config)

def model_select(model_name):
    
    for index_name in os.listdir('logs/' + model_name):

        if index_name.startswith('add'):
            if index_name.endswith('.index'):
                print(index_name)
                break

    file_index = now_dir + 'logs/' + model_name + '/' + index_name
    model_name += '.pth'

    return model_name, file_index

model_name, file_index = model_select('guanguanV1') #name of your model
input_file_name = 'test1' #name of wav file to inference

vc.get_vc(model_name)

while(True):

    if input("start?(y/n)") == 'y':
        vc.vc_infer(input_file_name, file_index) #inference
    else:
        break

#infer parameter

#sid_pth = 'guanguanV1.pth' #trained model
#input_audio_name = 'test1.wav' #input wav
#file_index_1 = now_dir + 'logs/' + model_name + '.index'
#sid = 0
#input_audio_path = now_dir + "\\assets\\inference_wav\\" + input_audio_name #input wav path / 함수 호출 시 인수
#f0_up_key = 12 #key of voice / 남성 wav를 여성 voice로 출력할 때는 12, 반대는 -12로 설정 / 일단은 0으로 설정
#f0_file_value = None
#f0_method = 'rmvpe' #inference method / 일반적으로 rmvpe 사용
#file_index_0 = ''
#index_ratio = 0.75 #index 반영 비율 / 비율이 높을 수록 trained model의 목소리를 따라감
#filter_radius = 3
#resample_sr = 0
#rms_mix_rate = 0.25
#protect_0 = 0.33 #호흡 시 숨소리 보정 / 비율이 높으면 model의 특성이 강해짐
#protect_1 = 0.33