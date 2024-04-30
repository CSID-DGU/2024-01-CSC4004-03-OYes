import traceback
import logging
import os

logger = logging.getLogger(__name__)
now_dir = os.getcwd()

import numpy as np
import soundfile as sf
import torch
from io import BytesIO

from source.infer.lib.audio import load_audio, wav2
from source.infer.lib.infer_pack.models import (
    SynthesizerTrnMs256NSFsid,
    SynthesizerTrnMs256NSFsid_nono,
    SynthesizerTrnMs768NSFsid,
    SynthesizerTrnMs768NSFsid_nono,
)
from source.infer.modules.vc.pipeline import Pipeline
from source.infer.modules.vc.utils import *

from scipy.io import wavfile


class source:
    def __init__(self, config, model_name):
        self.n_spk = None
        self.tgt_sr = None
        self.net_g = None
        self.pipeline = None
        self.cpt = None
        self.version = None
        self.if_f0 = None
        self.version = None
        self.hubert_model = None

        self.config = config

        self.origin_voice_path = ""

        self.model_name, self.file_index = source.select_model(model_name)
        self.load_model(self.model_name)

    def load_voice(self, input_voice_path):
        
        audio = load_audio(input_voice_path, 16000)

        return audio

    def load_model(self, sid, *to_return_protect):
        logger.info("Get sid: " + sid)

        to_return_protect0 = {
            "visible": self.if_f0 != 0,
            "value": to_return_protect[0]
            if self.if_f0 != 0 and to_return_protect
            else 0.5,
            "__type__": "update",
        }
        to_return_protect1 = {
            "visible": self.if_f0 != 0,
            "value": to_return_protect[1]
            if self.if_f0 != 0 and to_return_protect
            else 0.33,
            "__type__": "update",
        }

        if sid == "" or sid == []:
            if self.hubert_model is not None:
                logger.info("Clean model cache")
                del (self.net_g, self.n_spk, self.hubert_model, self.tgt_sr)
                self.hubert_model = (
                    self.net_g
                ) = self.n_spk = self.hubert_model = self.tgt_sr = None
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                self.if_f0 = self.cpt.get("f0", 1)
                self.version = self.cpt.get("version", "v1")
                if self.version == "v1":
                    if self.if_f0 == 1:
                        self.net_g = SynthesizerTrnMs256NSFsid(
                            *self.cpt["config"], is_half=self.config.is_half
                        )
                    else:
                        self.net_g = SynthesizerTrnMs256NSFsid_nono(*self.cpt["config"])
                elif self.version == "v2":
                    if self.if_f0 == 1:
                        self.net_g = SynthesizerTrnMs768NSFsid(
                            *self.cpt["config"], is_half=self.config.is_half
                        )
                    else:
                        self.net_g = SynthesizerTrnMs768NSFsid_nono(*self.cpt["config"])
                del self.net_g, self.cpt
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            return (
                {"visible": False, "__type__": "update"},
                {
                    "visible": True,
                    "value": to_return_protect0,
                    "__type__": "update",
                },
                {
                    "visible": True,
                    "value": to_return_protect1,
                    "__type__": "update",
                },
                "",
                "",
            )
        person = "source/" + f'{os.getenv("weight_root")}/{sid}'
        logger.info(f"Loading: {person}")

        self.cpt = torch.load(person, map_location="cpu")
        self.tgt_sr = self.cpt["config"][-1]
        self.cpt["config"][-3] = self.cpt["weight"]["emb_g.weight"].shape[0]  # n_spk
        self.if_f0 = self.cpt.get("f0", 1)
        self.version = self.cpt.get("version", "v1")

        synthesizer_class = {
            ("v1", 1): SynthesizerTrnMs256NSFsid,
            ("v1", 0): SynthesizerTrnMs256NSFsid_nono,
            ("v2", 1): SynthesizerTrnMs768NSFsid,
            ("v2", 0): SynthesizerTrnMs768NSFsid_nono,
        }

        self.net_g = synthesizer_class.get(
            (self.version, self.if_f0), SynthesizerTrnMs256NSFsid
        )(*self.cpt["config"], is_half=self.config.is_half)

        del self.net_g.enc_q

        self.net_g.load_state_dict(self.cpt["weight"], strict=False)
        self.net_g.eval().to(self.config.device)
        if self.config.is_half:
            self.net_g = self.net_g.half()
        else:
            self.net_g = self.net_g.float()

        self.pipeline = Pipeline(self.tgt_sr, self.config)
        n_spk = self.cpt["config"][-3]
        index = {"value": get_index_path_from_model(sid), "__type__": "update"}
        logger.info("Select index: " + index["value"])

        return (
            (
                {"visible": True, "maximum": n_spk, "__type__": "update"},
                to_return_protect0,
                to_return_protect1,
                index,
                index,
            )
            if to_return_protect
            else {"visible": True, "maximum": n_spk, "__type__": "update"}
        )

    def get_changed_voice(
        self,
        input_voice_path,
        #file_index2,
        f0_up_key = 0,
        f0_file = None,
        f0_method = 'rmvpe',
        file_index = '',
        sid = 0,
        index_rate = 0.75,
        filter_radius = 3,
        resample_sr = 0,
        rms_mix_rate = 0.25,
        protect = 0.33,
    ):

        f0_up_key = int(f0_up_key)
        try:
            
            audio = self.load_voice(input_voice_path)
            audio_max = np.abs(audio).max() / 0.95
            if audio_max > 1:
                audio /= audio_max
            times = [0, 0, 0]

            if self.hubert_model is None:
                self.hubert_model = load_hubert(self.config)

            file_index = (
                (
                    file_index.strip(" ")
                    .strip('"')
                    .strip("\n")
                    .strip('"')
                    .strip(" ")
                    .replace("trained", "added")
                )
                if file_index != ""
                else self.file_index
            )

            audio_opt = self.pipeline.pipeline(
                self.hubert_model,
                self.net_g,
                sid,
                audio,
                input_voice_path,
                times,
                f0_up_key,
                f0_method,
                file_index,
                index_rate,
                self.if_f0,
                filter_radius,
                self.tgt_sr,
                resample_sr,
                rms_mix_rate,
                self.version,
                protect,
                f0_file,
            )
            if self.tgt_sr != resample_sr >= 16000:
                tgt_sr = resample_sr
            else:
                tgt_sr = self.tgt_sr
            index_info = (
                "Index:\n%s." % file_index
                if os.path.exists(file_index)
                else "Index not used."
            )

            output_path = input_voice_path[0 : input_voice_path.find('inference_wav')] + 'inferenced_wav/inferenced_output.wav'

            wavfile.write(output_path, tgt_sr, audio_opt)
            
            return (
                "Success.\n%s\nTime:\nnpy: %.2fs, f0: %.2fs, infer: %.2fs."
                % (index_info, *times),
                (tgt_sr, audio_opt),
            )
        except:
            info = traceback.format_exc()
            logger.warning(info)
            return info, (None, None)
        
    def select_model(model_name):
    
        for index_name in os.listdir(os.path.join("source", "logs", model_name)):

            if index_name.startswith('add'):
                if index_name.endswith('.index'):
                    print(index_name)
                    break

        file_index = now_dir + 'logs/' + model_name + '/' + index_name
        model_name += '.pth'

        return model_name, file_index
        
