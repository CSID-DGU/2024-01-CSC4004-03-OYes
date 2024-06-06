import datetime
import os
import subprocess
import sys
import time
from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

# STT 객체 생성
from speechcorrection import stt

stt = stt.ScriptGenerator()

# Correction 객체 생성
from dotenv import load_dotenv
from speechcorrection import correction

load_dotenv(verbose=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
correction = correction.ScriptCorrection()
correction.api_key = OPENAI_API_KEY

# TTS 객체 생성
from speechcorrection import tts

WORK_DIR = "test/demo-file/"

tts = tts.VoiceGenerator()


async def save_file(file: IO):
    with NamedTemporaryFile("wb", delete=False) as temp_file:
        temp_file.write(file.read())
        return temp_file.name


@app.post("/speech-correction")
async def speech_correction(file: UploadFile = File(...)):
    path = await save_file(file.file)
    origin_script = stt_execute(path)
    print("STT 완료")
    print(origin_script)

    corrected_script = correction_execute(origin_script)
    print("Correction 완료")
    print(corrected_script)

    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S%f')
    basic_voice_file_name = 'basic_' + file_name_suffix + '.wav'
    basic_voice_path = os.path.join(WORK_DIR, basic_voice_file_name)
    tts_execute(corrected_script, basic_voice_path)
    print("TTS 완료")
    print(basic_voice_path)
    time.sleep(10)

    changed_voice_file_name = 'changed_' + file_name_suffix + '.wav'
    changed_voice_path = os.path.join(WORK_DIR, changed_voice_file_name)
    voice_infer_execute(basic_voice_path, os.path.abspath(changed_voice_path), "IU", 0.0, 12)
    print("Voice Change 완료")
    print(changed_voice_path)

    return FileResponse(changed_voice_path, filename='correction_' + file_name_suffix + '.wav', media_type="audio/wav")


def stt_execute(origin_voice_path):
    stt.origin_voice_path = origin_voice_path
    stt.execute()
    return stt.origin_script


def correction_execute(origin_script):
    correction.origin_script = origin_script
    correction.execute()
    return correction.corrected_script


def tts_execute(corrected_script, basic_voice_path):
    tts.corrected_script = corrected_script
    tts.basic_voice_path = basic_voice_path
    tts.execute()
    # return FileResponse(BASIC_VOICE_PATH, filename="speech-correction.wav", media_type="audio/wav")


@app.post("/voice-change")
async def voice_infer(file: UploadFile = File(...)):
    basic_voice_path = await save_file(file.file)
    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S%f')
    changed_voice_file_name = 'changed_' + file_name_suffix + '.wav'
    changed_voice_path = os.path.join(WORK_DIR, changed_voice_file_name)
    voice_infer_execute(basic_voice_path, os.path.abspath(changed_voice_path), "IU", 0.0, 12)
    print("Voice Change 완료")
    print(changed_voice_path)

    return FileResponse(changed_voice_path, filename='correction_' + file_name_suffix + '.wav', media_type="audio/wav")


def voice_infer_execute(basic_voice_path, changed_voice_path, model_name, index_rate, f0_up_key):
    print(basic_voice_path, changed_voice_path, model_name, index_rate, f0_up_key)
    proc = subprocess.Popen(
        f"{sys.executable} api-server/voice_infer.py",
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8")
    try:
        out, errs = proc.communicate(
            input=f"{basic_voice_path} {changed_voice_path} {model_name} {index_rate} {f0_up_key}", timeout=3000)
        print("====errs====")
        print(errs)
        print("====out====")
        print(out)
    except subprocess.TimeoutExpired:
        proc.kill()
