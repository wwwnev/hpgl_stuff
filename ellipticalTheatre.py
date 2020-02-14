# Simulates the irregular sound reflection in an eliptical theatre from Carl Ferdinand Langhans (1810)

from math import tan, radians

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

# Sequence of linear functions (y = ax + b)
class Sound_line():
    def __init__(self,coord,angle):
        self.bounce = True
        self.coordinates = [(X_MAX*coord[0], Y_MAX*coord[1])]
        # slope = tan()
        self.a = tan(angle)
        # b = y - ax
        self.b = self.coordinates[0][1] - self.a * self.coordinates[0][0]

    def stop_bounce(self):
        self.bounce = False

    def get_cur_coord(self):
        return self.coordinates[-1]

#p1 = Sound_line((.5, .5), radians(45))
#print(p1.coordinates, p1.a, p1.b)

vects = []
