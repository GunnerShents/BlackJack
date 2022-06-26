import yaml
from yaml.loader import SafeLoader
import random


class DataEntry:
    """Collects, adds and displays the information held in the yaml file."""

    def __init__(self, a_file: str):

        self.a_file: str = a_file
        self.all_players: dict[str, int] = {}
        self.player_names: list[str] = []

        self.set_up()

    def update_dict(self, a_name: str, new_bal: int):
        """Updates the balance in the dict collection.
        Adds, the player back into the player list."""
        self.all_players[a_name] = new_bal
        self.player_names.append(a_name)

    def update_file(self):
        """Updates the yaml file used to create the class,
        with all_players dict"""
        with open(f"{self.a_file}.yaml", "w") as yamlfile:
            yaml.dump(self.all_players, yamlfile)
            print(f"{self.a_file} updated")

    def read_in(self):
        """Loads the yaml file in as a dictionary to all_players."""
        try:
            with open(f"{self.a_file}.yaml") as f:
                self.all_players = yaml.load(f, Loader=SafeLoader)
                print(yaml.safe_load(f))
        except FileNotFoundError as exc:
            print(f"file name not recognised!!\n{exc}")

    def all_names(self):
        """creates a list of the just the player names."""
        player_list = self.get_collection().keys()
        for p_name in player_list:
            self.player_names.append(p_name)

    def get_collection(self) -> dict[str, int]:
        """@returns the full player collection"""
        return self.all_players

    def show_players(self):
        """prints all the players held in collection"""
        [print(k, v) for k, v in self.all_players.items()]

    def player_balance(self, name: str) -> str | int:
        """@returns a players balance."""
        return self.all_players[name]

    def set_up(self):
        """Runs all functions needed when the class is instantiated."""
        self.read_in()
        self.all_names()

    def create_random(self) -> tuple[str, int]:
        """Randomly choices a player rfemoves them from the player list,
        @returns the name and balance."""
        p_name = random.choice(self.player_names)
        self.player_names.remove(p_name)
        return p_name, self.all_players[p_name]
