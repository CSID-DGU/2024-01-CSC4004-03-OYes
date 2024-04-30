#region 필요한 모듈
from dotenv import load_dotenv
load_dotenv()

from source.configs.config import Config

config = Config()
#endregion 필요한 모듈

#region 클래스 호출 및 사용 예시
user_cmd = int(input("infer(1), train(2) quit(3): "))

if user_cmd == 1:
    from source.infer.modules.vc.modules import VoiceChanger

    model_name = input("enter trained model name: ")
    vc = VoiceChanger(config, model_name)

    input_voice_path = input("enter origin voice name: ")

    result = vc.get_changed_voice(input_voice_path) #변조
    print(result)

elif user_cmd == 2:
    from source.infer.modules.train.train_module import TrainVoice

    training = TrainVoice()

    new_model_name = input("enter your model name: ")

    #training.set_epoch(2, 2) // 현재 전체 epoch와 몇 epoch마다 저장할 것인지 모두 2로 설정되어 있음
    
    training.vc_train(new_model_name) #학습
#endregion 클래스 호출 및 사용 예시