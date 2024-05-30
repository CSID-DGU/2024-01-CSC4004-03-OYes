from speechcorrection.train.train_base import VoiceTrainBase
import os
from configs.config import Config
from sklearn.cluster import MiniBatchKMeans
import torch, platform
import numpy as np
import faiss
import fairseq
import pathlib
import json
from time import sleep
from subprocess import Popen
from random import shuffle
import warnings
import traceback
import threading
import shutil
import logging

logging.getLogger("numba").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
now_dir = os.path.join(os.getcwd())
outside_index_root = os.getenv("outside_index_root")
tmp = os.path.join(now_dir, "TEMP")
shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/infer_pack" % (now_dir), ignore_errors=True)
os.environ["TEMP"] = tmp
warnings.filterwarnings("ignore")
torch.manual_seed(114514)

config = Config()

ngpu = torch.cuda.device_count()
gpu_infos = []
mem = []
if_gpu_ok = False

if torch.cuda.is_available() or ngpu != 0:
    for i in range(ngpu):
        gpu_name = torch.cuda.get_device_name(i)
        if any(
            value in gpu_name.upper()
            for value in [
                "10",
                "16",
                "20",
                "30",
                "40",
                "A2",
                "A3",
                "A4",
                "P4",
                "A50",
                "500",
                "A60",
                "70",
                "80",
                "90",
                "M4",
                "T4",
                "TITAN",
            ]
        ):
            
            if_gpu_ok = True
            gpu_infos.append("%s\t%s" % (i, gpu_name))
            mem.append(
                int(
                    torch.cuda.get_device_properties(i).total_memory
                    / 1024
                    / 1024
                    / 1024
                    + 0.4
                )
            )

if if_gpu_ok and len(gpu_infos) > 0:
    gpu_info = "\n".join(gpu_infos)
    default_batch_size = min(mem) // 2
else:
    gpu_info = "gpu not found"
    default_batch_size = 1
gpus = "-".join([i[0] for i in gpu_infos])

sr_dict = {
    "32k": 32000,
    "40k": 40000,
    "48k": 48000,
}

def if_done(done, p):
    while 1:
        if p.poll() is None:
            sleep(0.5)
        else:
            break
    done[0] = True


def if_done_multi(done, ps):
    while 1:
        flag = 1
        for p in ps:
            if p.poll() is None:
                flag = 0
                sleep(0.5)
                break
        if flag == 1:
            break
    done[0] = True

