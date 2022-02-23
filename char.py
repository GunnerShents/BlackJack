import random, pygame
from cardClasses import Card, Deck, Deck_holder
import config
import os


class Character:
    """A character that does stuff"""

    def __init__(self):
        self.hand = []
        self.name = ""
        self.total = 0
        self.bust = False

    # Prints the cards you have in your hand
    def show_cards(self):

        print(f"{self.name} is holding: ")
        for card in self.hand:
            print(card)

    # Returns the characters name, name is defined on construction.
    def get_name(self):

        return self.name

    # Check to see if the player is bust, if not one card is added to the hand
    def hit(self, deck, x=0, y=0):

        # takes a new card
        new_card: Card = deck.deal_a_card()
        new_card.x = x
        new_card.y = y
        # adds the new card to the player hand
        self.hand.append(new_card)
        self.check_hand()
        if self.check_bust():
            self.print_bust()
            self.bust = True

    # Check hand for bust and check if it holds aces
    def check_hand(self):
        self.total = 0
        aces = 0
        # loop through cards in hand, tally aces.
        # value of ace is defaulted to 11!
        for card in self.hand:
            if card.number == "Ace":
                aces += 1
                self.total += card.get_card_value()
            else:
                self.total += card.get_card_value()
        # checks if hand total can be reduced by 10 for each ace in hand.
        if self.check_bust() == True and aces > 0:
            while aces > 0 and self.total > 21:
                self.total -= 10
                aces -= 1
        return self.total

    # returns true if the player is over 21.
    def check_bust(self):

        return self.total > 21

    def print_bust(self):

        print("You are bust!!")

    def get_total(self):

        return self.total

    def check_bj(self):

        return len(self.hand) == 2 and self.total == 21

    def reset(self):
        self.hand = []
        self.bust = False
        self.total = 0


class Player(Character):
    def __init__(self, name):

        # Load coin image and transform the size.
        self.hand = []
        self.name = name
        self.balance = 500
        self.bet = 0
        self.bet_made = False
        self.total = 0
        self.bust = False
        self.card_one_x_pos = 236
        self.card_one_y_pos = 496
        self.card_two_x_pos = 317
        self.card_two_y_pos = 496

    def get_balance(self):
        return self.balance

    # checks bet is valid, sets self.bet and deducts bet from balance.
    def set_bet(self, amount):
        if not self.bet_made:
            self.bet = amount
            self.bet_made = True

    def get_bet(self):
        return self.bet

    def black_jack(self):

        self.balance += self.bet * 3

    def lost(self):

        self.balance -= self.bet
        print(f"You lost, your balance is {self.balance}")

    def calc_win(self):
        if self.check_blackjack():
            self.black_jack()
            print("Black Jack!!")
        else:
            self.balance += self.bet
        print(f"You win, your balance is {self.balance}")

    def draw(self):

        print(f"It's a draw, your balance is {self.balance}")

    def check_blackjack(self):

        return self.total == 21 and len(self.hand) == 2

    def reset_bet(self):
        self.bet = 0
        self.bet_made = False


class Dealer(Character):
    def __init__(self):

        self.hand = []
        self.name = "Dealer"
        self.total = 0
        self.bust = False
        self.card_one_x_pos = 235
        self.card_one_y_pos = 137
        self.card_two_x_pos = 316
        self.card_two_y_pos = 137
        self.not_dealers_turn = True

    def check_for_stand(self):
        total = self.get_total()
        if 17 <= total <= 21:
            return True
