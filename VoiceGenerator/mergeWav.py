import numpy as np
from scipy.io import wavfile

#카이스트 오디오 북 wav 파일을 1분 분량으로 합지기 위한 source code

#파일 개수 입력
audio_file_cnt = 18

wav_files = []
for i in range(1, audio_file_cnt + 1):
    wav_files.append(f'audio/{i}.wav')

outfile = "sounds.wav"

# 첫 번째 WAV 파일 읽기
sample_rate, combined_signal = wavfile.read(wav_files[0])

# 나머지 WAV 파일을 읽어 합치기
for wav_file in wav_files[1:]:
    _, signal = wavfile.read(wav_file)
    combined_signal = np.concatenate((combined_signal, signal))

# 결과를 새로운 WAV 파일로 저장
output_filename = "combined_output.wav"
wavfile.write(output_filename, sample_rate, combined_signal)

print(f"파일이 {output_filename}로 병합되었습니다.")
