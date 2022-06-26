from data import DataEntry
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
from buttons import Game_button, generate_images
from timer import Timer

seed = random.randrange(sys.maxsize)
random.seed()


class MainGame:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        # Prepares the game, Deck, Dealer
        self.dealer = Dealer()
        self.card_plays = CardPlays()
        self.players_turn = False
        self.main_deck = Deck_holder()
        self.main_deck.create_multi_decks(6)
        self.main_deck.shuffle_holder()
        self.starting_cards = 2
        # ---------------------------------
        # Creates the game reset button
        all_images: dict[str, pygame.pygame.Surface] = generate_images()
        self.reset_btn = Game_button(
            self.reset_all_hands,
            all_images["reset1"],
            all_images["reset2"],
            config.WIDTH // 24,
            config.HEIGHT // 24,
            all_images["reset3"],
        )
        # --------------------------------
        self.screen = screen
        self.table = pygame.image.load(
            path.join(config.IMG_DIR, "blackjackTable2.png")
        ).convert_alpha()
        self.deck_img = Deck_holder()
        # ---------------------------------
        # Sets up the game
        self.player_data = DataEntry("playerData")
        self.timer = Timer(config.FPS)
        self.draw_card_images = CardImages()
        self.card_plays = CardPlays()
        self.seat_list: list[Seat] = []
        self.games_in_play: list[PlayerInSeat] = []
        self.game_index_position = 0
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
                    self.set_index_position()
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
        have their betting chips deactivated and turn_over variable is set to True.
        """
        first_player = True
        for game in self.games_in_play:
            if (game.bet_placed == True) and (first_player == True):
                game.bet_btn.set_active(False)
                game.double_btn.set_active(True)
                game.stand_btn.set_active(True)
                game.card_plays_btn.set_active(True)
                if game.main_player.can_split():
                    game.split_btn.set_active(True)
                first_player = False
            else:
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

            return all_bets == len(self.games_in_play) or self.timer.timer_finished()
        return False

    # -----------------------------------------------------
    # Clock methods
    def start_the_clock(self) -> None:
        """
        if any player has placed a bet start the clock
        """
        if any(game.bet_placed for game in self.games_in_play):
            self.timer.set_timer_limit(10)
            self.timer.run_timer()
            self.draw_clock()

    def draw_clock(self) -> None:
        self.the_clock.drawText(
            surf=self.screen,
            text=str(self.timer.get_second()),
            size=30,
            coords=(config.WIDTH // 20 * 18, config.HEIGHT // 20 * 1),
            colour=config.WHITE,
        )

    # ------------------------------------------------------
    # Game methods

    def updates_graphics_and_runs_functionality(self) -> None:
        """
        Draws the table, card_deck, seat images, reset button and checks the colide
        function on the seat image. If a player presses the leave button they
        are removed from the table.

        Run function in the main game body
        """
        self.screen.blit(self.table, (0, 0))
        self.deck_img.draw_deck(self.screen)
        self.reset_btn.draw_button(self.screen)
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
        for game in self.games_in_play:
            if game.game_over == True:
                self.games_in_play.remove(game)
                seat = Seat(game.main_player.get_player_pos(), self.check_click)
                self.seat_list.append(seat)
                self.player_data.update_dict(
                    game.main_player.get_name(), game.main_player.get_balance()
                )

    def check_click(self) -> None:
        """
        On clicking seat img, creates a player object
        function run in the game loop
        """
        for seat in self.seat_list:
            if seat.check_collide_click(*pygame.mouse.get_pos()):
                self.create_game(int(seat.x), int(seat.y), seat.get_position())
                self.seat_list.remove(seat)
        # actions click function if reset button clicked and active
        if self.reset_btn.check_collide(*pygame.mouse.get_pos()):
            self.reset_btn.click()

    # creates the player object
    def create_game(self, x: int, y: int, pos: int) -> None:
        """A game is defined as the plater versus the dealer."""
        p_name, p_bal = self.player_data.create_random()
        player = Player(p_name, int(p_bal), x, y, pos)
        game = PlayerInSeat(
            screen=self.screen, main_player=player, main_deck=self.main_deck, the_dealer=self.dealer
        )
        if self.betting_finished():
            game.set_all_btns(game.get_chip_btns(), False)
        self.games_in_play.append(game)

    def dealer_and_results(self):
        """Shows the dealers cards, hits to dealer if needed.
        Calulates the results for all hands playing.
        """
        while not self.dealer.check_for_stand():
            self.card_plays.hit(self.dealer, self.main_deck)
        for game in self.games_in_play:
            if game.main_player.get_bet_made():
                game.check_result()

    def set_index_position(self) -> bool:
        """Sets game_index_position to the first player in the list who has bet and
        is in play"""
        for index, game in enumerate(self.games_in_play):
            if game.main_player.get_bet_made():
                self.game_index_position = index
                return True
        return False

    def find_next_player(
        self,
    ) -> bool:
        """Checks the next player in the games list that has bet and is in play"""
        if self.game_index_position == len(self.games_in_play) - 1:
            return False
        else:
            for game in range(self.game_index_position + 1, len(self.games_in_play)):
                if self.games_in_play[game].main_player.get_bet_made():
                    self.game_index_position = game
                    return True
            return False

    def runs_game_play(self):
        """
        This method handles all the game logic for the table.
        Handles the bets placed, launches the clock, deals to the
        players. Checks next player and sets the buttons depending hand
        condition."""
        if self.betting:
            self.start_the_clock()
            self.deal_to_table()
        elif self.players_turn:
            if self.games_in_play[self.game_index_position].get_turn_over():
                if self.find_next_player():
                    self.games_in_play[self.game_index_position].bet_btn.set_active(False)
                    self.games_in_play[self.game_index_position].double_btn.set_active(True)
                    self.games_in_play[self.game_index_position].stand_btn.set_active(True)
                    self.games_in_play[self.game_index_position].card_plays_btn.set_active(True)
                    if self.games_in_play[self.game_index_position].main_player.can_split():
                        self.games_in_play[self.game_index_position].split_btn.set_active(True)
                else:
                    self.dealer_and_results()
                    self.players_turn = False
                    self.reset_btn.set_active(True)
                    self.reset_btn.reset_image()

    def reset_all_hands(self):
        """resets the hand after a round has played, including the clock, the,
        the dealer, the player betting chips, the bet button and betting, clears chip bets."""
        self.timer.reset_timer()
        self.dealer.reset()
        for game in self.games_in_play:
            game.main_player.reset()
            game.bet_placed = False
            game.set_turn_over(False)
            game.set_all_btns(game.chip_btns, True)
            game.player_bet.reset()
            game.leave_btn.set_active(True)
        self.reset_btn.set_active(False)
        self.betting = True

    def update_and_close_table(self):
        """Updates the database and file with the players current balances."""
        for g in self.games_in_play:
            n, b = g.main_player.get_name(), g.main_player.get_balance()
            self.player_data.update_dict(n, b)
        self.player_data.update_file()


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
                main_game.update_and_close_table()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                main_game.reset_btn.reset_image()

        screen.fill(config.BLACK)
        main_game.updates_graphics_and_runs_functionality()
        for game in main_game.games_in_play:
            game.draw_all_graphics()
        main_game.runs_game_play()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
