import sys
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


class Canvas:
    """
    cp 'current position' is a list [x,y]
    cd 'current direction' if a float representing an angle
    viewport and window are lists (left, right, bottom, top)
    color is used for drawing (red, green, blue)
    """
    def __init__(self, width, height, window_title: str):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(window_title.encode('ascii'))
        self.window = [0, width, 0,  height]
        self.viewport = [0, width, 0,  height]
        self.center = (0, 0)
        self.max_xy = (width, height)
        self.zoom = 1.0
        self.color = [0, 0, 0]
        self.cp = [0, 0]
        self.cd = 0.0
        self.set_window(0, width, 0, height)
        self.set_viewport(0, width, 0, height)

    @property
    def window_aspect(self):  # width / height
        return (self.window[1] - self.window[0]) / (self.window[3] - self.window[2])

    @staticmethod
    def swap():
        glutSwapBuffers()

    @staticmethod
    def clear_screen():
        glClear(GL_COLOR_BUFFER_BIT)

    @staticmethod
    def set_bc(r, g, b):
        glClearColor(r, g, b, 0.0)

    @staticmethod
    def thick(t):
        glLineWidth(t)

    def zoom_in(self):
        self.zoom = max(self.zoom / 2, 1/16)
        b = 10 * self.zoom
        c = self.center
        x = int((self.zoom * self.max_xy[0] / 2))
        y = int((self.zoom * self.max_xy[1] / 2))
        self.set_window(c[0] - b, c[0] + b, c[0] - b, c[0] + b)

    def zoom_out(self):
        self.zoom = min(self.zoom * 2, 4)
        b = 10 * self.zoom
        c = self.center
        x = int((self.zoom * self.max_xy[0] / 2))
        y = int((self.zoom * self.max_xy[1] / 2))
        self.set_window(c[0] - b, c[0] + b, c[0] - b, c[0] + b)

    def set_color(self, r, g, b):
        self.color = [r, g, b]
        glColor3f(r, g, b)

    def set_window(self, l, r, b, t):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(l, r, b, t)
        self.window = [l, r, b, t]

    def set_viewport(self, left, right, bottom, top):
        glViewport(left, bottom, right - left, top - bottom)
        self.viewport = [left, right, bottom, top]

    def line_to(self, x, y):
        glBegin(GL_LINES)
        glVertex2f(self.cp[0], self.cp[1])
        glVertex2f(x, y)
        glEnd()
        glFlush()
        self.cp = [x, y]

    def line_rel(self, dx, dy):
        self.line_to(self.cp[0] + dx, self.cp[1] + dy)

    def turn(self, ang):
        self.cd += ang

    def forward(self, dist, is_visible: bool = True):
        rad_per_deg = 0.017453393
        x = self.cp[0] + (dist * math.cos(rad_per_deg * self.cd))
        y = self.cp[1] + (dist * math.sin(rad_per_deg * self.cd))
        if is_visible:
            self.line_to(x, y)
        else:
            self.cp = [x, y]
