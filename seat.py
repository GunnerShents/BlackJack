# from betting import Betting
from typing import Callable
import config

# from char import Player
from os import path

# from buttons import generate_images, Button, Game_button, Chip_button
import pygame


class Seat:
    """
    Creates a player for the seated postion at the table,
    all the player settings are configured with the x, y values
    held in the dictionary.
    """

    def __init__(self, position: int, click: Callable[..., None]):

        # dict holds coords for the centre of the seat position, in the key as a tuple.
        self.position = position
        self.seat_coords: dict[int, tuple[int, int]] = {
            1: (config.WIDTH // 20 * 2, config.HEIGHT // 10 * 4),
            2: (config.WIDTH // 20 * 8, config.HEIGHT // 10 * 6),
            3: (config.WIDTH // 20 * 14, config.HEIGHT // 10 * 4),
            # 4 is the dealers position
            4: (config.WIDTH // 20 * 8, config.HEIGHT // 10 * 2),
        }
        self.seat_img = [
            pygame.image.load(path.join(config.IMG_DIR, "seat1.png")).convert_alpha(),
            pygame.image.load(path.join(config.IMG_DIR, "seat2.png")).convert_alpha(),
        ]
        self.index = 0
        self.x = self.seat_coords[position][0]
        self.y = self.seat_coords[position][1]
        self.rect = self.seat_img[self.index].get_rect(x=self.x, y=self.y)
        self.active = True
        self.on_click = click

    def draw_seats(self, area: pygame.surface.Surface) -> None:

        area.blit(self.seat_img[self.index], (self.x, self.y))

    def check_collide_img_change(self, x: int, y: int) -> None:
        if self.rect.collidepoint(x, y):
            self.index = 1
        else:
            self.index = 0

    def check_collide_click(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True
        else:
            return False

    def click(self):

        self.on_click()

    def get_position(self):
        return self.position


my_dict = {1: (10, 20)}

x = my_dict[1][0]
for x in range(3):
    print(x)
