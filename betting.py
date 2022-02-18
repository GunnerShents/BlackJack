import buttons 
import pygame
import config
from os import path, listdir 

#class Chip()
#constructor (self, chip_value, img)
#class betting()

class Chip():
    
    def __init__ (self, chip_value, img, x=0, y=0):
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
        
        self.total = 0
        self.bets_placed = []

    def reset(self):
        self.total = 0
        self.bets_placed = []
    
    def draw_total_bet(self, area):
        if len(self.bets_placed) > 0:
            chip_x = 100
            chip_y = 550
            for chip in self.bets_placed:
                chip.x = chip_x
                chip.y = chip_y
                chip.draw_chip(area)
                chip_y -= 4
            
    def get_total(self):
        return self.total

    def create_chip(self, value, image):    
        new_chip = Chip(value, image)
        self.bets_placed.append(new_chip)
        self.total += value
        print (self.get_total())

    def check_stack(self, value):
        return any(chip.chip_value == value for chip in self.bets_placed)
    
    def remove_chip(self, value):
        if self.check_stack(value):
            for chip in reversed(self.bets_placed):
                if chip.chip_value == value:
                    self.total -= chip.chip_value
                    self.bets_placed.remove(chip)
                    break
        print(self.get_total())
  
        
         
    
