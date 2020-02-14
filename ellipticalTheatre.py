# Simulates the irregular sound reflection in an eliptical theatre from Carl Ferdinand Langhans (1810)

from math import tan, atan, radians, sqrt

#hpgl stuff

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
        self.coordinates = [(X_MAX*coord[0], Y_MAX*coord[1])]
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
    (a,b) = e_param
    h = X_MAX/2
    k = Y_MAX/2

    ## TODO:
    if cangle == 0 or cangle == radians(180):
        return 0

    elif cangle == radians(90) or cangle == radians(270):
        return 0

    else:
        # dir = 1 if vector looks up, -1 otherwise
        dir = -1
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
        y1 = m*x1 + c

        # ellipse's tangent angle at x1,y1

        theta_tang = atan(-b**2*x/(a**2*y))

        # new angle of sound vector
        nangle = 2*theta_tang - cangle

        # updating the Sound_vector v
        v.add_coord((x1,y1))
        v.angle = nangle



#ellipse parameters (a,b)
e_param = (5000,3000)
vects = [Sound_vector((.5, .5), theta) for theta in range(0,360,20)]



v = vects[1]
