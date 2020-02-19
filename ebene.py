import numpy as np 

class Plane(object):
    def __init__(self, point, normal, mat):
        self.point = point
        self.normal = np.divide(normal, np.linalg.norm(normal))
        self.mat = mat

    def __repr__(self):
        return 'Plane(%s,%s)' %(repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point 
        a = np.dot (op, self.normal)
        b = np.dot(ray.direction, self.normal)
        if b:
            if (-a/b > 0):
                return -a/b
        else: 
            return None
    
    def normalAt(self, p):
        return self.normal

    