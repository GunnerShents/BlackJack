import os
import random
from os import path
from typing import Dict, List, Optional, Tuple

import pygame
from pygame.surface import Surface

import config

# -------------------------------------------------------------------


class Card:
    """
    Creates a card that holds the number and suit.
    """

    def __init__(self, name: str, suit: str) -> None:

        self.value = {
            "Ace": 11,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": 10,
            "Queen": 10,
            "King": 10,
        }
        self.name = name
        self.suit = suit
        self.width = 50
        self.x: Optional[int] = None
        self.y: Optional[int] = None

    # returns the number and suit.
    def __str__(self) -> str:

        return f"{self.name} of {self.suit}"

    # return the total amount in hand using the value dictionary.
    def get_card_value(self) -> int:

        return self.value[self.name]


class CardImages:
    """
    Creates the card graphics for the game. Namely the face up
    and the face down cards. Will render black numbers for black suits
    and red numbers for the red suits.
    """

    def __init__(self) -> None:
        # starting postionof blank card.
        blank_x = 50
        blank_y = 70
        # load images
        blank_card = pygame.image.load(
            path.join(config.IMG_DIR, "BJ_blankCard.png")
        ).convert_alpha()
        self.blank_card_img = pygame.transform.scale(blank_card, (blank_x, blank_y))
        card_back = pygame.image.load(path.join(config.IMG_DIR, "BJ_cardBack.png")).convert_alpha()
        self.card_back_img = pygame.transform.scale(card_back, (blank_x, blank_y))
        self.suits: Dict[str, pygame.surface.Surface] = {}
        self.red_numbers: Dict[str, pygame.surface.Surface] = {}
        self.black_numbers: Dict[str, pygame.surface.Surface] = {}
        self.create_suits_dict()
        self.num_dict("b", self.black_numbers)
        self.num_dict("r", self.red_numbers)

    def create_suits_dict(self) -> None:

        suits_path = path.join(config.IMG_DIR, "BJ_suits")

        for image in os.listdir(suits_path):

            key_entry = path.splitext(image)[0].split("_")[1]
            self.suits[key_entry.capitalize() + "s"] = pygame.image.load(
                path.join(suits_path, image)
            ).convert_alpha()

    def num_dict(self, colour: str, num_dict: Dict[str, Surface]) -> None:

        num_path = path.join(config.IMG_DIR, "BJ_numbers")

        for image in os.listdir(num_path):

            if image[0] == colour:
                key_entry = path.splitext(image)[0].split("_")[1]
                num_dict[key_entry.capitalize()] = pygame.image.load(
                    path.join(num_path, image)
                ).convert_alpha()

    def draw_card_back(self, x: int, y: int, area: Surface) -> None:

        area.blit(self.card_back_img, (x, y))

    def draw_card(self, area: Surface, card: Card) -> None:

        colour_dict: Dict[str, pygame.surface.Surface] = self.red_numbers
        if card.suit == "Spades" or card.suit == "Clubs":
            colour_dict = self.black_numbers
        if card.x is None or card.y is None:
            raise RuntimeError("Aaah")
        # card(x, y) is top right. name and suit need to be positioned
        # x + 15(pixels) & y + 10 for the name and 40 for the suit.
        area.blit(self.blank_card_img, (card.x, card.y))
        area.blit(colour_dict[card.name], (card.x + 15, card.y + 10))
        area.blit(self.suits[card.suit], (card.x + 15, card.y + 40))


class Deck:
    """
    Allows you to create 52 cards forming a deck.
    """

    def __init__(self) -> None:

        self.suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
        self.numbers = [
            "Ace",
            "Two",
            "Three",
            "Four",
            "Five",
            "Six",
            "Seven",
            "Eight",
            "Nine",
            "Ten",
            "Jack",
            "Queen",
            "King",
        ]
        self.deck: List[Card] = []

    # Creates a fresh deck of 52 cards.
    def create_deck(self) -> None:
        for suit in self.suits:
            for num in self.numbers:
                self.deck.append(Card(num, suit))


class Deck_holder:
    """
    Uses the deck class to create one larger cache of cards, with
    function to deal a card, shuffle all cards, check the amount of cards,
    and print all cards.
    """

    def __init__(self) -> None:

        deck = pygame.image.load(path.join(config.IMG_DIR, "BJ_deck.png")).convert_alpha()
        self.holder: List[Card] = []
        self.deck_img = pygame.transform.scale(deck, (55, 75))

    # Takes an integer of how many decks you want held in the holder.
    def create_multi_decks(self, number_of_wanted_decks: int) -> None:
        self.holder = []
        for _ in range(number_of_wanted_decks):
            new_deck = Deck()
            new_deck.create_deck()
            self.holder.extend(new_deck.deck)

    # Checks the number of cards left in the holder and returns the integer value.
    def num_cards(self) -> int:

        return len(self.holder)

    # prints a list of all the cards currently in the holder.
    def show_cards(self) -> None:

        for card in self.holder:
            print(card)

    # Shuffles the cards contained in the holder.
    def shuffle_holder(self) -> None:

        random.shuffle(self.holder)

    # pops the last card from the holder.
    def deal_a_card(self) -> Card:

        return self.holder.pop()

    def draw_deck(self, area: Surface, co_ords: Tuple[int, int]) -> None:

        area.blit(self.deck_img, (co_ords))
