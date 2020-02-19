import numpy as np
import color
import material


class CheckerboardMaterial(object):
    def __init__(self, baseColor, ambient, diffuse, specular, specKonst, reflected, otherColor = None):
        self.otherColor = otherColor if otherColor else color.Color(0,0,0)
        self.weiß = material.Material(baseColor, ambient, diffuse, specular, specKonst, reflected)
        self.schwarz = material.Material(self.otherColor, ambient, diffuse, specular, specKonst, reflected)

        self.reflected = reflected
        self.aktuellesMat = self.weiß
        self.checkSize = 1

    def getBaseColor(self, p):
        x = int((p[0] + 100)/ self.checkSize) % 2 == 0
        y = int((p[1] + 100)/ self.checkSize) % 2 == 0
        z = int((p[2] + 100)/ self.checkSize) % 2 == 0

        if (x is not y) is not z:
            self.aktuellesMat = self.weiß
            return self.weiß.getBaseColor(p)
        else:
            self.aktuellesMat = self.schwarz
            return self.schwarz.getBaseColor(p)
    
    def renderColor(self, lightray, normal, lightColor, ray):
        return self.aktuellesMat.renderColor(lightray, normal, lightColor, ray)