## VoiceGenerator.py

--------

### 1. Coqui-ai TTS 설치

```cmd
pip install TTS
```

### 2. xtts_v2

Coqui-ai에서 제공하는 다국어 TTS

### 3. VoiceGenerator 클래스 설명

```python
VoiceGenerator.set_correction_script(string)
```

TTS 변환할 문자열을 입력 (inputType: string, return: None)

```python
VoiceGenerator.get_basic_voice()
```

입력받은 문자열을 이용하여 TTS 음성파일을 생성하고 파일의 절대주소를 반환 (inputType: None, return: string), 
문자열을 입력 받은 적이 없거나 빈 문자열이면 프로그램 종료(abort)

### 4. 출처 및 라이센스 정보

speaker_voice.wav : 음성 합성을 위해서 카이스트 오디오북 데이터셋(KAIST Audio Book Dataset)에서 남1_자기계발1 wav파일을 1번부터 18번까지 합침

Coqui-ai TTS : Mozilla Public License 2.0 <https://www.mozilla.org/en-US/MPL/2.0/>

xtts_v2 : Coqui Public Model License 1.0.0 <https://coqui.ai/cpml.txt>
