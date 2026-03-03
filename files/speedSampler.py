
import sys
sys.path.insert(0, "./files")

from player import *
from math import modf

class Sampler:
    def __init__(self, speed):
        self.player = Player("media/piano.wav")
        self.speed = speed

        self.bufferIndex = CHUNK
    
    def next(self):

        ret = np.zeros(CHUNK)
        returnIndex = 0

        while returnIndex < CHUNK:

            if self.bufferIndex >= CHUNK - 1:
                self.bufferIndex -= CHUNK
                self.buf = self.player.next()

            frac, integer = modf(self.bufferIndex)
            i = int(integer)

            ret[returnIndex] = self.lerp(self.buf[i], self.buf[i+1], frac)

            returnIndex += 1
            self.bufferIndex += self.speed

        return ret

    def lerp(self, a, b, t):
        return (1 - t) * a + t * b