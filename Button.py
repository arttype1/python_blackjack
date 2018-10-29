"""

"""
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Button:
    def __init__(self,color1,color2, x1, y1, x2, y2):
        self.color1 = color1
        self.color2 = color2
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        r,g,b = self.color1
        glColor3f(r, g, b)
        glRecti(self.x1, self.y1, self.x2, self.y2)
        r,g,b = self.color2
        glColor3f(r, g, b)
        glRecti(self.x1 + 2, self.y1 + 2, self.x2 - 2, self.y2 - 2)

    def is_inside(self,x, y):
        if (self.x1 < x < self.x2) and (self.y1 < y < self.y2):
            return True
        else:
            return False
    
