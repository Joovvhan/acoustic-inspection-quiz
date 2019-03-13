import os
from params import params
from glob import glob
from scipy.io import wavfile
import librosa
import numpy as np

wav_file_list = glob(os.path.join(params.data_dir, '*.wav')) 

print(wav_file_list)

for wav_file in wav_file_list:
	# wavfile.read(wav_file)
	y = librosa.core.load(wav_file, duration=3)