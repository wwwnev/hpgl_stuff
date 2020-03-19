from math import cos, sin, tan, atan, radians, sqrt, degrees
import random

TOL = 0.00001

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
    def is_inside(self,x1,y1):
        return (float(x1)-self.x)**2/self.a**2 + (float(y1)-self.y)**2/self.b**2 < 0.78
        
def collision_line_ellipse(v, e):
    if not(v.bounce) : return
    # current coordinates and current angle and elispse params
    (x0,y0) = v.get_cur_coord()
    cangle = v.angle
    (h,k,a,b) = e.get_params()

    # dir = 1 if vector looks up, -1 otherwise (or something like that)
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
        if cangle > radians(270) or cangle < radians(90): dir = 1

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
            print("ALMOST EQUAL HAPPENED !!")
            x1 = x1_alt
        y1 = m*x1 + c

    # ellipse's tangent angle at x1,y1
    if y1 == 500:
        theta_tang = radians(90)
    elif x1 == 500:
        theta_tang = radians(0)
    else:
        # angle from center of ellipse to point on ellipse
        el_angle = atan((y1-500)/(x1-500))
        # angle of the tangent at said point of ellipse
        theta_tang = atan(-b*cos(el_angle)/a/sin(el_angle)) % radians(180)
        
    # new angle of sound vector
    nangle = (2*theta_tang - cangle) % radians(360)

    # updating the Sound_vector v
    v.add_coord((x1,y1))
    v.angle = nangle

# TODO adjust ymin and ymax in case the wall isnt directly in the middle of the ellipse
def collision_line_vline(v, x1, el):
    if not(v.bounce) or v.get_cur_coord()[0] <= 500 or degrees(v.angle) < 90 or degrees(v.angle) > 270 : return
    
    (x0,y0) = v.get_cur_coord()
    cangle = v.angle
    ymin = el.y - el.b
    ymax = el.y + el.b
    
    #projected y value when hitting wall
    y1 = tan(cangle) * (x1-x0) + y0
    
    # hits the absorbtion wall INSIDE the ellipse
    if ymin <= y1 <= ymax:
        v.add_coord((x1,y1))
        v.stop_bounce()
    else: return
        
    
# the theatre boundaries
el = Ellipse(500,500,400,300)

# sound vectors
vects = [Sound_vector((240,500), theta) for theta in range(0,360,15)]

# vertical line defined by its x value, it's the wall that absorbs sound
v_line = 500

def setup():
    size(1000, 1000)
    stroke(255)
    noFill()
    
def draw():
    #global t
    #t+=1
    #if t >= 6: noLoop()
    background(0)
    stroke(255,255,255,100)
    el.draw_it()
    stroke(255,255,255,120)
    for v in vects:
        #collision_line_vline(v,v_line,el)
        #collision_line_ellipse(v,el)
        v.draw_it()
    saveFrame("ellipticalTheatre-#####.png")
    
def mouseMoved():
    global vects
    if el.is_inside(mouseX,mouseY):
        print("TWASDO",mouseX,mouseY)
        vects = [Sound_vector((mouseX,mouseY), theta) for theta in range(0,360,15)]
        for v in vects:
            #it should never take more than stpr bounce to stop, if we get there, theres and infinite loop (TODO)
            stpr = 0
            while v.bounce and stpr < 10:
                stpr += 1
                collision_line_vline(v,v_line,el)
                collision_line_ellipse(v,el)
