from speechcorrection.voice.voice_base import VoiceBase
from infer.modules.vc.modules import VC
import os
from scipy.io import wavfile
from configs.config import Config

config = Config()


class VoiceChanger(VoiceBase):

    def __init__(self):
        super().__init__()

        self.__vc = VC(config)
        self.__voice_model = None
        self.__basic_voice_path = None
        self.__changed_voice_path = None
        self.__file_index = None
        self.__file_counter = 1

    def execute(self,
                sid=0,
                f0_up_key=0,
                f0_file=None,
                f0_method="rmvpe",
                index_rate=0,
                filter_radius=3,
                resample_sr=0,
                rms_mix_rate=0.25,
                protect=0.33
                ):

        result, (tgt_sr, audio_opt) = self.__vc.vc_single(
            sid=sid,
            input_audio_path=self.__basic_voice_path,
            f0_up_key=f0_up_key,
            f0_file=f0_file,
            f0_method=f0_method,
            file_index=None,
            file_index2=self.__file_index,
            index_rate=index_rate,
            filter_radius=filter_radius,
            resample_sr=resample_sr,
            rms_mix_rate=rms_mix_rate,
            protect=protect
        )

        print(result)
        self.write_changed_voice = (tgt_sr, audio_opt)

    @property
    def basic_voice_path(self):
        pass

    @basic_voice_path.setter
    def basic_voice_path(self, basic_voice_path):
        self.__basic_voice_path = os.path.abspath(basic_voice_path)

    @property
    def voice_model_name(self):
        pass

    @voice_model_name.setter
    def voice_model_name(self, model_name):
        self.__voice_model = model_name + ".pth"

    @property
    def changed_voice_path(self):
        pass

    @changed_voice_path.setter
    def changed_voice_path(self, changed_voice_path=os.path.join("assets", "vc_output", "vc_output.wav")):
        self.__changed_voice_path = changed_voice_path

    @property
    def load_vc_model(self):
        pass

    @load_vc_model.setter
    def load_vc_model(self, model_name):
        self.voice_model_name = model_name

        for index_name in os.listdir(os.path.join("logs", model_name)):

            if index_name.startswith('add'):
                if index_name.endswith('.index'):
                    break

        self.__file_index = os.path.join("logs", model_name, index_name)

        self.__vc.get_vc(self.__voice_model)

    @property
    def write_changed_voice(self):
        pass

    @write_changed_voice.setter
    def write_changed_voice(self, output):

        tgt_sr, audio_opt = output
        edited_path = self.__changed_voice_path

        while os.path.exists(edited_path):
            edited_path = self.__changed_voice_path[0: self.__changed_voice_path.find(".wav")] + "(" + str(
                self.__file_counter) + ")" + self.__changed_voice_path[self.__changed_voice_path.find(".wav"):]
            self.__file_counter += 1

        wavfile.write(edited_path, tgt_sr, audio_opt)
