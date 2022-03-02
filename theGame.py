from os import path
from typing import List, Tuple
import pygame
import config
from betting import Betting
from buttons import Chip_button, Game_button, generate_images
from cardclasses import Card, CardImages, Deck_holder
from char import Character, Dealer, Player
from text import Text

        

class TheGame:
    def __init__(self, screen: pygame.surface.Surface, main_player: Player) -> None:
        self.screen = screen
        self.main_deck = Deck_holder()
        self.main_deck.create_multi_decks(6)
        self.main_deck.shuffle_holder()
        self.starting_cards = 2
        # player attributes
        self.main_player = main_player
        # dealer attributes
        self.the_dealer = Dealer()
        # images and button attributes
        self.btn_imgs: List[Game_button] = []
        self.chip_btn_images: List[Chip_button] = []
        self.btn_dict = generate_images()
        coin_img = pygame.image.load(path.join(config.IMG_DIR, "coin.png")).convert_alpha()
        self.coin_img = pygame.transform.scale(coin_img, (config.COIN_X, config.COIN_Y))
        self.card_images = CardImages()
        self.create_game_buttons()
        self.create_chip_btns()
        self.need_back = False
        self.frame = 0
        # Betting functionality
        self.player_bet = Betting()
        #text rendering
        self.text = Text()

    # deal one card to each player in the self.total_player list
    def deal_table(self) -> None:

        self.need_back = True
        print(self.main_player.bet)
        self.hit(self.main_player)
        self.hit(self.the_dealer)
        self.hit(self.main_player)
        self.hit(self.the_dealer)
        print(f"the player has {self.main_player.get_total()}")
        print(f"the dealer has {self.the_dealer.get_total()}")
        self.deal_btn.set_active(False)
        self.stand_btn.set_active(True)
        self.hit_btn.set_active(True)

    def get_card_coords(self, card_position: int, player: Character) -> Tuple[int, int]:
        pixel_move = 30
        card_gap = 60
        if player == self.main_player:
            if card_position == 1:
                return self.main_player.get_x_y()
            else:
                x = card_position - 2
                return card_gap + self.main_player.get_x_y()[0]+(pixel_move * x), self.main_player.get_x_y()[1] - (pixel_move * x)
        elif player == self.the_dealer:
            if card_position == 1:
                return self.the_dealer.get_x_y()
            else:
                x = card_position - 2
                return  card_gap + self.the_dealer.get_x_y()[0]+ (pixel_move * x), self.the_dealer.get_x_y()[1] + (pixel_move * x)
        else:
            return (0, 0)

    def reset_hand(self) -> None:

        self.main_player.reset()
        self.the_dealer.reset()

    def hit(self, person: Character) -> None:
        """Hit the given person."""  # crypto docstring
        if not person.bust:
            x, y = self.get_card_coords(len(person.hand) + 1, person)
            person.hit(self.main_deck, x, y)

    def stand(self) -> None:

        self.need_back = False
        # returns true if dealer has 17 - 21
        if self.main_player.check_blackjack():
            self.check_result()
        elif self.the_dealer.check_for_stand() or self.main_player.check_bust():
            self.check_result()
        else:
            while not self.the_dealer.bust and not self.the_dealer.check_for_stand():
                self.hit(self.the_dealer)
                self.the_dealer.show_cards()
            self.check_result()
        self.deal_btn.set_active(False)
        self.stand_btn.set_active(False)
        self.hit_btn.set_active(False)
        self.bet_btn.set_active(False)
        for btn in self.chip_btn_images:
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
        #space out butons
        off_set = 100
        btn_pos_x, btn_pos_y = self.main_player.create_start_coords(100)

        def hit_main_player() -> None:
            self.hit(self.main_player)

        def player_place_bet() -> None:
            self.main_player.set_bet(self.player_bet.get_total())
            print(self.main_player.get_bet())
            self.deal_btn.set_active(True)
            self.bet_btn.set_active(False)
            self.reset_hand()
            for btn in self.chip_btn_images:
                btn.set_active(False)

        self.bet_btn = Game_button(
            player_place_bet,
            self.btn_dict["bet_up"],
            self.btn_dict["bet_down"],
            btn_pos_x,
            btn_pos_y,
            self.btn_dict["bet_grey"],
        )
        self.btn_imgs.append(self.bet_btn)
        self.deal_btn = Game_button(
            self.deal_table,
            self.btn_dict["deal_up"],
            self.btn_dict["deal_down"],
            btn_pos_x + off_set,
            btn_pos_y,
            self.btn_dict["deal_grey"],
        )
        self.btn_imgs.append(self.deal_btn)
        self.hit_btn = Game_button(
            hit_main_player,
            self.btn_dict["hit_up"],
            self.btn_dict["hit_down"],
            btn_pos_x + (off_set*2),
            btn_pos_y,
            self.btn_dict["hit_grey"],
        )
        self.btn_imgs.append(self.hit_btn)
        self.stand_btn = Game_button(
            self.stand,
            self.btn_dict["stand_up"],
            self.btn_dict["stand_down"],
            btn_pos_x + (off_set*3),
            btn_pos_y,
            self.btn_dict["stand_grey"],
        )
        self.btn_imgs.append(self.stand_btn)

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
            self.chip_btn_images.append(bet_btn)
            btn_x += 70

    def draw_all_graphics(self) -> None:
        # drawing the betting chips
        self.player_bet.draw_total_bet(self.screen, self.main_player.get_x_y(), self.main_player.get_player_pos())
        # drawing the betting chips
        for cbtn in self.chip_btn_images:
            cbtn.draw_button(self.screen)
        # drawing the game buttons
        for gbtn in self.btn_imgs:
            gbtn.draw_button(self.screen)
        self.draw_hand_cards(self.main_player.hand)
        self.draw_hand_cards(self.the_dealer.hand)
        #draw balance
        self.text.drawText(self.screen,
                           str(self.main_player.get_balance()),
                           34,
                           self.text.player_coords(self.main_player.get_player_pos()),
                           config.WHITE)

    def draw_back_card(self, x: int, y: int) -> None:
        CardImages().draw_card_back(x, y, self.screen)

    # @param hand_list needs to hold Card() objects
    # loops through CardImage().draw_card to blit card to screen
    def draw_hand_cards(self, hand_list: List[Card]) -> None:
        if hand_list == self.the_dealer.hand and self.need_back:
            self.draw_back_card(*self.the_dealer.get_x_y())
            self.card_images.draw_card(self.screen, hand_list[1])
        else:
            for card in hand_list:
                self.card_images.draw_card(self.screen, card)

    def event_handler_on_click(self) -> None:
        for gbtn in self.btn_imgs:
            if gbtn.check_collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                gbtn.click()
        for cbtn in self.chip_btn_images:
            if cbtn.check_collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                cbtn.click()

    def event_handler_right_click(self) -> None:
        for cbtn in self.chip_btn_images:
            if cbtn.check_collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.player_bet.remove_chip(cbtn.value)

    def reset_buttons(self) -> None:
        for gbtn in self.btn_imgs:
            gbtn.reset_image()
        for cbtn in self.chip_btn_images:
            cbtn.reset_image()
