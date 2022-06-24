from typing import List
from buttons import generate_images
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
        self.images = generate_images()

    def reset(self) -> None:
        """Clears all the betting chips."""
        self.bets_placed = []

    def draw_total_bet(self, area: Surface, player_pos: tuple[int, int], player_seat: int) -> None:
        """Collects the starting x ,y position. Iterates through bets_placed, decreases the
        y value to stack the chips."""
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

    def double_stack(self, current_player: Player) -> list[Chip]:
        """Iterates through a copy of bets_placed, checks for chip grouping
        then creates new chips, appends to bets_placed."""
        new_stack: list[Chip] = self.bets_placed.copy()
        for chip in new_stack:
            value, image = self.check_chip(chip.chip_value, chip.image, current_player)
            new_chip = Chip(value, image)
            self.bets_placed.append(new_chip)
        return new_stack

    def get_bet_chip_coords(
        self, player_pos: int, player_coords: tuple[int, int]
    ) -> tuple[int, int]:
        """@returns the x, y co-ords for the start position of where the chips are to be drawn."""
        x, y = player_coords
        x += 60
        if player_pos == 2:
            y += 120
        else:
            y += 160
        return x, y

    def create_chip(self, value: int, image: Surface, current_player: Player) -> None:
        """Checks the player has enough balance. Runs check chip for grouping, creates a new chip
        and adds the chip to bets_placed."""
        if value <= current_player.get_balance():
            value, image = self.check_chip(value, image, current_player)
            new_chip = Chip(value, image)
            self.add_chip(new_chip, current_player)

    def check_chip(self, value: int, image: Surface, current_player: Player) -> tuple[int, Surface]:
        """Checks if the new chip clicked can be grouped into a higher value chip
        @returns a tuple chip value and image."""
        num = 0
        # key is the chip value, first value holds number of chips needed to group
        # scenod value holds number of times to remove old chips, third is new chip amount.
        scale: dict[int, list[int]] = {
            5: [3, 4, 20],
            10: [4, 5, 50],
            20: [4, 5, 100],
            50: [1, 3, 100],
        }
        for chip in self.bets_placed:
            if chip.get_chip_value() == value:
                num += 1
        if value != 100 and num == scale[value][0]:
            for x in range(scale[value][1]):
                self.remove_chip(value, current_player)
            value = scale[value][2]
            image = self.images[f"chip_{value}_up"]
            value, image = self.check_chip(value, image, current_player)
            return (value, image)
        else:
            return (value, image)

    def check_stack(self, value: int) -> bool:
        """Checks a chip with @argument value is in bets_placed list"""
        return any(chip.chip_value == value for chip in self.bets_placed)

    def add_chip(self, a_chip: Chip, current_player: Player):
        """Adds a chip to the bets_placed list and increases the total to the players
        total bet made."""
        self.bets_placed.append(a_chip)
        current_player.bet += a_chip.get_chip_value()
        current_player.balance -= a_chip.get_chip_value()

    def remove_chip(self, value: int, current_player: Player) -> None:
        if self.check_stack(value):
            for chip in reversed(self.bets_placed):
                if chip.chip_value == value:
                    self.bets_placed.remove(chip)
                    current_player.bet -= value
                    current_player.balance += value
                    break
