import config
from char import Player 
#This class will create: 
#Player object / balance
#Game buttons
#Chip buttons
#----------------------------
# class seat()
    #create player, balance, seat position
    #holds a dictionary with the centre x,y 
    
class Seat():
    """
    Creates a player for the seated postion at the table, 
    all the player settings are configured with the x, y values
    held in the dictionary.
    """
    
    def __init__(self, seat_position:int, name:str, bal:int):
        
        self.seat_coords:dict[int,tuple[int,int]] = {1 : (config.WIDTH//20*2,config.HEIGHT//10*6), 
                                 2: (config.WIDTH//20*2,config.HEIGHT//10*7), 
                                 3: (config.WIDTH//20*2,config.HEIGHT//10*6)
                                 }

                
    def create_player(self, name:str, pos:int, bal:int):
        player = Player(name, bal, 
                    self.seat_coords[pos][0], 
                    self.seat_coords[pos][1])

        return player

    
