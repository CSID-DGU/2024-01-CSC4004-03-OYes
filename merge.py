import numpy as np
from scipy.io import wavfile

#카이스트 오디오 북  wav 파일을 1분 분량으로 합지기 위한 source code
wav_files = ["audio/1.wav", 
           "audio/2.wav",
           "audio/3.wav",
           "audio/4.wav",
           "audio/5.wav", 
           "audio/6.wav",
           "audio/7.wav", 
           "audio/8.wav",
           "audio/9.wav", 
           "audio/10.wav",
           "audio/11.wav", 
           "audio/12.wav",
           "audio/13.wav",
           "audio/14.wav",
           "audio/15.wav", 
           "audio/16.wav",
           "audio/17.wav",
           "audio/18.wav",
           ]
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