

#class Chip()
#constructor (self, chip_value, img)
#class betting()

class Chips():
    
    def __init__ (self, chip_value, img, x, y ):
        self.chip_value = chip_value
        self.image = img
        self.x = x
        self.y = y
        self.chip_number = 0 
    
    #draw method()
    
    def add_chip(self):
        self.chip_number += 1
    
    def remove_chip(self):    
        if self.chip_number > 0:
            self.chip_number -= 1 
            return True
            
    def get_num_chips(self):
        
        return self.chip_number
    
    def get_chip_value(self):
        
        return self.chip_value
    
class Betting():
    
    def __ini__ (self):
        self.betting_total = 0
        self.chips = {}
    
    #create the chip objects
    
    def get_total(self):
        
        return self.betting_total

    def add_to_total(self, chip_key: Chips):
        
        chip_key.add_chip()
        self.betting_total += self.chips[chip_key].get_chip_value() 
        
    def remove_from_total(self, chip_key: Chips):
        
        if self.chips[chip_key].remove_chip():
            self.betting_total -= self.chips[chip_key].get_chip_value() 
        
