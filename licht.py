import numpy as np 
import color

class Licht(object):
    
    def __init__(self, pos, farbe):
        self.pos = pos
        self.farbe = farbe

    def getPos(self):
        return self.pos

    def getFarbe(self):
        return self.farbe

