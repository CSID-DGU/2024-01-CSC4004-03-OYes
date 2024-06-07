import datetime
import os
import subprocess
import sys
import time
from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import FastAPI, File, UploadFile, Form
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
ABS_WORK_DIR = os.path.abspath(WORK_DIR)

tts = tts.VoiceGenerator()

# 프로그램 작동 로그 표시
execution_log: str = str()


async def save_file(file: IO):
    with NamedTemporaryFile("wb", delete=False) as temp_file:
        temp_file.write(file.read())
        return temp_file.name


@app.post("/speech-correction")
async def speech_correction(model: str = Form(...), rvc_enabled: bool = Form(...), file: UploadFile = File(...)):
    global execution_log
    execution_log = str()

    total_start_time = time.time()
    start_time = total_start_time
    path = await save_file(file.file)
    origin_script = execute_stt(path)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "1. STT 완료\n"
    current_log += f"인식된 스크립트: {origin_script}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log += current_log
    print(current_log)

    start_time = time.time()
    corrected_script = execute_correction(origin_script)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "2. Correction 완료\n"
    current_log += f"교정된 스크립트: {corrected_script}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log += current_log
    print(current_log)

    start_time = time.time()
    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S%f')
    basic_voice_file_name = 'basic_' + file_name_suffix + '.wav'
    basic_voice_path = os.path.join(ABS_WORK_DIR, basic_voice_file_name)
    execute_tts(corrected_script, basic_voice_path)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "3. TTS 완료\n"
    current_log += f"TTS 파일 경로: {basic_voice_path}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log += current_log
    print(current_log)

    if rvc_enabled:
        start_time = time.time()
        changed_voice_file_name = 'changed_' + file_name_suffix + '.wav'
        changed_voice_path = os.path.join(ABS_WORK_DIR, changed_voice_file_name)
        execute_voice_infer(basic_voice_path, changed_voice_path, model, 0.0, 12)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("Voice Change 완료")
        current_log = "4. Voice Change 완료\n"
        current_log += f"변조된 음성 파일 경로: {changed_voice_path}\n\n"
        current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
        execution_log += current_log
        print(current_log)
    else:
        changed_voice_path = basic_voice_path

    end_time = time.time()
    elapsed_time = end_time - total_start_time
    current_log = f"총 소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log += current_log
    print(current_log)

    return FileResponse(changed_voice_path, filename='correction_' + file_name_suffix + '.wav', media_type="audio/wav")


def execute_stt(origin_voice_path):
    stt.origin_voice_path = origin_voice_path
    stt.execute()
    return stt.origin_script


def execute_correction(origin_script):
    correction.origin_script = origin_script
    correction.execute()
    return correction.corrected_script


def execute_tts(corrected_script, basic_voice_path):
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
    execute_voice_infer(basic_voice_path, os.path.abspath(changed_voice_path), "IU", 0.0, 0)
    print("Voice Change 완료")
    print(changed_voice_path)

    return FileResponse(changed_voice_path, filename='correction_' + file_name_suffix + '.wav', media_type="audio/wav")


@app.get("/log")
async def get_log():
    print(execution_log)
    return execution_log.replace('\n', '<br>')


def execute_voice_infer(basic_voice_path, changed_voice_path, model_name, index_rate, f0_up_key):
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
