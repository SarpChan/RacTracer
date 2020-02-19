import numpy as np 

class Color(object):

    def __init__(self, r, g, b):
        self.r = r
        self.g = g 
        self.b = b 

    def toRGB(self):

        red = self.r 
        while red > 1:            
            red = int(red -1 )
        if self.r < 0:
            red = 0
        else:
            red = int(self.r * 255)

        grun = self.g
        while grun > 1:
            grun = int(grun -1 )
        if self.g < 0:
            grun = 0
        else:
            grun = int(self.g * 255)

        blau = self.b
        while blau > 1:
            blau = int(blau- 1)
        if self.b < 0:
            blau = 0
        else:
            blau = int(self.b * 255)

        return tuple([red,grun,blau])

    def getItems(self):
        return [self.r, self.g, self.b]

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

        


        
   