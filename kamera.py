import numpy as np 
import ray
from PIL import Image
import color
import threading 
from queue import Queue
import time 
from array import *

class Camera(object):

    def __init__(self, e , c ,up, imageWidth, imageHeight):
        self.fov = np.pi/4
        self.aspratio = imageWidth / imageHeight
        self.alpha = self.fov / 2
        self.e = e 
        self.c = c
        self.up = up

        self.f = (self.c - self.e)/np.linalg.norm(self.c - self.e)
        self.s = np.cross(self.f,self.up)/ np.linalg.norm(np.cross(self.f, self.up))
        self.u = np.cross(self.s, self.f) * -1
        self.height = 2 * np.tan(self.alpha)
        self.width = self.aspratio * self.height
        self.wRes = imageWidth
        self.hRes = imageHeight
        self.pixelWidth = self.width / self.wRes
        self.pixelHeight = self.height / self.hRes



    def calcRay(self, x,y):
        
        


        xcomp = self.s * (x*self.pixelWidth - self.width / 2)
        ycomp = self.u * (y*self.pixelHeight - self.height / 2)
        return ray.Ray(self.e, self.f + xcomp + ycomp)


    def findeAbstand(self, objectlist, rayInst):
        maxdist = float('inf')
        tempObject = None
        for object in objectlist:
            hitdist = object.intersectionParameter(rayInst)
            if hitdist:
                if hitdist < maxdist and hitdist > 0:
                    maxdist = hitdist 
                    tempObject = object
        return maxdist, tempObject


    def render(self, image, objectlist, light, bckgrnd, maxlevel):

        q = Queue()

        starts = [
            [0, self.wRes// 2, 0, self.hRes//2], [self.wRes // 2, self.wRes, 0, self.hRes // 2],
            [0, self.wRes// 2, self.hRes // 2, self.hRes], [self.wRes// 2, self.wRes, self.hRes // 2, self.hRes]
            ]  
        print_lock = threading.Lock()      

        def threader():
            while True:
                worker = q.get()
                renderJob(worker)
                q.task_done()

        def renderJob(worker):
            a = int(threading.current_thread().getName())
            
            for x in range(starts[a][0], starts[a][1]):
                for y in range(starts[a][2], starts[a][3]):
                    
                    #with print_lock:
                        #(print("ThreadName:", threading.current_thread().getName(), x,y))
                    rayInst = self.calcRay(x, y)
                    col = self.traceRay(objectlist, light, rayInst, bckgrnd, maxlevel, 0 )

                    rgbcol = col.toRGB()
                    image.putpixel((x,y), rgbcol )

        

        
        for x in range(4):
            
            t = threading.Thread( target= threader, name ="%s" %(x))
            t.daemon = True 
            t.start()
        start = time.time()

        for worker in range(4):
            q.put(worker)
        
        q.join()
        
        
            
        

        print('entire job took:', time.time()-start)

        
    
    def reachLight(self, lightray, objectlist, lichtentf, tempObject):
        
        maxdist = lichtentf
        for object in objectlist:
            if object != tempObject:
                hitdist = object.intersectionParameter(lightray)
                if hitdist is not None and hitdist > 0 and hitdist < maxdist:
                    
                    return False                    
        return True

    def traceRay(self, objectlist, light, rayInst, bckgrnd, maxlevel, level):

        hitdist, tempObject = self.findeAbstand(objectlist, rayInst)

        if tempObject != None:
        
            return self.shade(level, maxlevel, rayInst, tempObject, objectlist, bckgrnd, light, hitdist)
        else: 
            return bckgrnd
    
    def computeDirectLight(self, schnittpunkt, objectlist, tempObject, normale, rayInst, light):

        col = tempObject.mat.getBaseColor(schnittpunkt)
        
        lichtentf = np.linalg.norm(light.getPos() - schnittpunkt)

        lightray = ray.Ray(schnittpunkt, light.getPos() - schnittpunkt )

        if self.reachLight(lightray, objectlist, lichtentf, tempObject):

            tempCol = tempObject.mat.renderColor(lightray, normale, light.getFarbe(), rayInst)
            
            
            col.r += tempCol.r 
            col.g += tempCol.g 
            col.b += tempCol.b 
            
            return col
        else:
            col.r *= 0.5
            col.g *= 0.5
            col.b *= 0.5
            return col

    def shade (self, level, maxlevel, rayInst, tempObject, objectlist, bckgrnd, light, hitdist):
        schnittpunkt = rayInst.origin + rayInst.direction * hitdist 
        normale = tempObject.normalAt(schnittpunkt)
        
        directColor = self.computeDirectLight(schnittpunkt, objectlist, tempObject, normale, rayInst, light)
        

        if level == maxlevel:
            return directColor

        reflectedRay = ray.Ray(schnittpunkt, rayInst.direction - 2*(np.dot(normale, rayInst.direction) * normale))
        reflectedColor = self.traceRay(objectlist, light, reflectedRay, bckgrnd, maxlevel, level +1)
        

        col = color.Color(0,0,0)
        col.r = directColor.r + (reflectedColor.r * tempObject.mat.reflected)
        col.g = directColor.g + (reflectedColor.g * tempObject.mat.reflected)
        col.b = directColor.b + (reflectedColor.b * tempObject.mat.reflected)

        return col

        

    

    

            




    

