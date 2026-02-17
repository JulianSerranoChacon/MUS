# Julian Serrano Chacon
# Mika Rodriguez Castro

import numpy as np   
import osc
import scipy.signal as sg
import matplotlib.pyplot as plt
from consts import *

class OscFM:
    def __init__(self, beta = osc.Osc(), fc=110.0,amp=1.0,fm=6.0, fmshape='sin', fcshape='sin'):
        self.fc = fc
        self.amp = amp
        self.fm = fm
        self.beta = beta
        self.frame = 0
        self.fcShape = fcshape
        self.fmShape = fmshape

        # moduladora = βsin(2πfm)
        self.mod = osc.Osc(freq=fm, shape=fmshape)

    def next(self):  
        # sin(2πfc+mod)  
        # sacamos el siguiente chunk de la moduladora
        mod = self.mod.next()

        # soporte para el chunk de salida
        sample = np.arange(self.frame,self.frame+CHUNK)        
        # aplicamos formula
        sig = np.sin(2*np.pi*self.fc*sample/SRATE + mod)
        if self.fcShape == 'square':
            sig = sg.square(sig)
        elif self.fcShape == 'sawtooth':
            sig = sg.sawtooth(sig)
        elif self.fcShape == 'triangle':
            sig = sg.sawtooth(sig, 0.5)

        out =  self.amp*self.beta.next()*sig

        self.frame += CHUNK
        return out 

    def setFm(self,fm):
        self.fm = fm
        self.mod.freq = fm

    def getFm(self):
        return self.fm
    
    def setFcShape(self, shape):
        self.fcShape = shape

    def setFmShape(self, shape):
        self.fmShape = shape
        self.mod.setShape(shape)


