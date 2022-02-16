import pygame
import config
from os import path, listdir 

#----------------------------------------------------------------
def generate_images():
    btn_dict = {}
    for file in listdir(config.IMG_DIR):
        f = path.join(config.IMG_DIR, file)
        if path.isfile(f):
            btn_dict[file[:-4]] = pygame.image.load(f).convert_alpha()
        
    #loop scales each image value
    for btn in btn_dict.keys():
        if btn[:5] == "chip_":
            btn_dict[btn] = pygame.transform.scale(btn_dict[btn],((config.BUTTON_WIDTH/5)*3, (config.BUTTON_HEIGHT/5)*3))
        else:
           btn_dict[btn] = pygame.transform.scale(btn_dict[btn],(config.BUTTON_WIDTH, config.BUTTON_HEIGHT))
    return btn_dict           


class Buttons():

    def __init__ (self, on_click, grey_image, button_up_img, button_down_img, x ,y, active=True):
        assert callable(on_click)
        self.on_click = on_click
        self.image = [button_up_img, button_down_img, grey_image]
        self.index = 0
        self.rect = self.image[self.index].get_rect(x=x, y=y)
        # self.rect.x = x
        # self.rect.y = y
        self.active = active
        self.image_change = False
        self.grey_img = grey_image
        if not self.active:
            self.index = 2
    
    def click(self):
        if self.get_active():
            self.on_click()
    
    def set_active(self, bool:bool):
        self.active = bool
            
    def get_active(self):
        return self.active
    
    def draw_button (self, area):
        area.blit(self.image[self.index], (self.rect))
      
    def set_index(self,num):
        self.index = num
        
    #x, y are the mouse x, y co_ords
    def check_collide (self, x, y):
        if self.rect.collidepoint(x, y):
            if self.get_active():
                self.set_index(1)
                return True
    
    def reset_image(self):
        if self.get_active():
            self.set_index(0)
        else:
            self.set_index(2)
            

class Chip_button():
    
    def __init__ (self, on_click, button_up_img, button_down_img, x ,y, value):
        
        self.on_click = on_click
        self.image = [button_up_img, button_down_img]
        self.index = 0
        self.rect = self.image[self.index].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = value
    
    def click(self):
        self.on_click()
    
    def draw_button (self, area):
        
        area.blit(self.image[self.index], (self.rect))
        
    #x, y are the mouse x, y co_ords
    def check_collide (self, x, y):
        if self.rect.collidepoint(x, y):
            self.index = 1
            return True
    
    def reset_image(self):
        self.index = 0
            