class TrainVoice(VoiceTrainBase):

    def __init__(self):
        super().__init__()

        self.__total_epoch = 3
        self.__save_epoch = 3
        self.__sr = "40k"
        self.__if_f0 = True
        self.__dataset_path = ""
        self.__spk_id = 0
        self.__np_1 = int(np.ceil(config.n_cpu / 1.5))
        self.__f0method = "rmvpe_gpu"
        self.__batch_size = default_batch_size
        self.__if_save_latest = False
        self.__pretrained_G = os.path.join("assets", "pretrained_v2", "f0G40k.pth")
        self.__pretrained_D = os.path.join("assets", "pretrained_v2", "f0D40k.pth")
        self.__if_cache_gpu = False 
        self.__if_save_every_weights = False 
        self.__version = "v2"
        self.__gpus_rmvpe = "%s-%s" % (gpus, gpus)

    def execute(self, exp_dir):

        train_info = self.training(
        exp_dir,
        self.__total_epoch,
        self.__save_epoch,
        self.__sr,
        self.__if_f0,
        self.__dataset_path,
        self.__spk_id,
        self.__np_1,
        self.__f0method,
        self.__batch_size,
        self.__if_save_latest,
        self.__pretrained_G,
        self.__pretrained_D,
        gpus,
        self.__if_cache_gpu,
        self.__if_save_every_weights,
        self.__version,
        self.__gpus_rmvpe,
        )

        for i in train_info:
            pass

    @property
    def set_total_epoch(self):
        pass

    @set_total_epoch.setter
    def set_total_epoch(self, total_epoch = 2):
        self.__total_epoch = total_epoch

    @property
    def set_save_epoch(self):
        pass

    @set_save_epoch.setter
    def set_save_epoch(self, save_epoch = 2):
        self.__save_epoch = save_epoch

    @property
    def dataset_path(self):
        pass

    @dataset_path.setter
    def dataset_path(self, dataset_path):
        self.__dataset_path = os.path.abspath(dataset_path)

    def __preprocess_dataset(self, trainset_dir, exp_dir, sr, n_p):
        sr = sr_dict[sr]
        os.makedirs("%s/logs/%s" % (now_dir, exp_dir), exist_ok=True)
        f = open("%s/logs/%s/preprocess.log" % (now_dir, exp_dir), "w")
        f.close()
        cmd = '"%s" infer/modules/train/preprocess.py "%s" %s %s "%s/logs/%s" %s %.1f' % (
            config.python_cmd,
            trainset_dir,
            sr,
            n_p,
            now_dir,
            exp_dir,
            config.noparallel,
            config.preprocess_per,
        )
        logger.info("Execute: " + cmd)
        p = Popen(cmd, shell=True)

        done = [False]
        threading.Thread(
            target=if_done,
            args=(
                done,
                p,
            ),
        ).start()
        while 1:
            with open("%s/logs/%s/preprocess.log" % (now_dir, exp_dir), "r") as f:
                yield (f.read())
            sleep(1)
            if done[0]:
                break
        with open("%s/logs/%s/preprocess.log" % (now_dir, exp_dir), "r") as f:
            log = f.read()
        logger.info(log)
        yield log

    def __extract_f0_feature(self, gpus, n_p, f0method, if_f0, exp_dir, version19, gpus_rmvpe):
        gpus = gpus.split("-")
        os.makedirs("%s/logs/%s" % (now_dir, exp_dir), exist_ok=True)
        f = open("%s/logs/%s/extract_f0_feature.log" % (now_dir, exp_dir), "w")
        f.close()
        if if_f0:
            if f0method != "rmvpe_gpu":
                cmd = (
                    '"%s" infer/modules/train/extract/extract_f0_print.py "%s/logs/%s" %s %s'
                    % (
                        config.python_cmd,
                        now_dir,
                        exp_dir,
                        n_p,
                        f0method,
                    )
                )
                logger.info("Execute: " + cmd)
                p = Popen(
                    cmd, shell=True, cwd=now_dir
                )

                done = [False]
                threading.Thread(
                    target=if_done,
                    args=(
                        done,
                        p,
                    ),
                ).start()
            else:
                if gpus_rmvpe != "-":
                    gpus_rmvpe = gpus_rmvpe.split("-")
                    leng = len(gpus_rmvpe)
                    ps = []
                    for idx, n_g in enumerate(gpus_rmvpe):
                        cmd = (
                            '"%s" infer/modules/train/extract/extract_f0_rmvpe.py %s %s %s "%s/logs/%s" %s '
                            % (
                                config.python_cmd,
                                leng,
                                idx,
                                n_g,
                                now_dir,
                                exp_dir,
                                config.is_half,
                            )
                        )
                        logger.info("Execute: " + cmd)
                        p = Popen(
                            cmd, shell=True, cwd=now_dir
                        )
                        ps.append(p)

                    done = [False]
                    threading.Thread(
                        target=if_done_multi,  #
                        args=(
                            done,
                            ps,
                        ),
                    ).start()
                else:
                    cmd = (
                        config.python_cmd
                        + ' infer/modules/train/extract/extract_f0_rmvpe_dml.py "%s/logs/%s" '
                        % (
                            now_dir,
                            exp_dir,
                        )
                    )
                    logger.info("Execute: " + cmd)
                    p = Popen(
                        cmd, shell=True, cwd=now_dir
                    )
                    p.wait()
                    done = [True]
            while 1:
                with open(
                    "%s/logs/%s/extract_f0_feature.log" % (now_dir, exp_dir), "r"
                ) as f:
                    yield (f.read())
                sleep(1)
                if done[0]:
                    break
            with open("%s/logs/%s/extract_f0_feature.log" % (now_dir, exp_dir), "r") as f:
                log = f.read()
            logger.info(log)
            yield log

        leng = len(gpus)
        ps = []
        for idx, n_g in enumerate(gpus):
            cmd = (
                '"%s" infer/modules/train/extract_feature_print.py %s %s %s %s "%s/logs/%s" %s %s'
                % (
                    config.python_cmd,
                    config.device,
                    leng,
                    idx,
                    n_g,
                    now_dir,
                    exp_dir,
                    version19,
                    config.is_half,
                )
            )
            logger.info("Execute: " + cmd)
            p = Popen(
                cmd, shell=True, cwd=now_dir
            )
            ps.append(p)

        done = [False]
        threading.Thread(
            target=if_done_multi,
            args=(
                done,
                ps,
            ),
        ).start()
        while 1:
            with open("%s/logs/%s/extract_f0_feature.log" % (now_dir, exp_dir), "r") as f:
                yield (f.read())
            sleep(1)
            if done[0]:
                break
        with open("%s/logs/%s/extract_f0_feature.log" % (now_dir, exp_dir), "r") as f:
            log = f.read()
        logger.info(log)
        yield log


    def __get_pretrained_models(self, path_str, f0_str, sr2):
        if_pretrained_generator_exist = os.access(
            "assets/pretrained%s/%sG%s.pth" % (path_str, f0_str, sr2), os.F_OK
        )
        if_pretrained_discriminator_exist = os.access(
            "assets/pretrained%s/%sD%s.pth" % (path_str, f0_str, sr2), os.F_OK
        )
        if not if_pretrained_generator_exist:
            logger.warning(
                "assets/pretrained%s/%sG%s.pth not exist, will not use pretrained model",
                path_str,
                f0_str,
                sr2,
            )
        if not if_pretrained_discriminator_exist:
            logger.warning(
                "assets/pretrained%s/%sD%s.pth not exist, will not use pretrained model",
                path_str,
                f0_str,
                sr2,
            )
        return (
            (
                "assets/pretrained%s/%sG%s.pth" % (path_str, f0_str, sr2)
                if if_pretrained_generator_exist
                else ""
            ),
            (
                "assets/pretrained%s/%sD%s.pth" % (path_str, f0_str, sr2)
                if if_pretrained_discriminator_exist
                else ""
            ),
        )

    def __train(
        self,
        exp_dir1,
        sr2,
        if_f0_3,
        spk_id5,
        save_epoch10,
        total_epoch11,
        batch_size12,
        if_save_latest13,
        pretrained_G14,
        pretrained_D15,
        gpus16,
        if_cache_gpu17,
        if_save_every_weights18,
        version19,
    ):
        exp_dir = "%s/logs/%s" % (now_dir, exp_dir1)
        os.makedirs(exp_dir, exist_ok=True)
        gt_wavs_dir = "%s/0_gt_wavs" % (exp_dir)
        feature_dir = (
            "%s/3_feature256" % (exp_dir)
            if version19 == "v1"
            else "%s/3_feature768" % (exp_dir)
        )
        if if_f0_3:
            f0_dir = "%s/2a_f0" % (exp_dir)
            f0nsf_dir = "%s/2b-f0nsf" % (exp_dir)
            names = (
                set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)])
                & set([name.split(".")[0] for name in os.listdir(feature_dir)])
                & set([name.split(".")[0] for name in os.listdir(f0_dir)])
                & set([name.split(".")[0] for name in os.listdir(f0nsf_dir)])
            )
        else:
            names = set([name.split(".")[0] for name in os.listdir(gt_wavs_dir)]) & set(
                [name.split(".")[0] for name in os.listdir(feature_dir)]
            )
        opt = []
        for name in names:
            if if_f0_3:
                opt.append(
                    "%s/%s.wav|%s/%s.npy|%s/%s.wav.npy|%s/%s.wav.npy|%s"
                    % (
                        gt_wavs_dir.replace("\\", "\\\\"),
                        name,
                        feature_dir.replace("\\", "\\\\"),
                        name,
                        f0_dir.replace("\\", "\\\\"),
                        name,
                        f0nsf_dir.replace("\\", "\\\\"),
                        name,
                        spk_id5,
                    )
                )
            else:
                opt.append(
                    "%s/%s.wav|%s/%s.npy|%s"
                    % (
                        gt_wavs_dir.replace("\\", "\\\\"),
                        name,
                        feature_dir.replace("\\", "\\\\"),
                        name,
                        spk_id5,
                    )
                )
        fea_dim = 256 if version19 == "v1" else 768
        if if_f0_3:
            for _ in range(2):
                opt.append(
                    "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature%s/mute.npy|%s/logs/mute/2a_f0/mute.wav.npy|%s/logs/mute/2b-f0nsf/mute.wav.npy|%s"
                    % (now_dir, sr2, now_dir, fea_dim, now_dir, now_dir, spk_id5)
                )
        else:
            for _ in range(2):
                opt.append(
                    "%s/logs/mute/0_gt_wavs/mute%s.wav|%s/logs/mute/3_feature%s/mute.npy|%s"
                    % (now_dir, sr2, now_dir, fea_dim, spk_id5)
                )
        shuffle(opt)
        with open("%s/filelist.txt" % exp_dir, "w") as f:
            f.write("\n".join(opt))
        logger.debug("Write filelist done")

        logger.info("Use gpus: %s", str(gpus16))
        if pretrained_G14 == "":
            logger.info("No pretrained Generator")
        if pretrained_D15 == "":
            logger.info("No pretrained Discriminator")
        if version19 == "v1" or sr2 == "40k":
            config_path = "v1/%s.json" % sr2
        else:
            config_path = "v2/%s.json" % sr2
        config_save_path = os.path.join(exp_dir, "config.json")
        if not pathlib.Path(config_save_path).exists():
            with open(config_save_path, "w", encoding="utf-8") as f:
                json.dump(
                    config.json_config[config_path],
                    f,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )
                f.write("\n")
        if gpus16:
            cmd = (
                '"%s" infer/modules/train/train.py -e "%s" -sr %s -f0 %s -bs %s -g %s -te %s -se %s %s %s -l %s -c %s -sw %s -v %s'
                % (
                    config.python_cmd,
                    exp_dir1,
                    sr2,
                    1 if if_f0_3 else 0,
                    batch_size12,
                    gpus16,
                    total_epoch11,
                    save_epoch10,
                    "-pg %s" % pretrained_G14 if pretrained_G14 != "" else "",
                    "-pd %s" % pretrained_D15 if pretrained_D15 != "" else "",
                    1 if if_save_latest13 == True else 0,
                    1 if if_cache_gpu17 == True else 0,
                    1 if if_save_every_weights18 == True else 0,
                    version19,
                )
            )
        else:
            cmd = (
                '"%s" infer/modules/train/train.py -e "%s" -sr %s -f0 %s -bs %s -te %s -se %s %s %s -l %s -c %s -sw %s -v %s'
                % (
                    config.python_cmd,
                    exp_dir1,
                    sr2,
                    1 if if_f0_3 else 0,
                    batch_size12,
                    total_epoch11,
                    save_epoch10,
                    "-pg %s" % pretrained_G14 if pretrained_G14 != "" else "",
                    "-pd %s" % pretrained_D15 if pretrained_D15 != "" else "",
                    1 if if_save_latest13 == True else 0,
                    1 if if_cache_gpu17 == True else 0,
                    1 if if_save_every_weights18 == True else 0,
                    version19,
                )
            )
        logger.info("Execute: " + cmd)
        p = Popen(cmd, shell=True, cwd=now_dir)
        p.wait()
        return "you can find train log after training."

    def __train_index(self, exp_dir1, version19):

        exp_dir = "logs/%s" % (exp_dir1)
        os.makedirs(exp_dir, exist_ok=True)
        feature_dir = (
            "%s/3_feature256" % (exp_dir)
            if version19 == "v1"
            else "%s/3_feature768" % (exp_dir)
        )
        if not os.path.exists(feature_dir):
            return "need feature extract first!"
        listdir_res = list(os.listdir(feature_dir))
        if len(listdir_res) == 0:
            return "need feature extract first！"
        infos = []
        npys = []
        for name in sorted(listdir_res):
            phone = np.load("%s/%s" % (feature_dir, name))
            npys.append(phone)
        big_npy = np.concatenate(npys, 0)
        big_npy_idx = np.arange(big_npy.shape[0])
        np.random.shuffle(big_npy_idx)
        big_npy = big_npy[big_npy_idx]
        if big_npy.shape[0] > 2e5:
            infos.append("Trying doing kmeans %s shape to 10k centers." % big_npy.shape[0])
            yield "\n".join(infos)
            try:
                big_npy = (
                    MiniBatchKMeans(
                        n_clusters=10000,
                        verbose=True,
                        batch_size=256 * config.n_cpu,
                        compute_labels=False,
                        init="random",
                    )
                    .fit(big_npy)
                    .cluster_centers_
                )
            except:
                info = traceback.format_exc()
                logger.info(info)
                infos.append(info)
                yield "\n".join(infos)

        np.save("%s/total_fea.npy" % exp_dir, big_npy)
        n_ivf = min(int(16 * np.sqrt(big_npy.shape[0])), big_npy.shape[0] // 39)
        infos.append("%s,%s" % (big_npy.shape, n_ivf))
        yield "\n".join(infos)
        index = faiss.index_factory(256 if version19 == "v1" else 768, "IVF%s,Flat" % n_ivf)

        infos.append("training")
        yield "\n".join(infos)
        index_ivf = faiss.extract_index_ivf(index)  #
        index_ivf.nprobe = 1
        index.train(big_npy)
        faiss.write_index(
            index,
            "%s/trained_IVF%s_Flat_nprobe_%s_%s_%s.index"
            % (exp_dir, n_ivf, index_ivf.nprobe, exp_dir1, version19),
        )
        infos.append("adding")
        yield "\n".join(infos)
        batch_size_add = 8192
        for i in range(0, big_npy.shape[0], batch_size_add):
            index.add(big_npy[i : i + batch_size_add])
        faiss.write_index(
            index,
            "%s/added_IVF%s_Flat_nprobe_%s_%s_%s.index"
            % (exp_dir, n_ivf, index_ivf.nprobe, exp_dir1, version19),
        )
        infos.append(
            "creating index added_IVF%s_Flat_nprobe_%s_%s_%s.index"
            % (n_ivf, index_ivf.nprobe, exp_dir1, version19)
        )
        try:
            link = os.link if platform.system() == "Windows" else os.symlink
            link(
                "%s/added_IVF%s_Flat_nprobe_%s_%s_%s.index"
                % (exp_dir, n_ivf, index_ivf.nprobe, exp_dir1, version19),
                "%s/%s_IVF%s_Flat_nprobe_%s_%s_%s.index"
                % (
                    outside_index_root,
                    exp_dir1,
                    n_ivf,
                    index_ivf.nprobe,
                    exp_dir1,
                    version19,
                ),
            )
            infos.append("index to outside-%s" % (outside_index_root))
        except:
            infos.append("index to outside-%sfail" % (outside_index_root))

        yield "\n".join(infos)

    def training(
        self,
        exp_dir1,     
        total_epoch11,
        save_epoch10,
        sr2,
        if_f0_3,
        trainset_dir4,
        spk_id5,
        np7,
        f0method8,
        batch_size12,
        if_save_latest13,
        pretrained_G14,
        pretrained_D15,
        gpus16,
        if_cache_gpu17,
        if_save_every_weights18,
        version19,
        gpus_rmvpe,
    ):
        infos = []

        def get_info_str(strr):
            infos.append(strr)
            return "\n".join(infos)

        yield get_info_str("step1:preprocess dataset")
        [get_info_str(_) for _ in self.__preprocess_dataset(trainset_dir4, exp_dir1, sr2, np7)]

        yield get_info_str("step2:extract feature")
        [
            get_info_str(_)
            for _ in self.__extract_f0_feature(
                gpus16, np7, f0method8, if_f0_3, exp_dir1, version19, gpus_rmvpe
            )
        ]

        yield get_info_str("step3a:train")
        self.__train(
            exp_dir1,
            sr2,
            if_f0_3,
            spk_id5,
            save_epoch10,
            total_epoch11,
            batch_size12,
            if_save_latest13,
            pretrained_G14,
            pretrained_D15,
            gpus16,
            if_cache_gpu17,
            if_save_every_weights18,
            version19,
        )
        yield get_info_str("you can find train.log after training")

        [get_info_str(_) for _ in self.__train_index(exp_dir1, version19)]
        yield get_info_str("training process end")