# Simulates the irregular sound reflection in an eliptical theatre from Carl Ferdinand Langhans (1810)

from math import tan, atan, radians, sqrt, degrees
import random

#hpgl stuff for exporting the simulation later

X_MIN = 0
Y_MIN = 0
_11x17 = True
if _11x17:
    X_MAX = 16640
    Y_MAX = 10365
else:
    X_MAX = 10365
    Y_MAX = 7692


class Sound_vector():
    def __init__(self,coord,angle):
        self.bounce = True
        self.on = True
        self.coordinates = [coord]
        self.angle = angle

    def stop_bounce(self):
        self.bounce = False
    def stop(self):
        self.on = False

    def get_cur_coord(self):
        return self.coordinates[-1]

    def add_coord(self, coords):
        self.coordinates.append(coords)

def collision_line_ellipse(v, e_param):
    # current coordinates and current angle and elispse params
    (x0,y0) = v.get_cur_coord()
    cangle = v.angle
    (a,b,h,k) = e_param

    print(x0,y0,cangle, "\n")

    # dir = 1 if vector looks up, -1 otherwise
    dir = -1

    #horizontal line
    if cangle == 0 or cangle == radians(180):
        if cangle == 0: dir = 1
        #horizontal line y = c
        d = y0
        x1 = h + dir * a/b * sqrt(b**2 - d**2 - k**2 + 2*d*k)
        x1_alt = h - dir * a/b * sqrt(b**2 - d**2 - k**2 + 2*d*k)
        if x1 == x0: x1 = x1_alt
        y1 = y0

    #vertical line
    elif cangle == radians(90) or cangle == radians(270):
        if cangle == radians(90): dir = 1
        d = x0
        y1 = k + dir * b/a * sqrt(a**2 - d**2 - h**2 + 2*d*h)
        y1_alt = k - dir * b/a * sqrt(a**2 - d**2 - h**2 + 2*d*h)
        if y1 == y0: y1 = y1_alt
        x1 = x0

    else:
        if cangle > 0 and cangle < radians(180): dir = 1

        # y = mx + c, is linear function
        m = tan(cangle)
        # c as in y = mx + c
        c = y0 - m * x0

        #preparation for big bertha
        phi = c - k
        mu = c + m * h

        # big bertha to find x1, intersection of line/vector and ellipse
        x1 = (b**2*k - a**2*m*phi + dir * a*b*sqrt(b**2 + (a*m)**2 - 2*m*phi*h - phi**2 - (m*h)*2)) / (b**2 + (a*m)**2)
        x1_alt = (b**2*k - a**2*m*phi - dir * a*b*sqrt(b**2 + (a*m)**2 - 2*m*phi*h - phi**2 - (m*h)*2)) / (b**2 + (a*m)**2)
        if x1 == x0: x1 = x1_alt
        y1 = m*x1 + c

    # ellipse's tangent angle at x1,y1
    if y1 == 0:
        theta_tang = radians(90)
    elif x1 ==0:
        theta_tang = radians(0)
    else:
        theta_tang = atan(-b**2*x1/(a**2*y1))

    # new angle of sound vector
    nangle = (2*theta_tang - cangle) % radians(360)

    # updating the Sound_vector v
    v.add_coord((x1,y1))
    v.angle = nangle

    if random.random() > 0.8: v.bounce = False



#ellipse parameters (a,b,h,k)
e_param = (.5,.5,0,0)
vects = [Sound_vector((-sqrt(.5)/2, 0), theta) for theta in range(0,360,45)]



v = vects[2]
while(v.bounce):
    collision_line_ellipse(v,e_param)

#print(v.coordinates)
