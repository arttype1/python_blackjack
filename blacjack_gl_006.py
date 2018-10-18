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
version 004 start of bet mode
version 005 separated out Deck and Card classes
version 006 added card textures
"""
#################################################################################################
#

from Canvas import Canvas
from Deck import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

# globals
s_off = {'Spades': 3, 'Hearts': 2, 'Clubs': 0, 'Diamonds': 1}
r_off = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
         'Nine': 9, 'Ten': 10, 'Jack': 11, 'Queen': 12, 'King':13, 'Ace': 1}

chips_player = 200
chips_dealer = 1000000
cvs = Canvas(1885, 1025, 'BlackJack')
game_mode = 'start'
current_bet = 20
hand_player = []
hand_dealer = []
all_cards_image = Image.open(r"res\all_cards.png")
all_cards = all_cards_image.transpose(Image.FLIP_TOP_BOTTOM)
my_deck = Deck()
my_deck.shuffle()


def draw_message(color, coord, message):
    r,g,b = color
    x,y = coord
    glColor3f(r, g, b)
    glRasterPos2d(x, y)
    for c in message:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))


def draw_card(x, y, card='back'):
    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    if card == 'back':
        card_image = Image.open("res\card_back.jpg")
    else:
        xoff, yoff = r_off[card.rank] - 1, s_off[card.suit]
        card_image = all_cards.crop((xoff * 153 + 7, yoff * 224 + 2,
                                     xoff * 153 + 157, yoff * 224 + 227))
        pass
    img_data = card_image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 150, 225, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2i(x, y)
    glTexCoord2f(0, 1)
    glVertex2i(x, y + 225)
    glTexCoord2f(1, 1)
    glVertex2i(x + 150, y + 225)
    glTexCoord2f(1, 0)
    glVertex2i(x + 150, y)
    glEnd()
    glDisable(GL_TEXTURE_2D)


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


def draw_start():
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
    draw_message((0.6, 0.0, 0.9), (825, 100), 'Click Anywhere to Start')
    pass


def draw_chip_counts():
    global chips_player
    global chips_dealer
    cvs.set_bc(0, 0.69, 0)
    cvs.clear_screen()
    glColor3f(0, 0, 0)
    glRecti(75, 600, 350, 900)
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
    pass


def draw_place_bet():
    global current_bet
    global game_mode
    if game_mode == 'bet':
        draw_message((0, 0, 0), (650, 500), 'Minium bet is 20 chips')
        draw_message((0, 0, 0), (650, 475), 'Place a bet below')
        glRecti(600, 350, 900, 450)
        draw_message((0.0, .6, 0.), (700, 400), 'Your Current bet:')
        draw_message((0.9, 0.6, 0.0), (800, 375), f'{current_bet}')
        glRecti(840, 310, 900, 348)
        glColor3f(1.0, 1.0, 0.0)
        glRecti(842, 312, 898, 346)
        draw_message((0.0, 0.0, 0.0),(845, 323), 'BET')


def draw_cards():
    global hand_player
    global hand_dealer
    glColor3f(1.0, 1.0, 1.0)
    draw_card(600, 500)
    draw_card(775, 500, hand_dealer[0])
    draw_card(600, 200, hand_player[0])
    draw_card(775, 200, hand_player[1])
    # draw_card(950, 200, hand_player[])
    # draw_card(1125, 200, hand_player[])

    pass


def my_mouse(button, state, x, y):
    global game_mode
    if game_mode == 'start':
        game_mode = 'bet'
    elif game_mode == 'bet':
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and (840<x< 900 and 310<y>348):
            game_mode = 'player'
    else:
        pass


def my_display():
    global cvs
    hand_player.append(my_deck.cards.pop())
    hand_player.append(my_deck.cards.pop())
    cvs.set_window(0, 1885, 0, 1025)
    cvs.set_viewport(0, 1885, 0, 1025)
    if game_mode == 'start':
        draw_start()
    else:
        draw_chip_counts()
    if game_mode == 'bet':
        draw_place_bet()
    elif game_mode == 'player':
        hand_player.append(my_deck.cards.pop())
        hand_player.append(my_deck.cards.pop())
        hand_dealer.append(my_deck.cards.pop())
        draw_cards()
        pass
    glFlush()
    cvs.swap()


# register the callback functions
glutDisplayFunc(my_display)
glutMouseFunc(my_mouse)
glutMainLoop()
