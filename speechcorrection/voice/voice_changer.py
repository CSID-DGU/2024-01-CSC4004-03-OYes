# from speechcorrection.voice.voice_base import VoiceBase
from voice_base import VoiceBase
from infer.modules.vc.modules import VC

import os

now_dir = os.getcwd()


class VoiceChanger(VoiceBase):

    def __init__(self, config):
        super().__init__()
        self.__vc = VC(config)
        self.__model_name = None
        self.__basic_voice_path = None
        self.__changed_voice_path = None
        self.__file_index = None
        self.__file_counter = 1

    def execute(
        self,
        sid1=0,
        f0_up_key3=0,
        f0_file4=None,
        f0_method5="rmvpe",
        index_rate8=0,
        filter_radius9=3,
        resample_sr10=0,
        rms_mix_rate11=0.25,
        protect12=0.33,
    ):

        result, (tgt_sr, audio_opt) = self.__vc.vc_single(
            sid=sid1,
            input_audio_path=self.__basic_voice_path,
            f0_up_key=f0_up_key3,
            f0_file=f0_file4,
            f0_method=f0_method5,
            file_index=None,
            file_index2=self.__file_index,
            index_rate=index_rate8,
            filter_radius=filter_radius9,
            resample_sr=resample_sr10,
            rms_mix_rate=rms_mix_rate11,
            protect=protect12,
        )

        print(result)
        self.write_changed_voice = (tgt_sr, audio_opt)

    @property
    def basic_voice_path(self):
        pass

    @basic_voice_path.setter
    def basic_voice_path(self, basic_voice_path):
        self.__basic_voice_path = basic_voice_path

    @property
    def changed_voice_path(self):
        pass

    @changed_voice_path.setter
    def changed_voice_path(
        self,
        changed_voice_path=os.path.join(
            now_dir, "assets", "vc_output", "vc_output.wav"
        ),
    ):
        self.__changed_voice_path = changed_voice_path

    @property
    def load_vc_model(self):
        pass

    @load_vc_model.setter
    def load_vc_model(self, model_name):
        self.__model_name = model_name + ".pth"

        for index_name in os.listdir(os.path.join("logs", model_name)):

            if index_name.startswith("add"):
                if index_name.endswith(".index"):
                    break

        self.__file_index = os.path.join(now_dir, "logs", model_name, index_name)

        self.__vc.get_vc(self.__model_name)

    @property
    def write_changed_voice(self):
        pass

    @write_changed_voice.setter
    def write_changed_voice(self, output):

        tgt_sr, audio_opt = output
        edited_path = self.__changed_voice_path

        if os.path.exists(self.__changed_voice_path):
            edited_path = (
                self.__changed_voice_path[0 : self.__changed_voice_path.find(".wav")]
                + "("
                + str(self.__file_counter)
                + ")"
                + self.__changed_voice_path[self.__changed_voice_path.find(".wav") :]
            )
            self.__file_counter += 1

        wavfile.write(edited_path, tgt_sr, audio_opt)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    from configs.config import Config

    config = Config()

    from scipy.io import wavfile

    voice_changer = VoiceChanger(config)
    voice_changer.basic_voice_path = "rvc_test_origin.wav"
    voice_changer.changed_voice_path = os.path.join(
        now_dir, "assets", "vc_output", "vc_output.wav"
    )
    voice_changer.load_vc_model = "IU"

    voice_changer.execute()
