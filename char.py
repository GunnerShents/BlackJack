from typing import List
import config
from cardclasses import Card, Deck_holder


class Character:
    """
    Abstract class holds cards, prints the cards in the terminal. Checks
    for bust, black jack, actions a hit and adds to the hand list. Returns
    the total and will calculate aces correctly determining when they should
    be value 11 or 1.
    """

    def __init__(self) -> None:
        self.hand: List[Card] = []
        self.name = ""
        self.total = 0
        self.bust = False

    # Prints the cards you have in your hand
    def show_cards(self) -> None:

        print(f"{self.name} is holding: ")
        for card in self.hand:
            print(card)

    # Returns the characters name, name is defined on construction.
    def get_name(self) -> str:

        return self.name

    # Check to see if the player is bust, if not one card is added to the hand
    def hit(self, deck: Deck_holder, x: int = 0, y: int = 0) -> None:

        # takes a new card
        new_card: Card = deck.deal_a_card()
        new_card.x = x
        new_card.y = y
        # adds the new card to the player hand
        self.hand.append(new_card)
        self.check_hand()
        if self.check_bust():
            self.bust = True

    # Check hand for bust and check if it holds aces
    def check_hand(self) -> int:
        self.total = 0
        aces = 0
        # loop through cards in hand, tally aces.
        # value of ace is defaulted to 11!
        card: Card
        for card in self.hand:
            if card.name == "Ace":
                aces += 1
                self.total += card.get_card_value()
            else:
                self.total += card.get_card_value()
        # checks if hand total can be reduced by 10 for each ace in hand.
        if self.check_bust() == True and aces > 0:
            while aces > 0 and self.total > 21:
                self.total -= 10
                aces -= 1
        return self.total

    # returns true if the player is over 21.
    def check_bust(self) -> bool:

        return self.total > 21

    def get_total(self) -> int:

        return self.total

    def check_bj(self) -> bool:

        return len(self.hand) == 2 and self.total == 21

    def reset(self) -> None:
        print("I am the char reset method - parent method")
        self.hand = []
        self.bust = False
        self.total = 0


class Player(Character):
    """
    Inherts form Character(). Holds all the functionality for the player.
    Calculates the logic for winning, losing, drawing and blackjack.
    Will also hold the balance and current bet. Stores x ,y for where the
    cards should render on the game board.
    """

    def __init__(self, name: str, balance: int, start_x: int, start_y: int, position: int) -> None:

        # Load coin image and transform the size.
        self.position = position
        self.hand = []
        self.name = name
        self.balance = balance
        self.bet = 0
        self.bet_made = False
        self.total = 0
        self.bust = False
        self.player_x = start_x
        self.player_y = start_y

    def get_bet_made(self) -> bool:
        return self.bet_made

    def create_start_coords(self, the_offset: int) -> tuple[int, int]:
        # creates game button based off main_player position.
        offset = the_offset
        if self.get_player_pos() == 2:
            btn_pos_x, btn_pos_y = self.get_x_y()[0] - offset, self.get_x_y()[1] + (offset * 2)
        else:
            btn_pos_x, btn_pos_y = self.get_x_y()[0] - offset, self.get_x_y()[1] + (offset // 2 * 5)

        return btn_pos_x, btn_pos_y

    def get_player_pos(self):

        return self.position

    def get_x_y(self) -> tuple[int, int]:

        return self.player_x, self.player_y

    def get_balance(self) -> int:
        return self.balance

    # checks bet is valid, sets self.bet and deducts bet from balance.
    def set_bet(self, amount: int) -> None:
        if not self.bet_made:
            self.bet = amount
            self.balance -= self.bet
            self.bet_made = True

    def get_bet(self) -> int:
        return self.bet

    def black_jack(self) -> None:

        self.balance += self.bet * 3

    def lost(self) -> None:

        print(f"You lost, your balance is {self.balance}")

    def calc_win(self) -> None:
        if self.check_blackjack():
            self.black_jack()
            print("Black Jack!!")
        else:
            self.balance += self.bet
        print(f"You win, your balance is {self.balance}")

    def draw(self) -> None:

        print(f"It's a draw, your balance is {self.balance}")

    def check_blackjack(self) -> bool:

        return self.total == 21 and len(self.hand) == 2

    def reset_bet(self) -> None:
        print("I am the player reset - child method")
        self.bet = 0
        self.bet_made = False


class Dealer(Character):
    """
    Inherts from Character(). Holds the x, y for where the cards render on
    the board. Checks for stand function.
    """

    def __init__(self) -> None:

        self.hand = []
        self.name = "Dealer"
        self.total = 0
        self.bust = False
        self.dealer_x = config.WIDTH // 2 - (config.CARD_WIDTH)
        self.dealer_y = config.HEIGHT // 14 * 2
        self.not_dealers_turn = True

    def get_x_y(self) -> tuple[int, int]:

        return (self.dealer_x, self.dealer_y)

    def check_for_stand(self) -> bool:
        total = self.get_total()
        if 17 <= total <= 21:
            return True
        return False
