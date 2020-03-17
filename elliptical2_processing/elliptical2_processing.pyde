from math import tan, atan, radians, sqrt, degrees
import random

TOL = 0.0001

def almost_equal(x,y):
    return abs(x-y) < TOL


class Sound_vector():
    def __init__(self,coord,angle):
        self.bounce = True
        self.coordinates = [coord]
        self.angle = radians(angle)

    def stop_bounce(self):
        self.bounce = False

    def get_cur_coord(self):
        return self.coordinates[-1]

    def add_coord(self, coords):
        self.coordinates.append(coords)
        
    def draw_it(self):
        c = self.coordinates
        #print(c)
        if len(c) == 0: return
        if len(c) == 1: 
            point(c[0][0],c[0][1]) 
            return
        else: 
            for i in range(1,len(c)):
                line(c[i-1][0], c[i-1][1], c[i][0], c[i][1])


class Ellipse():
    def __init__(self,x,y,a,b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
    def get_params(self):
        return (self.x,self.y,self.a,self.b)
    def draw_it(self):
        ellipse(self.x,self.y, 2*self.a, 2*self.b)
        
def collision_line_ellipse(v, e):
    if not(v.bounce) : return
    # current coordinates and current angle and elispse params
    (x0,y0) = v.get_cur_coord()
    cangle = v.angle
    (h,k,a,b) = e.get_params()
    #print(h,k,a,b)
    #print(x0,y0,degrees(cangle), "\n")

    # dir = 1 if vector looks up, -1 otherwise
    dir = -1

    #horizontal line
    if cangle == 0 or cangle == radians(180):
        if cangle == 0: dir = 1
        #horizontal line y = c
        d = y0

        x1 = h + dir * float(a)/b * sqrt(b**2 - d**2 - k**2 + 2*d*k)
        x1_alt = h - dir * float(a)/b * sqrt(b**2 - d**2 - k**2 + 2*d*k)
        if almost_equal(x0,x1): x1 = x1_alt
        y1 = y0

    #vertical line
    elif cangle == radians(90) or cangle == radians(270):
        if cangle == radians(90): dir = 1
        d = x0
        y1 = k + dir * float(b)/a * sqrt(a**2 - d**2 - h**2 + 2*d*h)
        y1_alt = k - dir * float(b)/a * sqrt(a**2 - d**2 - h**2 + 2*d*h)
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
        x1 = (b**2*h - a**2*m*phi + dir * a*b*sqrt(b**2 + (a*m)**2 - 2*m*phi*h - phi**2 - (m*h)**2)) / (b**2 + (a*m)**2)
        x1_alt = (b**2*h - a**2*m*phi - dir * a*b*sqrt(b**2 + (a*m)**2 - 2*m*phi*h - phi**2 - (m*h)**2)) / (b**2 + (a*m)**2)
        if almost_equal(x0,x1): 
            #print("ALMOST EQUAL HAPPENED !!")
            x1 = x1_alt
        y1 = m*x1 + c

    # ellipse's tangent angle at x1,y1
    if y1 == 0:
        theta_tang = radians(90)
    elif x1 == 0:
        theta_tang = radians(0)
    else:
        theta_tang = atan(-b**2*x1/(a**2*y1))

    # new angle of sound vector
    #print (degrees(2*theta_tang - cangle))
    #print (degrees((2*theta_tang - cangle) % radians(360)))
    nangle = (2*theta_tang - cangle) % radians(360)

    # updating the Sound_vector v
    v.add_coord((x1,y1))
    v.angle = nangle

    #if random.random() > 0.9: v.bounce = False

def collision_line_vline(v, x1, el):
    print(not(v.bounce), v.get_cur_coord()[0], degrees(v.angle))
    
    if not(v.bounce) or v.get_cur_coord()[0] <= 500 or degrees(v.angle) < 90 or degrees(v.angle) > 270 : return
    
    
    (x0,y0) = v.get_cur_coord()
    cangle = v.angle
    ymin = el.y - el.b
    ymax = el.y + el.b
    
    y1 = tan(cangle) * (x1-x0) + y0
    
    if ymin <= y1 <= ymax:
        print("mid stop ", x1, y1) 
        v.add_coord((x1,y1))
        v.stop_bounce()
    else: return
        
    

el = Ellipse(500,500,400,300)

#sv1 = Sound_vector((200,400), 0)

#vects = [Sound_vector((264.5751311,500), theta) for theta in range(0,360,15)]

vects = [Sound_vector((264.5751311,500), theta) for theta in [8]]

#print(sv1.coordinates)

#vertical line defined by its x value
v_line = 500



def setup():
    size(1000, 1000)
    stroke(255)
    noFill()
    

def draw():
    line(0,0,1000,1000)
    if frameCount >= 3: noLoop()
    background(0)
    el.draw_it()
    for v in vects:
        collision_line_vline(v,v_line,el)
        collision_line_ellipse(v,el)
        v.draw_it()
    line(v_line,800,v_line,200)
