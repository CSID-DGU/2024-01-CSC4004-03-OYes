# 설치해야 하는 패키지: fastapi, python-multipart, uvicorn
# 실행방법: 파이썬 파일이 있는 폴더에서 [ uvicorn test-api:app --reload ] 명령 실행
# 호출방법: http://127.0.0.1:8000/speech-correction 으로 post 요청
# 전달값: model, rvc_enabled, file

import datetime
from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

app = FastAPI()


async def save_file(file: IO):
    with NamedTemporaryFile("wb", delete=False) as temp_file:
        temp_file.write(file.read())
        return temp_file.name


@app.post("/speech-correction")
async def speech_correction(model: str = Form(...), rvc_enabled: bool = Form(...), file: UploadFile = File(...)):
    path = await save_file(file.file)

    file_name_suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S%f')
    print(f"model: {model}")
    print(f"rvc_enabled: {rvc_enabled}")
    print(f"path: {path}")

    return FileResponse(path, filename='test' + file_name_suffix + '.wav', media_type="audio/wav")
