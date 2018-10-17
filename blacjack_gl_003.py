"""
this project is from an online course available on udemy.com
called "Complete-Python3 Bootcamp"
Milestone Project 2 - Blackjack Game¶
In this milestone project you will be creating a Complete BlackJack Card Game in Python.

Here are the requirements:

You need to create a simple text-based BlackJack game
The game needs to have one player versus an automated dealer.
The player can stand or hit.
The player must be able to pick their betting amount.
You need to keep track of the player's total money.
You need to alert the player of wins, losses, or busts, etc...
#############################################################################################
all code is by George A. Merrill except where otherwise noted
version 001 text based version
version 002 start of OpenGl version
version 003 start of GUI
"""
#################################################################################################
#

from Canvas import Canvas
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
from random import shuffle

suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
ranks = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
         'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King':10, 'Ace': 11}
chips_player = 200
chips_dealer = 1000000
cvs = Canvas(1885, 1025, 'BlackJack')
game_mode = 'start'
current_bet = 0

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    def __init__(self):
        self.cards = []
        for s in suits:
            for r in ranks:
                self.cards.append(Card(s,r))

    def shuffle(self):
        shuffle(self.cards)


def find_total(hand):
    total = 0
    aces = 0
    for r in hand:
        if r.rank == 'Ace':
            aces += 1
        total += ranks[r.rank]
    while total > 21 and aces >= 1:
        total -= 10
        aces -= 1

    return total


def place_bet():
    global current_bet
    global game_mode
    if game_mode == 'bet':
        glColor3f(0, 0, 0)
        glRasterPos2d(650, 500)
        for c in 'Minium bet is 20 chips':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        glRecti(600, 350, 900, 450)
        glRasterPos2d(650, 475)
        for c in 'Place a bet below':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        glRecti(600, 350, 900, 450)
        glColor3f(0.0, .6, 0.)
        glRasterPos2d(700, 400)
        for c in 'Your Current bet:':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        glColor3f(0.9, 0.6, 0.0)
        glRasterPos2d(800, 375)
        for c in f'{current_bet}':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
    pass


def my_mouse(button, state, x, y):
    global game_mode
    if game_mode == 'start':
        game_mode = 'bet'

def my_display():
    global cvs
    cvs.set_window(0, 1885, 0, 1025)
    cvs.set_viewport(0, 1885, 0, 1025)
    if game_mode == 'start':
        cvs.set_bc(0, 0, 0)
        cvs.clear_screen()
        glColor3f(1, 1, 1)
        cvs.thick(8)
        glEnable(GL_TEXTURE_2D)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image = Image.open("res\Splash.png")
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = flipped_image.convert("RGBA").tobytes()
        # .crop((0, 0, 256, 244))
        # img_data = raw_data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 500, 300, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2i(425, 200)
        glTexCoord2f(0, 1)
        glVertex2i(425, 800)
        glTexCoord2f(1, 1)
        glVertex2i(1425, 800)
        glTexCoord2f(1, 0)
        glVertex2i(1425, 200)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.6, 0.0, 0.9)
        glRasterPos2d(825, 100)
        for c in 'Click Anywhere to Start':
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
    elif game_mode == 'bet':
        cvs.set_bc(0, 1, 0)
        cvs.clear_screen()
        glColor3f(0, 0, 0)
        glRecti(75,600, 350, 900)
        my_deck = Deck()
        my_deck.shuffle()
        hand_player = []
        hand_dealer = []
        global chips_player
        global chips_dealer
        glColor3f(0.6, 0.0, 0.9)
        glRasterPos2d(100, 850)
        for c in 'Dealers Chips:':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        glColor3f(0.0, .6, 0.)
        glRasterPos2d(100, 750)
        for c in 'Your Chips:':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        glColor3f(0.9, 0.6, 0.0)
        glRasterPos2d(100, 825)
        for c in f'{chips_dealer}':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        glColor3f(0.9, 0.6, 0.0)
        glRasterPos2d(100, 725)
        for c in f'{chips_player}':
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
        # place bet
        place_bet()

    else:
        pass
    glFlush()
    cvs.swap()


# register the callback functions
glutDisplayFunc(my_display)
glutMouseFunc(my_mouse)
glutMainLoop()
