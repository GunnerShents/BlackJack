import pygame
import config
from os import path



#----------------------------------------------------------------

def generate_button_images():
    # load images
    btn_dict = {
        "bet_up":pygame.image.load(path.join(config.IMG_DIR,"bet_btn_up.png")).convert_alpha(), 
        "bet_down":pygame.image.load(path.join(config.IMG_DIR,"bet_btn_down.png")).convert_alpha(),
        "deal_up":pygame.image.load(path.join(config.IMG_DIR,"deal_btn_up.png")).convert_alpha(),
        "deal_down":pygame.image.load(path.join(config.IMG_DIR,"deal_btn_down.png")).convert_alpha(),
        "hit_up":pygame.image.load(path.join(config.IMG_DIR,"hit_btn_up.png")).convert_alpha(),
        "hit_down":pygame.image.load(path.join(config.IMG_DIR,"hit_btn_down.png")).convert_alpha(),
        "stand_up":pygame.image.load(path.join(config.IMG_DIR,"stand_btn_up.png")).convert_alpha(),
        "stand_down":pygame.image.load(path.join(config.IMG_DIR,"stand_btn_down.png")).convert_alpha(),
        "stand_down":pygame.image.load(path.join(config.IMG_DIR,"stand_btn_down.png")).convert_alpha(),
        "hit_grey":pygame.image.load(path.join(config.IMG_DIR,"hit_grey1.png")).convert_alpha(),
        "deal_grey":pygame.image.load(path.join(config.IMG_DIR,"deal_grey1.png")).convert_alpha(),
        "stand_grey":pygame.image.load(path.join(config.IMG_DIR,"stand_grey1.png")).convert_alpha(),
        "bet_grey":pygame.image.load(path.join(config.IMG_DIR,"bet_grey1.png")).convert_alpha(),
   
   }
    #loop scales each image value
    for btn in btn_dict.keys():
        btn_dict[btn] = pygame.transform.scale(btn_dict[btn],(config.BUTTON_WIDTH, config.BUTTON_HEIGHT))

    return btn_dict

class Buttons():

    def __init__ (self, on_click, grey_image, button_up_img, button_down_img, x ,y, active=True):
        assert callable(on_click)
        self.on_click = on_click
        self.image = [button_up_img, button_down_img, grey_image]
        self.index = 0
        self.rect = self.image[self.index].get_rect()
        self.rect.x = x
        self.rect.y = y
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










