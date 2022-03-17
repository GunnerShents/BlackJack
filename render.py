import pygame
from cardclasses import Deck_holder, Card, CardImages
from char import Player, Dealer, Character


class Text:
    def __init__(self):

        self.font_name = pygame.font.match_font("californianfb")
        self.balance_pos = {1: (40, 430), 2: (655, 535), 3: (1050, 430)}

    def drawText(
        self,
        surf: pygame.surface.Surface,
        text: str,
        size: int,
        coords: tuple[int, int],
        colour: tuple[int, int, int],
    ):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midleft = coords
        surf.blit(text_surface, text_rect)

    def player_coords(self, pos: int) -> tuple[int, int]:
        return self.balance_pos[pos]


class CardPlays:
    """
    Calculates the x, y coords for the cards, calls the hit function on a
    Character() adding a card to the hand.
    """

    def get_card_coords(self, card_position: int, char: Character) -> tuple[int, int]:
        """
        Calculates the x, y pixel positions for the card based on its
        table position.
        """
        pixel_move = 30
        card_gap = 60
        if isinstance(char, Player):
            if card_position == 1:
                return char.get_x_y()
            else:
                x = card_position - 2
                return card_gap + char.get_x_y()[0] + (pixel_move * x), char.get_x_y()[1] - (
                    pixel_move * x
                )
        elif isinstance(char, Dealer):
            if card_position == 1:
                return char.get_x_y()
            else:
                x = card_position - 2
                return card_gap + char.get_x_y()[0] + (pixel_move * x), char.get_x_y()[1] + (
                    pixel_move * x
                )
        else:
            return (0, 0)

    def hit(self, person: Character, deck: Deck_holder) -> None:
        """Hit the given person."""  # crypto docstring
        if not person.bust:
            x, y = self.get_card_coords(len(person.hand) + 1, person)
            person.hit(deck, x, y)

    def draw_hand_cards(self, hand_list: list[Card], area: pygame.surface.Surface) -> None:
        """
        Takes a players hand and displays the cards onto a Pygame surface
        """
        for card in hand_list:
            CardImages().draw_card(area, card)
