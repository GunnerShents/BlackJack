# class Chip()
# constructor (self, chip_value, img)
# class betting()
from typing import List

from pygame.surface import Surface

from char import Player


class Chip:
    """
    Creats a chip when the player bets. Draws the chip and can return its value.
    """

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
    """
    Controls the betting logic in the game. Instantiates a chip when the
    player bets. Holds the total bet. All chips are held in a list. Chips
    can be removed based off their value.
    """

    def __init__(
        self,
    ) -> None:

        self.bets_placed: List[Chip] = []

    def reset(self) -> None:
        """Clears all the betting chips."""
        self.bets_placed = []

    def draw_total_bet(self, area: Surface, player_pos: tuple[int, int], player_seat: int) -> None:
        if len(self.bets_placed) > 0:
            chip_x, chip_y = self.get_bet_chip_coords(
                player_seat,
                player_pos,
            )
            for chip in self.bets_placed:
                # player x, y is corrected to render infront of chip button
                # graphics.
                chip.x = chip_x
                chip.y = chip_y
                chip.draw_chip(area)
                chip_y -= 4

    def double_stack(self) -> list[Chip]:
        """Creates a new list, iterates through bets_placed, creates new chips,
        ammend x co-ord and appends to new list. Then extends the bets_placed list."""
        new_stack: list[Chip] = []
        for chip in self.bets_placed:
            new_x = chip.x - chip.image.get_width()
            new_chip = Chip(chip.chip_value, chip.image, new_x, chip.y)
            new_stack.append(new_chip)
        return new_stack

    def get_bet_chip_coords(
        self, player_pos: int, player_coords: tuple[int, int]
    ) -> tuple[int, int]:
        x, y = player_coords
        x += 60
        if player_pos == 2:
            y += 120
        else:
            y += 160
        return x, y

    def create_chip(self, value: int, image: Surface, current_player: Player) -> None:
        """Checks there is enough balance the place another betting chip down.
        Creates a chip with the correct value and image, adds to bets_placed lit.
        tallies the total, deducts the value from the player balance."""
        if current_player.get_bet() + value <= current_player.get_balance():
            new_chip = Chip(value, image)
            self.bets_placed.append(new_chip)
            current_player.bet += value
            current_player.balance -= value
            print(current_player.get_bet())

    def check_stack(self, value: int) -> bool:
        return any(chip.chip_value == value for chip in self.bets_placed)

    def remove_chip(self, value: int, current_player: Player) -> None:
        if self.check_stack(value):
            for chip in reversed(self.bets_placed):
                if chip.chip_value == value:
                    self.bets_placed.remove(chip)
                    current_player.bet -= value
                    current_player.balance += value
                    print(current_player.get_bet())
                    break
