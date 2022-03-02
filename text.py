import pygame
#from char import Player


class Text:
    
    def __init__(self):
        
        self.font_name = pygame.font.match_font('californianfb')
        self.balance_pos = {1: (40,430), 2 : (655,535), 3 : (1050,430)}
        
    def drawText(
            self, 
            surf:pygame.surface.Surface, 
            text:str, 
            size:int, 
            coords:tuple[int,int], 
            colour:tuple[int,int,int]):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (coords)
        surf.blit(text_surface, text_rect)
        
    def player_coords(self, pos:int) -> tuple[int,int]:
         return self.balance_pos[pos]
     
    
        
     
        
        
