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

# 프로그램 작동 로그
execution_log: str = str()


async def save_file(file: IO):
    with NamedTemporaryFile("wb", delete=False) as temp_file:
        temp_file.write(file.read())
        return temp_file.name


@app.post("/speech-correction")
async def speech_correction(model: str = Form(...), rvc_enabled: str = Form(...), file: UploadFile = File(...)):
    global execution_log
    execution_log = str()

    # RVC 활성화 여부 체크
    if rvc_enabled == "true":
        rvc_enabled_bool = bool(True)
    else:
        rvc_enabled_bool = bool(False)

    # 모델 이름 및 f0_up_key 정보 체크
    model_name = str(model.split("_")[0])
    model_f0_up_key = int(model.split("_")[1])

    # STT 모듈 동작
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

    # Correction 모듈 동작
    start_time = time.time()
    corrected_script = execute_correction(origin_script)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "2. Correction 완료\n"
    current_log += f"교정된 스크립트: {corrected_script}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log += current_log
    print(current_log)

    # TTS 모듈 동작
    start_time = time.time()
    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
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

    # Voice 모듈 동작
    if rvc_enabled_bool:
        start_time = time.time()
        changed_voice_file_name = 'changed_' + file_name_suffix + '.wav'
        changed_voice_path = os.path.join(ABS_WORK_DIR, changed_voice_file_name)
        execute_voice_infer(basic_voice_path, changed_voice_path, model_name, 0.0, model_f0_up_key)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("Voice Change 완료")
        current_log = "4. Voice Change 완료\n"
        current_log += f"변조된 음성 파일 경로: {changed_voice_path}\n\n"
        current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
        execution_log += current_log
        print(current_log)
    else:
        model_name = "TTS"
        changed_voice_path = basic_voice_path

    end_time = time.time()
    elapsed_time = end_time - total_start_time
    current_log = f"총 소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log += current_log
    print(current_log)

    return FileResponse(changed_voice_path, filename=f"c_{model_name}_{file_name_suffix}.wav",
                        media_type="audio/wav")


@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    global execution_log
    start_time = time.time()
    path = await save_file(file.file)
    origin_script = execute_stt(path)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "STT 완료\n"
    current_log += f"인식된 스크립트: {origin_script}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log = current_log
    print(current_log)

    return origin_script


@app.post("/correction")
async def text_correction(origin_script: str = Form(...)):
    global execution_log
    start_time = time.time()
    corrected_script = execute_correction(origin_script)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "Correction 완료\n"
    current_log += f"교정된 스크립트: {corrected_script}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log = current_log
    print(current_log)

    return corrected_script


@app.post("/tts")
async def text_to_speech(corrected_script: str = Form(...)):
    global execution_log
    start_time = time.time()
    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S_%f')
    basic_voice_file_name = 'basic_' + file_name_suffix + '.wav'
    basic_voice_path = os.path.join(ABS_WORK_DIR, basic_voice_file_name)
    execute_tts(corrected_script, basic_voice_path)
    end_time = time.time()
    elapsed_time = end_time - start_time

    current_log = "3. TTS 완료\n"
    current_log += f"TTS 파일 경로: {basic_voice_path}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log = current_log
    print(current_log)

    return FileResponse(basic_voice_path, filename=f"tts_{file_name_suffix}.wav", media_type="audio/wav")


@app.post("/voice-change")
async def voice_infer(model: str = Form(...), file: UploadFile = File(...)):
    model_name = str(model.split("_")[0])
    model_f0_up_key = int(model.split("_")[1])
    basic_voice_path = await save_file(file.file)

    global execution_log
    start_time = time.time()
    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S%f')
    changed_voice_file_name = 'changed_' + file_name_suffix + '.wav'
    changed_voice_path = os.path.join(ABS_WORK_DIR, changed_voice_file_name)
    execute_voice_infer(basic_voice_path, changed_voice_path, model_name, 0.0, model_f0_up_key)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Voice Change 완료")
    current_log = "4. Voice Change 완료\n"
    current_log += f"변조된 음성 파일 경로: {changed_voice_path}\n\n"
    current_log += f"소요 시간: {elapsed_time:.6f} sec\n\n"
    execution_log = current_log
    print(current_log)

    return FileResponse(changed_voice_path, filename=f"infer_{model_name}_{file_name_suffix}.wav",
                        media_type="audio/wav")


@app.get("/log")
async def get_log():
    print(execution_log)
    return execution_log.replace('\n', '<br>')


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
    return True


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
        return True
    except subprocess.TimeoutExpired:
        proc.kill()
        return False
