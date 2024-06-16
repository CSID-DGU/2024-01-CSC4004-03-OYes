# Speech Correction API 서버

> **생성형AI 및 RVC 기반 음성 교정 SW** `speechcorrection` 패키지를 API 서버로 실행하기 위한 코드입니다.

## 실행 방법

프로젝트의 최상위(root) 폴더에서 다음의 명령어를 수행합니다.

```shell
uvicorn api-server.main:app [--reload] [--host HOST_NAME] [--port PORT_NUMBER]
```
> `--reload`: 옵션 지정 시 소스 코드가 변경되었을 때 API 서버가 자동으로 재시작 됩니다.
> 
> `--host HOST_NAME`: API 서비스가 실행 될 host 주소를 입력합니다(ex. `--host 127.0.0.1`). 미입력 시 localhost에서 실행됩니다.
>
> `--port PORT_NUMBER` API 서비스가 실행 될 port 주소를 입력합니다(ex. `--port 8000`). 미입력 시 8000 포트로 지정됩니다.

## API 문서 보기

`/docs` URL로 접속하면 사용할 수 있는 API의 종류를 확인할 수 있으며, API 동작을 직접 테스트할 수 있습니다.

## API 종류

| 메서드  | 엔드포인트                |
|------|----------------------|
| POST | `/speech-correction` |

음성 파일을 받아 `/stt`, `/correction`, `/tts`, `/voice-change`를 한번에 수행하여 최종 음성 파일을 반환합니다.

### Request Form 데이터

- `model`(str): 모델 이름 (예: model_1)
- `rvc_enabled`(str): RVC 활성화 여부 (true 또는 false)
- `file`(UploadFile): 업로드 된 음성 파일.

### Response

- `content`: 변조된 음성 파일 (audio/wav)

---

| 메서드  | 엔드포인트  |
|------|--------|
| POST | `/stt` |

음성 파일을 받아 텍스트로 변환합니다.

### Request Form 데이터

- `file`(UploadFile): 업로드 된 음성 파일.

### Response

- `content`: 인식된 텍스트 (text/plain)

---

| 메서드  | 엔드포인트         |
|------|---------------|
| POST | `/correction` |

입력된 텍스트를 chatGPT를 이용하여 교정합니다.

### Request Form 데이터

- `origin_script`(str): 원본 텍스트

### Response

- `content`: 교정된 텍스트 (text/plain)

---

| 메서드  | 엔드포인트  |
|------|--------|
| POST | `/tts` |

교정된 텍스트를 받아 음성 파일로 변환합니다.

### Request Form 데이터

- `corrected_script`(str): 교정된 텍스트

### Response

- `content`: 생성된 음성 파일 (audio/wav)

---

| 메서드  | 엔드포인트           |
|------|-----------------|
| POST | `/voice-change` |

음성 파일을 받아 지정된 모델을 사용해 음성을 변조합니다.

### Request Form 데이터

- `model`(str): 모델 이름과 f0_up_key 정보를 포함한 문자열 (예: model_1)
- `file`(UploadFile): 업로드된 음성 파일.

### Response

- `content`: 변조된 음성 파일 (audio/wav)

---

| 메서드 | 엔드포인트  |
|-----|--------|
| GET | `/log` |

최근 실행 로그를 반환합니다.

### Request Form 데이터

없음

### Response

- `content`: 실행 로그 (text/plain)