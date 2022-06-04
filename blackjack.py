import random
import sys
from os import path
import pygame
import config
from playerInSeat import PlayerInSeat
from cardclasses import Deck_holder, CardImages
from char import Player, Dealer
from seat import Seat
from render import Text, CardPlays

seed = random.randrange(sys.maxsize)
random.seed()


class MainGame:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        # Prepares the game, Deck, Dealer
        self.dealer = Dealer()
        self.players_turn = False
        self.main_deck = Deck_holder()
        self.main_deck.create_multi_decks(6)
        self.main_deck.shuffle_holder()
        self.starting_cards = 2
        # --------------------------------
        self.screen = screen
        self.table = pygame.image.load(
            path.join(config.IMG_DIR, "blackjackTable2.png")
        ).convert_alpha()
        self.deck_img = Deck_holder()
        # ---------------------------------
        # Sets up the game
        self.draw_card_images = CardImages()
        self.card_plays = CardPlays()
        self.seat_list: list[Seat] = []
        self.games_in_play: list[PlayerInSeat] = []
        # self.hand_in_play = []
        for x in range(3):
            seat = Seat(x + 1, self.check_click)
            self.seat_list.append(seat)
        self.betting = True
        self.frame = 0
        self.the_clock = Text()
        self.bet_timer = 10
        self.seats_in_play: set[int] = set()

    # --------------------------------------------------
    def deal_to_table(self):
        """
        Checks which players have bet and deals two cards to each player in turn.
        Resets the clock after the cards are dealt.
        """
        if self.betting_finished():
            self.order_player_list()
            for game in self.games_in_play:
                if game.main_player.get_bet_made() and len(game.main_player.hand) < 2:
                    game.card_plays.hit(game.main_player, self.main_deck)
            # if the dealer has < 2 cards in the hand.
            if len(self.dealer.hand) < 2:
                #   deal one card
                self.card_plays.hit(self.dealer, self.main_deck)
                if len(self.dealer.hand) == 2:
                    self.players_turn = True
                    self.set_buttons()
                    self.betting = False
                    for x in self.games_in_play:
                        x.reset_buttons()

    def order_player_list(self):
        """orders the player list by seat position"""
        sorted_list: list[PlayerInSeat] = []
        index = 3
        while len(sorted_list) != len(self.games_in_play):
            for game in self.games_in_play:
                if game.main_player.get_player_pos() == index:
                    sorted_list.append(game)
            index -= 1
        self.games_in_play = sorted_list

    def set_buttons(self) -> None:
        """
        For players with a placed bet deactivates the deal and bet button.
        Activates the stand and hit buttons. Players at the table with no bets placed
        have their betting chips deactivated.
        """
        first_player = True
        for game in self.games_in_play:
            print(game.bet_placed)
            if (game.bet_placed == True) and (first_player == True):
                game.bet_btn.set_active(False)
                game.deal_btn.set_active(False)
                game.stand_btn.set_active(True)
                game.card_plays_btn.set_active(True)
                first_player = False
                print("you see me once")
            else:
                print("you see me twice")
                game.set_all_btns(game.get_game_btns(), False)
                game.set_all_btns(game.get_chip_btns(), False)

    def betting_finished(self) -> bool:
        """
        if table is not empty. Returns true if all players have made their
        bet or if the timer has reached the cut off.
        """
        if len(self.games_in_play) > 0:
            all_bets = 0
            for game in self.games_in_play:
                if game.main_player.get_bet_made():
                    all_bets += 1

            return all_bets == len(self.games_in_play) or self.get_second() == self.bet_timer
        return False

    # -----------------------------------------------------
    # Clock methods
    def start_the_clock(self) -> None:
        """
        if any player has placed a bet start the clock
        """
        if any(game.bet_placed for game in self.games_in_play):
            self.run_clock()

    def run_clock(self) -> None:
        """
        Checks the bet_timer in seconds have not passed. Updates the frames and
        renders the changeable clock to the game board.
        """
        if self.get_second() < self.bet_timer:
            self.frame += 1
            self.draw_clock()

    def get_second(self) -> int:
        second = self.frame // config.FPS
        return second

    def draw_clock(self) -> None:
        self.the_clock.drawText(
            surf=self.screen,
            text=str(self.get_second()),
            size=30,
            coords=(config.WIDTH // 20 * 18, config.HEIGHT // 20 * 1),
            colour=config.WHITE,
        )

    def reset_clock(self) -> None:
        self.frame = 0

    # ------------------------------------------------------
    # Game methods

    def update_graphics_events(self) -> None:
        """
        Draws the table, card_deck, seat images and checks the colide
        function on the seat image.
        Run function in the main game body
        """
        self.screen.blit(self.table, (0, 0))
        self.deck_img.draw_deck(self.screen)
        if self.players_turn:
            self.draw_card_images.draw_card_back(self.screen, self.dealer.hand[0])
            self.draw_card_images.draw_card(self.screen, self.dealer.hand[1])
        else:
            for card in self.dealer.hand:
                self.draw_card_images.draw_card(self.screen, card)
        if len(self.seat_list) > 0:
            for seat in self.seat_list:
                seat.draw_seats(self.screen)
                seat.check_collide_img_change(*pygame.mouse.get_pos())

    def check_click(self) -> None:
        """
        On clicking seat img, creates a player object
        function run in the game loop
        """
        for seat in self.seat_list:
            if seat.check_collide_click(*pygame.mouse.get_pos()):
                print(seat.position)
                self.create_game(seat.x, seat.y, seat.get_position())
                self.seat_list.remove(seat)

    # creates the player object
    def create_game(self, x: int, y: int, pos: int) -> None:
        player = "Phil"
        balance = 150
        player = Player(player, int(balance), x, y, pos)
        game = PlayerInSeat(
            screen=self.screen, main_player=player, main_deck=self.main_deck, the_dealer=self.dealer
        )
        if self.betting_finished():
            game.set_all_btns(game.get_chip_btns(), False)
        self.games_in_play.append(game)

    def runs_game_play(self):
        """
        This method handles all the game logic for the table.
        Handles the bets placed, launches the clock, deals to the
        players.
        """
        if self.betting:
            self.start_the_clock()
            self.deal_to_table()


def main() -> None:
    pygame.init()

    screen: pygame.surface.Surface = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Black Jack")
    clock = pygame.time.Clock()
    config.IMG_DIR = path.join(path.dirname(__file__), "images")

    # Loading the main game
    main_game = MainGame(screen)

    running = True
    # --------------------------------------------------------------------------
    # main game loop
    while running:

        clock.tick(config.FPS)
        for event in pygame.event.get():

            # Check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    main_game.check_click()
                    for game in main_game.games_in_play:
                        game.event_handler_on_click()
                if pygame.mouse.get_pressed() == (0, 0, 1):
                    for game in main_game.games_in_play:
                        game.event_handler_right_click()
            elif event.type == pygame.MOUSEBUTTONUP:
                for game in main_game.games_in_play:
                    game.reset_buttons()

        screen.fill(config.BLACK)
        main_game.update_graphics_events()
        for game in main_game.games_in_play:
            game.draw_all_graphics()
        main_game.runs_game_play()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
