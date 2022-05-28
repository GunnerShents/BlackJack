from os import path
from typing import List, TypeVar
import pygame
import config
from betting import Betting
from buttons import Button, Chip_button, Game_button, generate_images
from cardclasses import CardImages, Deck_holder
from char import Dealer, Player
from render import Text, CardPlays

T = TypeVar("T", bound=Button)


class PlayerInSeat:
    def __init__(
        self,
        screen: pygame.surface.Surface,
        main_player: Player,
        main_deck: Deck_holder,
        the_dealer: Dealer,
    ) -> None:
        self.screen = screen
        self.the_deck = main_deck
        self.starting_cards = 2
        # player attributes
        self.main_player = main_player
        # dealer attributes
        self.the_dealer = the_dealer
        # images and button attributes
        self.game_btns: List[Game_button] = []
        self.chip_btns: List[Chip_button] = []
        self.btn_dict = generate_images()
        coin_img = pygame.image.load(path.join(config.IMG_DIR, "coin.png")).convert_alpha()
        self.coin_img = pygame.transform.scale(coin_img, (config.COIN_X, config.COIN_Y))
        self.card_images = CardImages()
        self.create_game_buttons()
        self.create_chip_btns()
        self.need_back = False
        self.frame = 0
        # Betting functionality
        self.card_plays = CardPlays()
        self.player_bet = Betting()
        self.bet_placed = False
        # text rendering
        self.text = Text()

    def set_all_btns(self, btn_list: list[T], bool: bool):
        """sets all the chip buttons to the argument"""
        for btn in btn_list:
            btn.set_active(bool)

    def get_chip_btns(self) -> list[Chip_button]:
        return self.chip_btns

    def get_game_btns(self) -> list[Game_button]:
        return self.game_btns

    # # deal one card to each player in the self.total_player list
    def deal_table(self) -> None:
        pass

    #     self.need_back = True
    #     print(self.main_player.bet)
    #     self.card_plays.hit(self.main_player, self.the_deck)
    #     # self.card_plays(self.the_dealer)
    #     self.card_plays.hit(self.main_player, self.the_deck)
    #     # self.card_plays(self.the_dealer)
    #     print(f"the player has {self.main_player.get_total()}")
    #     # print(f"the dealer has {self.the_dealer.get_total()}")
    #     self.deal_btn.set_active(False)
    #     self.stand_btn.set_active(True)
    #     self.card_plays_btn.set_active(True)

    def stand(self) -> None:

        self.need_back = False
        # returns true if dealer has 17 - 21
        if self.main_player.check_blackjack():
            self.check_result()
        elif self.the_dealer.check_for_stand() or self.main_player.check_bust():
            self.check_result()
        else:
            while not self.the_dealer.bust and not self.the_dealer.check_for_stand():
                self.card_plays.hit(self.the_dealer, self.the_deck)
                self.the_dealer.show_cards()
            self.check_result()
        self.deal_btn.set_active(False)
        self.stand_btn.set_active(False)
        self.card_plays_btn.set_active(False)
        self.bet_btn.set_active(False)
        for btn in self.chip_btns:
            btn.set_active(True)

    # checks player score to the dealers score
    # calculates the bet return.
    def check_result(self) -> None:
        if self.main_player.check_bust():
            self.main_player.lost()
        elif self.the_dealer.check_bust():
            self.main_player.calc_win()
        elif self.main_player.total > self.the_dealer.total:
            self.main_player.calc_win()
        elif self.main_player.total < self.the_dealer.total:
            self.main_player.lost()
        else:
            self.main_player.draw()
        self.deal_btn.set_active(True)
        # reset bets and chip stack
        self.main_player.reset_bet()
        self.player_bet.reset()

    def create_game_buttons(self) -> None:
        # space out butons
        off_set = 100
        btn_pos_x, btn_pos_y = self.main_player.create_start_coords(100)

        def hit_main_player() -> None:
            self.card_plays.hit(self.main_player, self.the_deck)

        def player_place_bet() -> None:
            self.main_player.set_bet(self.player_bet.get_total())
            print(self.main_player.get_bet())
            self.deal_btn.set_active(True)
            self.bet_btn.set_active(False)
            self.reset_hand()
            for btn in self.chip_btns:
                btn.set_active(False)
            # game action bet placed
            self.bet_placed = True

        self.bet_btn = Game_button(
            player_place_bet,
            self.btn_dict["bet_up"],
            self.btn_dict["bet_down"],
            btn_pos_x,
            btn_pos_y,
            self.btn_dict["bet_grey"],
        )
        self.game_btns.append(self.bet_btn)
        self.deal_btn = Game_button(
            self.deal_table,
            self.btn_dict["deal_up"],
            self.btn_dict["deal_down"],
            btn_pos_x + off_set,
            btn_pos_y,
            self.btn_dict["deal_grey"],
        )
        self.game_btns.append(self.deal_btn)
        self.card_plays_btn = Game_button(
            hit_main_player,
            self.btn_dict["hit_up"],
            self.btn_dict["hit_down"],
            btn_pos_x + (off_set * 2),
            btn_pos_y,
            self.btn_dict["hit_grey"],
        )
        self.game_btns.append(self.card_plays_btn)
        self.stand_btn = Game_button(
            self.stand,
            self.btn_dict["stand_up"],
            self.btn_dict["stand_down"],
            btn_pos_x + (off_set * 3),
            btn_pos_y,
            self.btn_dict["stand_grey"],
        )
        self.game_btns.append(self.stand_btn)

    def create_chip_btns(self) -> None:
        def chip_btn_action(value: int) -> None:

            self.player_bet.create_chip(
                value, self.btn_dict[f"chip_{value}_up"], self.main_player.get_balance()
            )
            self.bet_btn.set_active(True)

        self.btn_dict = generate_images()
        btn_x, btn_y = self.main_player.create_start_coords(80)
        numbers = [5, 10, 20, 50, 100]
        for num in numbers:
            bet_btn = Chip_button(
                chip_btn_action,
                self.btn_dict[f"chip_{num}_up"],
                self.btn_dict[f"chip_{num}_down"],
                btn_x,
                btn_y,
                num,
            )
            self.chip_btns.append(bet_btn)
            btn_x += 70

    def reset_hand(self) -> None:
        self.main_player.reset()
        # self.the_dealer.reset()

    def draw_all_graphics(self) -> None:
        # drawing the betting chips
        self.player_bet.draw_total_bet(
            self.screen, self.main_player.get_x_y(), self.main_player.get_player_pos()
        )
        # drawing the betting chips
        for cbtn in self.chip_btns:
            cbtn.draw_button(self.screen)
        # drawing the game buttons
        for gbtn in self.game_btns:
            gbtn.draw_button(self.screen)
        for card in self.main_player.hand:
            self.card_images.draw_card(self.screen, card)
        # self.draw_hand_cards(self.the_dealer.hand)
        # draw balance
        self.text.drawText(
            surf=self.screen,
            text=str(self.main_player.get_balance()),
            size=34,
            coords=self.text.player_coords(self.main_player.get_player_pos()),
            colour=config.WHITE,
        )

    def event_handler_on_click(self) -> None:
        for gbtn in self.game_btns:
            if gbtn.check_collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                gbtn.click()
        for cbtn in self.chip_btns:
            if cbtn.check_collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                cbtn.click()

    def event_handler_right_click(self) -> None:
        for cbtn in self.chip_btns:
            if cbtn.check_collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.player_bet.remove_chip(cbtn.value)

    def reset_buttons(self) -> None:
        for gbtn in self.game_btns:
            gbtn.reset_image()
        for cbtn in self.chip_btns:
            cbtn.reset_image()
