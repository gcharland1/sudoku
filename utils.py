import pygame

class Button:
    FONT_COLOR = (10, 10, 10)
    FONT_SIZE = 18
    pygame.font.init()
    font = pygame.font.SysFont('Arial Black', FONT_SIZE)


    COLOR1 = (200, 30, 200)
    COLOR2 = (180, 25, 180)
    
    BORDER = 10
     
    def __init__(self, x0, y0, w, h, rounded=False, text='Button'):
        self.rounded = rounded
        self.text = text
        
        self.x0 = x0
        self.x1 = x0 + w
        self.w = w

        self.y0 = y0
        self.y1 = y0 + h
        self.h = h
        
        self.color = Button.COLOR1
        
        self.out_rect = pygame.Rect(x0, y0, w, h)
    
    
    def draw(self, surf):
        if self.rounded:
            pygame.draw.rect(surf, self.color, self.out_rect, border_radius= int(0.2*min(self.out_rect.size)))
        else:
            pygame.draw.rect(surf, self.color, self.out_rect) 
        
        text_center = (self.x0 + self.w/2, self.y0 + self.h/2)
        text_surf = Button.font.render(self.text, True, Button.FONT_COLOR)
        text_rect = text_surf.get_rect(center=text_center) 
        surf.blit(text_surf, text_rect) 


    def on_click(self):
        if self.color == Button.COLOR1:
            self.color = Button.COLOR2
        else:
            self.color = Button.COLOR1


class Menu:
    BG_COLOR = (0, 0, 0)
    BUTTON_SIZE = 50

    def __init__(self, x0, y0, w, h):
        self.x0 = x0
        self.x1 = x0 + w
        self.w = w
        
        self.y0 = y0
        self.y1 = y0 + h
        self.h = h

        self.rect = pygame.Rect(self.x0, self.y0, self.w, self.h)
        self.buttons = []

        self.SPACING = 0.05 # 5% button width between each button
        self.BUTTON_SIZE = int(self.w/(3 * (1 + self.SPACING)))
        self.gen_num_buttons()
        self.gen_indices_buttons()

    def gen_num_buttons(self):
        w = h = self.BUTTON_SIZE
        x0 = self.x0
        y0 = self.y0 + int((self.h/2 - 3*(1+self.SPACING)*self.BUTTON_SIZE)/2)
        
        self.num_buttons = []
        for i in range(0, 9):
            x = x0 + i%3*(1 + self.SPACING)*self.BUTTON_SIZE
            y = y0 + i//3*(1 + self.SPACING)*self.BUTTON_SIZE
            button = Button(x, y, w, h, rounded=True, text=str(i + 1))
            self.num_buttons.append(button)
            self.buttons.append(button)


    def gen_indices_buttons(self):
        w = h = self.BUTTON_SIZE
        x0 = self.x0
        y0 = int(self.h/2) + int((self.h/2 - 3*(1+self.SPACING)*self.BUTTON_SIZE)/2)
        
        self.ind_buttons = []
        for i in range(0, 9):
            x = x0 + i%3*(1 + self.SPACING)*self.BUTTON_SIZE
            y = y0 + i//3*(1 + self.SPACING)*self.BUTTON_SIZE
            button = Button(x, y, w, h, rounded=True, text=str(i + 1))
            self.ind_buttons.append(button)
            self.buttons.append(button)

    def render(self, surf):
        pygame.draw.rect(surf, Menu.BG_COLOR, self.rect)
        for b in self.buttons:
            b.draw(surf)
         
