
import color 
import numpy as np 


class Material(object):
    def __init__(self, baseColor, ambient, diffuse, specular, specKonst, reflected, otherColor = None):
        self.baseColor = baseColor
        self.ambient = ambient
        self.diffuse = diffuse
        self.specKonst = specKonst
        self.specular = specular * ((self.specKonst + 2 ) / (np.pi * 2))
        self.reflected = reflected
    
    

    def getBaseColor(self, point):
        temp = self.baseColor.getItems()
        for ele in temp:
            ele *= self.ambient
            
        
        return color.Color(temp[0],temp[1], temp[2])


    def getDiffuse(self, lightray, normal):
        return np.dot(lightray.direction, normal)

    def getSpecular(self, lightray, normal, ray):
        lr = (lightray.direction - 2* np.dot(normal, lightray.direction) * normal)
        return np.dot(lr, np.negative(ray.direction))


    def renderColor(self, lightray, normal, lightColor, ray):
        col = color.Color(0,0,0)
        
        diffuseFactor = self.getDiffuse(lightray, normal)
        if diffuseFactor > 0:
            colTemp = col.getItems()
            lightTemp = lightColor.getItems()
            baseTemp = self.baseColor.getItems()

            for num in range(3):
                colTemp[num] += baseTemp[num] * diffuseFactor * self.diffuse * lightTemp[num]

            
            specFactor = self.getSpecular(lightray, normal, ray) 
            if specFactor > 0:
                for num in range(3):
                    colTemp[num] += lightTemp[num] *self.specular * (specFactor **self.specKonst)
            col.r = colTemp[0]
            col.g = colTemp[1]
            col.b = colTemp[2]      
            return col
        return col
            