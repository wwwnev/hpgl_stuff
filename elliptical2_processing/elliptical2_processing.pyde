from math import tan, atan, radians, sqrt, degrees
import random

TOL = 0.0001

def almost_equal(x,y):
    return abs(x-y) < TOL


class Sound_vector():
    def __init__(self,coord,angle):
        self.bounce = True
        self.on = True
        self.coordinates = [coord]
        self.angle = radians(angle)

    def stop_bounce(self):
        self.bounce = False
    def stop(self):
        self.on = False

    def get_cur_coord(self):
        return self.coordinates[-1]

    def add_coord(self, coords):
        self.coordinates.append(coords)
        
    def draw_it(self):
        c = self.coordinates
        if len(c) == 0: return
        if len(c) == 1: 
            point(c[0]) 
            return
        else: 
            for i in range(1,len(c)):
                line(c[i-1][0], c[i-1][1], c[i][0], c[i][1])


class Ellipse():
    def __init__(self,x,y,a,b):
        self.x = x
        self.y = y
        self.a = 2*a
        self.b = 2*b
    def draw_it(self):
        ellipse(self.x,self.y, self.a, self.b)

el = Ellipse(500,500,400,300)

sv1 = Sound_vector([(200,500),(800,500)], 0)

def setup():
    size(1000, 1000)
    stroke(255)
    noFill()


def draw():
    background(0)
    el.draw_it()
