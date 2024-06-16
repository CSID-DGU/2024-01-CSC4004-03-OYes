# RVC 및 생성형 AI 기반 음성 교정 SW 개발

2024-01-CSC4004-03-OYes
---

2024-1 공개SW프로젝트(CSC4004) 03분반

5조 오예스(Open-source Yes!)

## 팀 구성원

| 학과      | 이름  | 역할                  |
|---------|-----|---------------------|
| 컴퓨터공학전공 | 김해환 | 프로젝트 총괄(팀장), API 개발 |
| 컴퓨터공학전공 | 김상현 | TTS 모듈, 데모서비스 개발    |
| 컴퓨터공학전공 | 장윤영 | Correction 모듈 개발    |
| 컴퓨터공학전공 | 장태영 | STT 모듈 개발           |
| 철학과     | 최용희 | Voice 모듈 개발         |

## 프로젝트 소개

> 의사소통에 있어 사투리, 발음, 억양, 말의 빠르기 등 화자의 의미전달을 방해하는 음성적인 요소를 생성형 AI와 RVC를 바탕으로 교정하여
> 원활하고 자연스러운 의사소통을 도와주는 음성 교정 SW 소프트웨어 개발 프로젝트입니다.

![의미전달 방해요소 예시](docs/miscommunication.png)

## 작동 구조도

![SW 작동 구조도](docs/scgr-structure-diagram.png)

## 프로젝트 산출물

### [speechcorrection 파이썬 패키지](speechcorrection)

> RVC 및 생성형 AI 기반 음성 교정 SW가 구현된 파이썬 패키지

### [API 서버](api-server)

> speechcorrection 파이썬 패키지 API 형태로 사용할 수 있는 API 서버

### [데모 서비스](demoservice)

> API 서버를 간단하게 사용해 볼 수 있는 데모 웹 서비스
