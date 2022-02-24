# class Chip()
# constructor (self, chip_value, img)
# class betting()
from typing import List

from pygame.surface import Surface


class Chip:
    def __init__(self, chip_value: int, img: Surface, x: int = 0, y: int = 0):
        self.chip_value = chip_value
        self.image = img
        self.x = x
        self.y = y
        self.chip_number = 0

    def draw_chip(self, area: Surface) -> None:
        area.blit(self.image, (self.x, self.y))

    def get_chip_value(self) -> int:
        return self.chip_value


class Betting:
    def __init__(
        self,
    ) -> None:

        self.total = 0
        self.bets_placed: List[Chip] = []

    def reset(self) -> None:
        self.total = 0
        self.bets_placed = []

    def draw_total_bet(self, area: Surface) -> None:
        if len(self.bets_placed) > 0:
            chip_x = 100
            chip_y = 550
            for chip in self.bets_placed:
                chip.x = chip_x
                chip.y = chip_y
                chip.draw_chip(area)
                chip_y -= 4

    def get_total(self) -> int:
        return self.total

    def create_chip(self, value: int, image: Surface, current_player_balance: int) -> None:
        if self.get_total() + value <= current_player_balance:
            new_chip = Chip(value, image)
            self.bets_placed.append(new_chip)
            self.total += value
            print(self.get_total())

    def check_stack(self, value: int) -> bool:
        return any(chip.chip_value == value for chip in self.bets_placed)

    def remove_chip(self, value: int) -> None:
        if self.check_stack(value):
            for chip in reversed(self.bets_placed):
                if chip.chip_value == value:
                    self.total -= chip.chip_value
                    self.bets_placed.remove(chip)
                    break
        print(self.get_total())
