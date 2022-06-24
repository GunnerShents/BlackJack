# class Chip()
# constructor (self, chip_value, img)
# class betting()
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
        appends to new list. Then extends the bets_placed list."""
        new_stack: list[Chip] = []
        for chip in self.bets_placed:
            new_chip = Chip(chip.chip_value, chip.image, chip.x, chip.y)
            new_stack.append(new_chip)
        self.bets_placed.extend(new_stack)
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
        """Checks there is enough balance places another betting chip down.
        Creates a chip with the correct value and image, adds to bets_placed list.
        tallies the total, deducts the value from the player balance."""
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
            print(f"i am working with value {value}")
            for x in range(scale[value][1]):
                self.remove_chip(value, current_player)
            value = scale[value][2]
            image = self.images[f"chip_{value}_up"]
            value, image = self.check_chip(value, image, current_player)
            print(f"I am the value {value}")
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
                    print(current_player.get_bet())
                    break
