"""
#############################################################################################
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
"""
from random import randint as rdi, shuffle
suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
ranks = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
         'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King':10, 'Ace': 11}
chips_player = 200
chips_dealer = 1000000

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


def main():
    play_again = True
    my_Deck = Deck()
    my_Deck.shuffle()
    while play_again:
        hand_player = []
        hand_dealer = []
        global chips_player
        global chips_dealer
        need_bet = True
        while need_bet:
            bet = str(input(f'You have {chips_player} chips, How much is your bet?: '))
            try:
                if int(bet):
                    bet = int(bet)
            except:
                print('I do not understand, please enter a positive integer!')
                bet = 0
            if bet > chips_player:
                print('Sorry,You lack the chips!')
            elif bet <= 0:
                print('Oh, a wise guy huh?')
            else:
                need_bet = False
        turn = 'player'
        while turn == 'player':
            if len(hand_player) <= 1:
                hand_player.append(my_Deck.cards.pop())
                hand_player.append(my_Deck.cards.pop())
            need_input = True
            while need_input:
                print('your hsnd:')
                for item in hand_player:
                    print(item)
                total = find_total(hand_player)
                action = str(input(f'Your total is {total}, (H)it or (S)tay: '))
                if action.upper() == 'H':
                    hand_player.append(my_Deck.cards.pop())
                    print (f'you got {hand_player[-1]}')
                elif action.upper() == 'S':
                    need_input = False
                if find_total(hand_player) >= 22:
                    print('You busted!, you lost {str(bet)} chips')
                    chips_player -= bet
                    need_input = False
            turn = 'dealer'
            total_player = find_total(hand_player)
            if total_player > 21:
                break
            else:
                print('Dealers Turn.')
                total = find_total(hand_dealer)
                while total < min(17, total_player):
                    hand_dealer.append(my_Deck.cards.pop())
                    total = find_total(hand_dealer)
                    print (f'Dealer gets {hand_dealer[-1]}')
                if total > 21:
                    print('Dealer busts!')
                    chips_player += bet
                    chips_dealer -= bet
                elif total > find_total(hand_player):
                    print(f'Dealer wins with {total}')
                    chips_player -= bet
                    chips_dealer += bet
                elif total_player == total:
                    print('it is a tie')
                else:
                    print(f'Dealer loses with {total}')
                    chips_player += bet
                    chips_dealer -= bet

        print(f'You have {chips_player} chips,')
        play_again = str(input('Play Again?(Y)es or any other key to quit: '))
        if not play_again.upper() == 'Y':
            play_again = False
            print('Thanks for playing')
        elif chips_player <= 0:
            play_again = False
            print('Your broke, go home.')
        elif chips_dealer <=200:
            play_again = False
            print('You took too much of our money already!!!')



main()
