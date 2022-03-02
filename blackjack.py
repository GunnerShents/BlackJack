import random
import sys
from os import path
#from typing import List, Tuple
import pygame
import config
from theGame import MainGame
#from betting import Betting
#from buttons import Chip_button, Game_button, generate_images
#from cardclasses import Card, CardImages, Deck_holder
#from char import Character, Dealer, Player
#from seat import Seat
# random.seed()

seed = random.randrange(sys.maxsize)
random.seed()

def main() -> None:
    pygame.init()

    screen: pygame.surface.Surface = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Black Jack")
    clock = pygame.time.Clock()
    config.IMG_DIR = path.join(path.dirname(__file__), "images")

    #player = Player("Phil", 500, config.WIDTH//2-(config.CARD_WIDTH), config.HEIGHT//14*10)
    #game = TheGame(screen, player)
    #player.show_cards()
    #print(player.get_total())
    #print("")
    #game.the_dealer.show_cards()
    #print(game.the_dealer.get_total())
    
    #Loading the main game
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
                print (pygame.mouse.get_pos())
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
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
