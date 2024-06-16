# RVC 및 생성형 AI 기반 음성 교정 SW 개발

2024-01-CSC4004-03-OYes
---

2024-1 공개SW프로젝트(CSC4004) 03분반 - 5조 오예스(Open-source Yes!)

## 🧑‍🤝‍🧑 팀 구성원

| 학과      | 이름  | 역할                  |
|---------|-----|---------------------|
| 컴퓨터공학전공 | 김해환 | 프로젝트 총괄(팀장), API 개발 |
| 컴퓨터공학전공 | 김상현 | TTS 모듈, 데모서비스 개발    |
| 컴퓨터공학전공 | 장윤영 | Correction 모듈 개발    |
| 컴퓨터공학전공 | 장태영 | STT 모듈 개발           |
| 철학과     | 최용희 | Voice 모듈 개발         |

## ✏️ 프로젝트 소개

본 프로젝트는 의사소통에 있어 사투리, 발음, 억양, 말의 빠르기 등 화자의 의미전달을 방해하는 음성적인 요소를 생성형 AI와 RVC를 바탕으로 교정하여 원활하고 자연스러운 의사소통을 도와주는 음성 교정 SW
소프트웨어 개발 프로젝트입니다.

<p align="center">
  <img src="docs/miscommunication.png">
</p>

## 🔍 작동 구조도

<p align="center">
  <img src="docs/scgr-structure-diagram.png">
</p>

## 📀 프로젝트 산출물

### [speechcorrection 파이썬 패키지](speechcorrection)

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

> RVC 및 생성형 AI 기반 음성 교정 SW가 구현된 파이썬 패키지

아래의 하위패키지를 import하여 사용합니다.

```python
from speechcorrection import stt
from speechcorrection import correction
from speechcorrection import tts
from speechcorrection import voice
from speechcorrection import train
```

#### stt 하위패키지 사용 예제

```python
from speechcorrection import stt

stt = stt.ScriptGenerator()

stt.origin_voice_path = "FILE_PATH"
stt.execute()
print(stt.origin_script)
```

#### correction 하위패키지 사용 예제

```python
import os
from dotenv import load_dotenv
from speechcorrection import correction

load_dotenv(verbose=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
correction = correction.ScriptCorrection()
correction.api_key = OPENAI_API_KEY

correction.origin_script = "ORIGIN_SCRIPT"
correction.execute()
print(correction.corrected_script)
```

#### tts 하위패키지 사용 예제

```python
from speechcorrection import tts

tts = tts.VoiceGenerator()

tts.corrected_script = "SCRIPT"
tts.basic_voice_path = "FILE_SAVE_PATH"
tts.execute()
```

#### voice 하위패키지 사용 예제

- 목소리 모델 학습 예제는 [train_test.py](test/train_test.py)를 참고해주세요.
    - 학습할 목소리 데이터 셋은 `Retrieval-based-Voice-Conversion-WebUI-main/assets/dataset/` 폴더에 복사합니다.
    - 학습된 목소리 모델은 `Retrieval-based-Voice-Conversion-WebUI-main/assets/weights/` 폴더에 `.pth` 파일로 저장됩니다.


- 목소리 변조 예제는 [infer_test.py](test/infer_test.py)를 참고해주세요.

---

### 2. [API 서버](api-server)

<img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white">

> speechcorrection 파이썬 패키지 API 형태로 사용할 수 있는 API 서버

실행 방법 및 API 사용 방법은 [api-server/README.md](api-server/README.md)를 참고해주세요.

---

### 3. [데모 서비스](demoservice)

<img src="https://img.shields.io/badge/node.js-339933?style=for-the-badge&logo=Node.js&logoColor=white"/> <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"> <img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>

> API 서버를 간단하게 사용해 볼 수 있는 데모 웹 서비스

실행 방법은 [demoservice/README.md](demoservice/README.md)를 참고해주세요.

## 🛠️ 설치 방법

1. 아래 명령어를 실행하여 필요한 패키지를 설치합니다.

```shell
pip install -r requirements.txt
```

2. [Retrieval-based-Voice-Conversion-WebUI-main.zip](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/archive/refs/heads/main.zip)
   파일을 다운받아 압축파일명 폴더에 풀고, 폴더채로 프로젝트 최상단(루트)에 복사합니다.


3. [Google Cloud 콘솔](https://cloud.google.com/iam/docs/keys-create-delete?hl=ko#iam-service-account-keys-create-console)
   에서 아래와 같이 JSON 유형의 서비스 계정 키를 생성하여, `auth_key.json`이름으로 프로젝트 최상단(루트)에 저장합니다.

```json
{
  "type": "service_account",
  "project_id": "PROJECT_ID",
  "private_key_id": "KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\nPRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "SERVICE_ACCOUNT_EMAIL",
  "client_id": "CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/SERVICE_ACCOUNT_EMAIL",
  "universe_domain": "googleapis.com"
}
```

4. [OpenAI API 플랫폼](https://platform.openai.com/)에서 OpenAI API키를 생성합니다.


5. 아래와 같이 프로젝트 최상단에 위치한 `.env` 파일의 `"OPENAI_API_KEY"` 부분에 생성한 OpenAI API키를 작성하여 저장합니다.

```
OPENAI_API_KEY = "OPENAI_API_KEY"
OPENBLAS_NUM_THREADS = 1
no_proxy = localhost, 127.0.0.1, ::1

# RVC 모델 경로 설정
weight_root = assets/weights
weight_uvr5_root = assets/uvr5_weights
index_root = logs
outside_index_root = assets/indices
rmvpe_root = assets/rmvpe
```

## 🔖 Credits

[whisper](https://github.com/openai/whisper) / MIT License / Copyright (c) 2022 OpenAI

[openai-python](https://github.com/openai/openai-python) / Apache-2.0 license / openai

[google-cloud-python](https://github.com/googleapis/google-cloud-python) / Apache-2.0 license / googleapis

[Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) / MIT License / Copyright (c) 2023 liujing04 / Copyright (c) 2023 源文雨 / Copyright (c) 2023 Ftps

[FastAPI](https://github.com/tiangolo/fastapi) / MIT License / Copyright (c) 2018 Sebastián Ramírez

[react](https://github.com/facebook/react) / MIT License / Copyright (c) Meta Platforms, Inc. and affiliates.

[bootstrap](https://github.com/twbs/bootstrap) / MIT License / Copyright (c) 2011-2024 The Bootstrap Authors

