# ScriptGenerator.py

## 1. pytorch 설치

```pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 ```

## 2. ffmpeg 설치

```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

## 3. whisper 설치

```pip install git+https://github.com/openai/whisper.git```

## 4. 메소드 정의

```python
ScriptGenerator.set_origin_voice()
```

매개변수로 받은 음성 파일의 경로를 멤버 변수에 저장하는 메소드

```python
ScriptGenerator.get_origin_script()
``` 

음성을 텍스트로 변환한 텍스트 파일의 경로를 저장한 멤버 변수를 반환하는 메소드

```python
ScriptGenerator.transcribe_to_text()
```

음성파일을 텍스트로 변환하는 메소드

## 5. 출처

> whisper : https://github.com/openai/whisper
