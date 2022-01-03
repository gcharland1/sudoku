import pygame

class Menu:
    def __init__(self, surf):
        self._display_surf = surf

    def display_menu(self):
        self._display_surf.fill((0, 0, 0))
        pygame.display.flip() 
        if input('Press any key to continue: '):
            pass
