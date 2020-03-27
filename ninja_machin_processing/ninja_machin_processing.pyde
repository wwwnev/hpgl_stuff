#ninja strike
from random import randint
def setup():
    size(1000,1000)
    stroke(255)
    noFill()

r = [randint(100,300) for i  in range(8)]
def draw():
    background(0)
    
    beginShape()
    for i in range(4):
        curveVertex(randint(100,900),randint(100,900))
    endShape()
