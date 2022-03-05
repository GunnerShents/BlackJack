import random
import sys
from os import path
import pygame
import config
from theGame import TheGame
from cardclasses import Deck_holder
from char import Player, Dealer
from seat import Seat
from render import Render

seed = random.randrange(sys.maxsize)
random.seed()


class MainGame:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        # Prepares the game, Deck, Dealer
        self.dealer = Dealer()
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
        self.seat_list: list[Seat] = []
        self.games_in_play: list[TheGame] = []
        for x in range(3):
            seat = Seat(x + 1, self.check_click)
            self.seat_list.append(seat)
        self.frame = 0
        self.the_clock = Render()
        self.a_bet_placed = False
        self.start_clock = False
        self.seats_in_play: set[int] = set()

    def deal_to_table(self):
        """
        Checks which players have bet and deals a round of cards out top all
        players and then the daeler twice.
        """
        for game in self.games_in_play:
            if game.main_player.get_bet_made():
                game.hit(game.main_player)

    def check_whos_in_play(self):
        pass

    def bet_placed(self) -> None:
        """
        checks what players have placed a bet
        """
        print(self.a_bet_placed)
        for game in self.games_in_play:
            if game.bet_placed:
                self.a_bet_placed = True
                if self.players_at_table() > 1:
                    pass
                break
            else:
                self.a_bet_placed = False

    def start_the_clock(self) -> None:
        """
        if any player has placed a bet start the clock
        """
        if self.a_bet_placed:
            self.run_clock()

    def run_clock(self) -> None:
        """
        Checks 30 seconds have not passed. Updates the frames and
        renders the changeable clock to the game board.
        """
        if self.get_second() < 30:
            self.frame += 1
            self.draw_clock()
            print(f"{self.frame} - {self.get_second()}")

    def players_at_table(self) -> int:
        """
        @return number of players at the table during the time a bet
        was locked in.
        """
        return len(self.games_in_play)

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

    def set_clock(self, set_flag: bool) -> None:
        self.start_clock = set_flag

    def reset_clock(self) -> None:
        self.frame = 0
        self.set_clock(False)

    def update_graphics_events(self) -> None:
        """
        Draws the table, card_deck, saet images and checks the colide
        function on the seat image.
        Run function in the main game body
        """
        self.screen.blit(self.table, (0, 0))
        self.deck_img.draw_deck(self.screen)
        if self.check_list_len(self.seat_list):
            for seat in self.seat_list:
                seat.draw_seats(self.screen)
                seat.check_collide_img_change(*pygame.mouse.get_pos())

    def check_list_len(self, list: list[Seat]) -> int:
        return len(list) > 0

    def check_click(self) -> None:
        """
        On clicking seat img, creates a player object
        function run in the game loop
        """
        for seat in self.seat_list:
            if seat.check_collide_click(*pygame.mouse.get_pos()):
                pos = seat.get_position()
                print(f"you clicked seat {pos}")
                self.create_game(seat.x, seat.y, seat.get_position())
                self.seat_list.remove(seat)

    # creates the player object
    def create_game(self, x: int, y: int, pos: int) -> None:
        player = "Phil"
        balance = 150
        player = Player(player, int(balance), x, y, pos)
        game = TheGame(
            screen=self.screen, main_player=player, main_deck=self.main_deck, the_dealer=self.dealer
        )
        self.games_in_play.append(game)

    def runs_game_play(self):
        """
        This method handles all the game logic
        Function run in the game loop
        """
        self.bet_placed()
        self.start_the_clock()


def main() -> None:
    pygame.init()

    screen: pygame.surface.Surface = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Black Jack")
    clock = pygame.time.Clock()
    config.IMG_DIR = path.join(path.dirname(__file__), "images")

    # player = Player("Phil", 500, config.WIDTH//2-(config.CARD_WIDTH), config.HEIGHT//14*10)
    # game = TheGame(screen, player)
    # player.show_cards()
    # print(player.get_total())
    # print("")
    # game.the_dealer.show_cards()
    # print(game.the_dealer.get_total())

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
