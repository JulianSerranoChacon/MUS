
import sys
sys.path.insert(0, "./files")        

from consts import *
import numpy as np
import soundfile as sf
import librosa

class Player:
    def __init__(self, file):
        # leemos archivo de audio, data y srate del archivo
        data, srate = sf.read(file,dtype=np.float32)       
        # resampleamos data a SRATE
        self.data = librosa.resample(data, orig_sr=srate, target_sr=SRATE)     
        self.finished = False
        self.frame = 0

    def next(self):
        if self.frame+CHUNK>len(self.data): # si no queda suficiente data, rellenamos con ceros
            self.finished = True
            return np.pad(self.data[self.frame:],(0,CHUNK-len(self.data[self.frame:])),mode='constant')
        else:
            ret = self.data[self.frame:self.frame+CHUNK]
            self.frame += CHUNK
            return ret

    def isFinished(self):
        return self.finished

    def sRate(self):
        return self.SRATE
