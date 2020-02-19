import numpy as np 
import color 
import licht 
from sphere import Sphere 
from dreieck import Triangle
from ebene import Plane
import kamera 
from PIL import Image
import material
import threading

import schach
import time 

light = licht.Licht(np.array([30,30,10]), color.Color(1,1,1))
bckgrnd = color.Color(0, 0, 0)

rotMat = material.Material(color.Color(0.7,0,0), 0.6, 0.7, 0.2, 40, 0.30)
grunMat = material.Material(color.Color(0,0.7,0), 0.6, 0.7, 0.2, 40, 0.30)
greyMat = material.Material(color.Color(0.3,0.3,0.3), 0.6, 0.7, 0.2, 1, 0)
blauMat = material.Material(color.Color(0,0,0.7), 0.6, 0.7, 0.2, 40, 0.30)
yellowMat = material.Material(color.Color(0.6,0.6,0), 0.6, 0.7, 0.2, 1, 0.11)
brettMat = schach.CheckerboardMaterial(color.Color(0.5,0.5,0.5), 0.3, 0.7, 0.2, 10, 0)



objectlist = [
    Plane(np.array([0, 0, 0,]), np.array([0, 1, 0,]), brettMat),
   
    Sphere(np.array([2.5, 3, -10 ]), 2, rotMat),
    Sphere(np.array([-2.5, 3, -10]), 2, grunMat),
    Sphere(np.array([0, 7, -10]), 2, blauMat),
    Triangle(np.array([2.5, 3, -10]), np.array([-2.5, 3, -10]), np.array([0, 7, -10]), yellowMat)
    
    
]

imageWidth = 200
imageHeight = 200
cam = kamera.Camera(np.array([0, 1.8, 10]), np.array([0, 3, 0]), np.array([0, 1, 0]), imageWidth, imageHeight)
maxlevel = 3

print("starte. Dauert 2 bis 3 Minuten")
image = Image.new("RGB", (imageWidth, imageHeight), color= 0)

cam.render(image, objectlist, light, bckgrnd, maxlevel)



image.show()

