import pygame
import config
from os import path, listdir

# ----------------------------------------------------------------
def generate_images():
    btn_dict = {}
    for file in listdir(config.IMG_DIR):
        f = path.join(config.IMG_DIR, file)
        if path.isfile(f):
            btn_dict[file[:-4]] = pygame.image.load(f).convert_alpha()

    # loop scales each image value
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
    def __init__(self, on_click, button_up_img, button_down_img, x, y, active):
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

    def draw_button(self, area) -> None:
        area.blit(self.image[self.index], (self.rect))

    def set_index(self, num) -> None:
        self.index = num

    # x, y are the mouse x, y co_ords
    def check_collide(self, x, y) -> bool:
        if self.rect.collidepoint(x, y) and self.get_active():
            self.set_index(1)
            return True
        return False


class Game_button(Button):
    def __init__(self, on_click, button_up_img, button_down_img, x, y, grey_image):
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
    def __init__(self, on_click, button_up_img, button_down_img, x, y, value):
        super().__init__(on_click, button_up_img, button_down_img, x, y, active=True)
        self.value = value

    def click(self) -> None:
        if self.get_active():
            self.on_click(self.value)

    def reset_image(self) -> None:
        self.set_index(0)
