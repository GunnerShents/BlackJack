import buttons 
import pygame
import config
from os import path, listdir 

#class Chip()
#constructor (self, chip_value, img)
#class betting()

class Chip():
    
    def __init__ (self, chip_value, img, x, y ):
        self.chip_value = chip_value
        self.image = img
        self.x = x
        self.y = y
        self.chip_number = 0 
    
    def draw_chip(self, area):
        area.blit(self.image,(self.x, self.y))
    
    def get_chip_value(self):    
        return self.chip_value
    
class Betting():
    
    def __init__ (self):
        
        self.betting_total = 0
        self.chips = {}
        self.bets_placed = []
        #self.all_images = buttons.generate_images()
    
    def draw_total_bet(self, area):
        for chip in self.bets_placed:
            chip.draw_chip(area)
            
    def get_total(self):
        return self.betting_total

    def create_chip(self, value, image):
        x = 100
        y = 500
        y_increase = -6
        num = self.get_position()+1  
        new_chip = Chip(value, image, x, y+(y_increase*num))
        self.bets_placed.append(new_chip)
        self.show_chips()
        
    def check_stack(self, value):
        for chip in self.bets_placed:
            if chip.chip_value == value:
                return True
            else:
                return False
    
    def remove_chip(self, value):
        for 
        
    def show_chips(self):
        for chip in self.bets_placed:
            print(chip.chip_value)
        
    def get_position(self):
        return len(self.bets_placed)
        
    def remove_from_total(self, chip_key: Chip):
        if self.chips[chip_key].remove_chip():
            self.betting_total -= self.chips[chip_key].get_chip_value() 
        
bet = Betting()
