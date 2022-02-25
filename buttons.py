from os import listdir, path
from typing import Callable, Dict

import pygame
from pygame.surface import Surface

import config


# ----------------------------------------------------------------
#pulls all graphice into a dictionary, key is the png name.
#value is the pygame image.
def generate_images() -> Dict[str, Surface]:
    btn_dict: Dict[str, Surface] = {}
    for file in listdir(config.IMG_DIR):
        f = path.join(config.IMG_DIR, file)
        if path.isfile(f):
            btn_dict[file[:-4]] = pygame.image.load(f).convert_alpha()

    # loop scales each image value and resizes.
    btn: str
    for btn in btn_dict.keys():
        if btn[:5] == "chip_":
            btn_dict[btn] = pygame.transform.scale(
                btn_dict[btn],
                ((config.BUTTON_WIDTH / 5) * 3, (config.BUTTON_HEIGHT / 5) * 3),
            )
        else:
            btn_dict[btn] = pygame.transform.scale(
                btn_dict[btn], (config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
            )

    return btn_dict


class Button:
    """
    Abstract class, draws the button, checks collide and sets active. Also
    uses a call back function from the first argument in the constructor back 
    to the game. 
    """
    def __init__(
        self,
        on_click: Callable[..., None],
        button_up_img: Surface,
        button_down_img: Surface,
        x: int,
        y: int,
        active: bool,
    ):
        assert callable(on_click)
        self.on_click = on_click
        self.image = [button_up_img, button_down_img]
        self.index = 0
        self.rect = self.image[self.index].get_rect(x=x, y=y)
        self.active = active
        # self.image_change = False

    def set_active(self, bool: bool) -> None:
        self.active = bool

    def get_active(self) -> bool:
        return self.active

    def draw_button(self, area: Surface) -> None:
        area.blit(self.image[self.index], (self.rect))

    def set_index(self, num: int) -> None:
        self.index = num

    # x, y are the mouse x, y co_ords
    def check_collide(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y) and self.get_active():
            self.set_index(1)
            return True
        return False


class Game_button(Button):
    """
    Controls the game buttons running along the bottom of the interface.
    Inherts form Button(). Game buttons have 3 images.
    """
    def __init__(
        self,
        on_click: Callable[..., None],
        button_up_img: Surface,
        button_down_img: Surface,
        x: int,
        y: int,
        grey_image: Surface,
    ):
        super().__init__(on_click, button_up_img, button_down_img, x, y, active=False)
        self.grey_img = grey_image
        self.image.append(self.grey_img)
        if not self.active:
            self.index = 2

    def reset_image(self) -> None:
        if self.get_active():
            self.set_index(0)
        else:
            self.set_index(2)

    def click(self) -> None:
        if self.get_active():
            self.on_click()


class Chip_button(Button):
    """
    Inherts form Button, this class controls the betting chip buttons.
    Chip buttons have two images.
    """
    def __init__(
        self,
        on_click: Callable[..., None],
        button_up_img: Surface,
        button_down_img: Surface,
        x: int,
        y: int,
        value: int,
    ) -> None:
        super().__init__(on_click, button_up_img, button_down_img, x, y, active=True)
        self.value = value

    def click(self) -> None:
        if self.get_active():
            self.on_click(self.value)

    def reset_image(self) -> None:
        self.set_index(0)
