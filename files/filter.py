
import sys
sys.path.insert(0, "./files")  

from consts import *

class Filter:
    def __init__(self,signal):
        self.signal = signal
        # memoria con la última muestra del bloque anterior, para el cálculo de la primera muestra del bloque actual
        # inicialmente silencio
        self.mem = 0
        # por defecto inactivo
        self.act = False

    def next(self):
        data = self.signal.next()

        if self.act:
            data[1:]=0.5*(data[0:-1]+data[1:]) # media entre cada muestra y la siguiente
            data[0] = 0.5*(self.mem+data[0]) # la primera muestra se calcula por separado, utilizando la última del bloque anterior

        self.mem = data[-1] # actualizamos memo con ultima muestra
        return data

    def activate(self):
        self.act = True

    def deactivate(self):
        self.act = False    

    def isActive(self):
        return self.act

