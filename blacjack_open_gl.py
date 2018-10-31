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
version 007 added buttons
version 008 added dealer logic
version 009 added replay
version 010 a playable game
"""
#################################################################################################
#
from Button import Button
from Canvas import Canvas
from Deck import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

# globals#####################################
screen_width = 1885
screen_height = 1025
cvs = Canvas(screen_width, screen_height, 'BlackJack')
cvs.set_window(0, 1885, 0, 1025)
cvs.set_viewport(0, 1885, 0, 1025)
# offsets for card textures
s_off = {'Spades': 3, 'Hearts': 2, 'Clubs': 0, 'Diamonds': 1}
r_off = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
         'Nine': 9, 'Ten': 10, 'Jack': 11, 'Queen': 12, 'King':13, 'Ace': 1}
# Buttons#####################################
button_place_bet = Button((0.9, 0.6, 0.0), (1, 1, 0), 840, 310, 900, 348)
button_hit = Button((0.0, 0.0, 0.0), (1, 1, 1), 100, 400, 300, 450)
button_stay = Button((0.0, 0.0, 0.0), (1, 1, 1), 100, 300, 300, 350)
button_up_bet = Button((0.0, 0.0, 0.0), (.6, .9, 0), 910, 410, 960, 460)
button_down_bet = Button((0.0, 0.0, 0.0), (.9, .6, 0), 910, 330, 960, 380)
chips_player = 200
chips_dealer = 1000000

game_mode = 'start'
bet = 20
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
    global bet
    global game_mode
    if game_mode == 'bet':
        draw_message((0, 0, 0), (650, 475), 'Minium bet is 20 chips')
        draw_message((0, 0, 0), (650, 450), 'Place a bet below')
        glRecti(600, 350, 900, 425)
        draw_message((0.0, .6, 0.), (700, 400), 'Your Current bet:')
        draw_message((0.9, 0.6, 0.0), (800, 375), f'{bet}')
        button_place_bet.draw()
        draw_message((0, 0, 0),(845, 323), 'BET')
        button_up_bet.draw()
        draw_message((0, 0, 0), (915, 425), '+20  RAISE')
        button_down_bet.draw()
        draw_message((0, 0, 0), (915, 345), '-20  LOWER')


def draw_player():
    button_hit.draw()
    draw_message((0, 0, 0), (180, 415), 'HIT')
    button_stay.draw()
    draw_message((0, 0, 0), (170, 315), 'STAY')


def draw_dealer():
    draw_message((0, 0, 0), (125, 375), f'Dealer has the {hand_dealer[-1]}')
    button_stay.draw()
    draw_message((0, 0, 0), (170, 315), 'Next')


def draw_play_again():
    button_hit.draw()
    draw_message((0, 0, 0), (170, 415), 'QUIT')
    button_stay.draw()
    draw_message((0, 0, 0), (170, 315), 'PLAY')
    # 5 possible outcomes (player busts, dealer busts, dealer wins, player wins, tie)
    if game_mode == 'busted':
        draw_message((0, 0, 0), (150, 470), 'YOU BUST')
    elif game_mode == 'lose':
        draw_message((0, 0, 0), (150, 470), 'YOU LOSE')
    elif game_mode == 'tie':
        draw_message((0, 0, 0), (150, 470), 'It IS A TIE')
    elif game_mode[0] == 'w':
        if game_mode[-1] == '1':
            draw_message((0, 0, 0), (20, 470), 'DEALER BUSTS -')
        draw_message((0, 0, 0), (225, 470), 'YOU WIN')
        pass


def draw_cards():
    global hand_player
    global hand_dealer
    glColor3f(1.0, 1.0, 1.0)
    if len(hand_dealer) < 2:
        draw_card(775, 500)
        if len(hand_dealer) >= 1:
            draw_card(600, 500, hand_dealer[0])
    else:
        for i in range(len(hand_dealer)):
            draw_card((600 + 175 * i), 500, hand_dealer[i])
    for i in range(len(hand_player)):
        draw_card((600 + 175 * i), 200, hand_player[i])
    glColor3f(0, 0, 0)
    glRecti(75, 500, 350, 700)
    draw_message((0.0, .6, 0.), (100, 700), 'Your Current bet:')
    draw_message((0.9, 0.6, 0.0), (100, 675), f'{bet}')
    draw_message((0.6, .0, 0.9), (100, 600), 'Dealer is showing:')
    draw_message((0.9, 0.6, 0.0), (100, 575), f'{find_total(hand_dealer)}')
    draw_message((0.0, .6, 0.), (100, 550), 'Your Current total:')
    draw_message((0.9, 0.6, 0.0), (100, 525), f'{find_total(hand_player)}')


def my_mouse(button, state, x, neg_y):
    y  = screen_height - neg_y
    global game_mode
    global chips_dealer, chips_player
    global hand_dealer, hand_player
    global my_deck
    global bet
    if game_mode == 'start':
        game_mode = 'bet'
    elif game_mode == 'bet':
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_place_bet.is_inside(x, y):
            game_mode = 'player'
            hand_player.append(my_deck.cards.pop())
            hand_player.append(my_deck.cards.pop())
            if find_total(hand_player) == 21:
                game_mode = 'win0'
            hand_dealer.append(my_deck.cards.pop())
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_up_bet.is_inside(x, y):
            bet += 20
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_down_bet.is_inside(x, y):
            bet -= 20
        bet = max(bet, 20)
        bet = min(bet, chips_player, chips_dealer)

    elif game_mode == 'player':
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_hit.is_inside(x, y):
            hand_player.append(my_deck.cards.pop())
            if find_total(hand_player) >= 22:
                chips_player -= bet
                chips_dealer += bet
                # print('player busts!')
                game_mode = 'busted'
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_stay.is_inside(x, y):
            game_mode = 'dealer'
    elif game_mode == 'dealer':
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_stay.is_inside(x, y):
            total = find_total(hand_dealer)
            if total < 17:
                hand_dealer.append(my_deck.cards.pop())
            else:
                if total > 21:
                    # print('Dealer busts!')
                    game_mode = 'win1'
                    chips_player += bet
                    chips_dealer -= bet
                elif total > find_total(hand_player):
                    # print(f'Dealer wins with {total}')
                    game_mode ='lose'
                    chips_player -= bet
                    chips_dealer += bet
                elif find_total(hand_player) == total:
                    # print('it is a tie')
                    game_mode = 'tie'
                else:
                    # print(f'Dealer loses with {total}')
                    game_mode = 'win0'
                    chips_player += bet
                    chips_dealer -= bet
    else:  # play again section#
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_hit.is_inside(x, y):
            quit()
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_stay.is_inside(x, y):
            # reset hands and deck
            hand_player = []
            hand_dealer = []
            if len(my_deck.cards) <= 10:
                my_deck = Deck()
                my_deck.shuffle()
            game_mode = 'bet'



def my_display():
    global cvs
    global game_mode
    if game_mode == 'start':
        draw_start()
    else:
        draw_chip_counts()
        draw_cards()
        if game_mode == 'bet':
            draw_place_bet()
        elif game_mode == 'player':
            draw_player()
        elif game_mode == 'dealer':
            draw_dealer()
        else:
            draw_play_again()
    glFlush()
    cvs.swap()


# register the callback functions
glutDisplayFunc(my_display)
glutMouseFunc(my_mouse)
glutMainLoop()
