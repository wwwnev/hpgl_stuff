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

def collision_line_ellipse(v, e_param):
    # current coordinates and current angle and elispse params
    (x0,y0) = v.get_cur_coord()
    cangle = v.angle
    (a,b,h,k) = e_param

    print(x0,y0,degrees(cangle), "\n")

    # dir = 1 if vector looks up, -1 otherwise
    dir = -1

    #horizontal line
    if cangle == 0 or cangle == radians(180):
        if cangle == 0: dir = 1
        #horizontal line y = c
        d = y0
        x1 = h + dir * a/b * sqrt(b**2 - d**2 - k**2 + 2*d*k)
        x1_alt = h - dir * a/b * sqrt(b**2 - d**2 - k**2 + 2*d*k)
        if almost_equal(x0,x1): x1 = x1_alt
        y1 = y0

    #vertical line
    elif cangle == radians(90) or cangle == radians(270):
        if cangle == radians(90): dir = 1
        d = x0
        y1 = k + dir * b/a * sqrt(a**2 - d**2 - h**2 + 2*d*h)
        y1_alt = k - dir * b/a * sqrt(a**2 - d**2 - h**2 + 2*d*h)
        if almost_equal(y0,y1): y1 = y1_alt
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
        if almost_equal(x0,x1): x1 = x1_alt
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

    if random.random() > 0.9: v.bounce = False



#ellipse parameters (a,b,h,k)
e_param = (sqrt(2),sqrt(2),0,0)
vects = [Sound_vector((-1, 0), theta) for theta in range(0,360,45)]



v = vects[2]
while(v.bounce):
    collision_line_ellipse(v,e_param)

print(v.coordinates)

def setup():
    size(1000, 1000)
    stroke(255)
    noFill()


def draw():
    background(0)
    old = 0
    new = 1
    
    scaled_v = list(map(lambda x: ((x[0]+1)*50,(x[1]+1)*50), v.coordinates))
    print(v.coordinates)
    print(scaled_v)
    l = len(v.coordinates)
    while new < l:
        line(scaled_v[old][0],scaled_v[old][1],scaled_v[new][0],scaled_v[new][1])
        new+=1
        old+=1
    
    line(0,500,1000,500)
        
        
