import sudoku 
import solver
import pygame
import time
import menu
import utils

class App:
    NUM_KEYS = [pygame.K_0,
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
                pygame.K_6,
                pygame.K_7,
                pygame.K_8,
                pygame.K_9]

    BG_COLOR = (255, 238, 230)
    INPUT_COLOR = (200, 200, 0)
    FONT_COLOR = (51, 8, 0) 
    USER_FONT_COLOR = (255, 100, 0)
     
    FONT_SIZE = 40
 
    SIZE = WIDTH, HEIGHT = (800, 600)
    SQUARE_SIZE = SQ_WIDTH, SQ_HEIGHT = (FONT_SIZE + 10, FONT_SIZE + 10)
    GRID_THICKNESS = 1
    
    FPS = 15 

    def __init__(self):
        self.running = True
        self.update = True
        self._display_surf = None
        self.original_board = None

    def on_execute(self):
        pygame.init()
        if self.on_init() == False:
            self.running = False
        
        while self.running:
            for event in pygame.event.get():
                self.on_event(event) 
            if time.time() - self.tic > 1/App.FPS:
                self.on_render()
                self.tic = time.time()
         
        self.on_cleanup()

    def on_init(self):
        self._display_surf = pygame.display.set_mode(self.SIZE)
        self.font = pygame.font.SysFont('Arial Black', self.FONT_SIZE)
        
        self.Y0 = int((App.HEIGHT - (9*App.SQ_HEIGHT + (9-1)*App.GRID_THICKNESS))/2)
        self.Y1 = int((App.HEIGHT + (9*App.SQ_HEIGHT + (9-1)*App.GRID_THICKNESS))/2)
        self.Y_INC = App.SQ_HEIGHT + App.GRID_THICKNESS
        
        self.X0 = int((App.WIDTH - (9*App.SQ_WIDTH + (9-1)*App.GRID_THICKNESS))/2)
        self.X1 = int((App.WIDTH + (9*App.SQ_WIDTH + (9-1)*App.GRID_THICKNESS))/2)
        self.X_INC = App.SQ_WIDTH + App.GRID_THICKNESS
        
        self.sudoku = sudoku.Sudoku()
        self.new_board()
        
        self.menu = utils.Menu(self.X1 + 10, 0, self.WIDTH - self.X1, self.HEIGHT)
        
        self.tic = time.time()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.KEYUP:
            if event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_q:
                    self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            #for button in self.buttons:
            #    if x >= button.x0 and x <= button.x1 and y >= button.y0 and y <= button.y1:
            #        button.on_click()

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            xi, yi = self.get_index(pos)
            if xi in range(9) and yi in range(9):
                if not self.original_board[xi, yi]:
                    self.fill_number(pygame.mouse.get_pos())
            else:
                x, y = pygame.mouse.get_pos()
                #for button in self.buttons:
                #    if x >= button.x0 and x <= button.x1 and y >= button.y0 and y <= button.y1:
                #        button.on_click()


    def on_cleanup(self):
        pygame.display.quit()
        pygame.quit()

    def on_render(self):
        self._display_surf.fill(self.BG_COLOR)
        self.display_grid()
        self.fill_board()
        self.menu.render(self._display_surf)
        #for button in self.buttons:
        #    button.draw(self._display_surf)

        pygame.display.flip()

    def get_index(self, pos):
        x, y = pos
        xi = (x - self.X0)//self.SQ_WIDTH
        yi = (y - self.Y0)//self.SQ_HEIGHT
        if xi in range(9) and yi in range(9):
            return (xi, yi)
        else:
            return (None, None)

    def get_square(self, pos):
        x, y = pos
        x0  = self.X0 + (self.SQ_WIDTH + self.GRID_THICKNESS)*((x - self.X0)//self.SQ_WIDTH)
        y0  = self.Y0 + (self.SQ_HEIGHT + self.GRID_THICKNESS)*((y - self.Y0)//self.SQ_HEIGHT)
        
        if not (y0 < self.Y0 or x0 < self.X0 or y0 + self.SQ_HEIGHT > self.Y1 or x0 + self.SQ_WIDTH > self.X1):
            rect = pygame.Rect(x0, y0, self.SQ_HEIGHT, self.SQ_WIDTH)
        else:
            rect = pygame.Rect(0, 0, 0, 0) 
        return rect

    def display_grid(self):
        x_counter = 0
        
        for x in range(self.X0 + self.SQ_WIDTH, self.X1, self.X_INC):
            v0 = (x, self.Y0)
            v1 = (x, self.Y1)
            if x_counter in [2, 5]:
                pygame.draw.line(self._display_surf, (0, 0, 0), v0, v1, 3*self.GRID_THICKNESS)
            else:
                pygame.draw.line(self._display_surf, (0, 0, 0), v0, v1, self.GRID_THICKNESS)
            x_counter += 1
        
        y_counter = 0
        for y in range(self.Y0 + self.SQ_HEIGHT, self.Y1, self.Y_INC):
            h0 = (self.X0, y)
            h1 = (self.X1, y)
            if y_counter in [2, 5]:
                pygame.draw.line(self._display_surf, (0, 0, 0), h0, h1, 3*self.GRID_THICKNESS)
            else:
                pygame.draw.line(self._display_surf, (0, 0, 0), h0, h1, self.GRID_THICKNESS)
            y_counter += 1

    def fill_board(self):
        for x in range(9):
            for y in range(9):
                n = str(self.sudoku.board[x, y])
                if n == '0':
                    n = ''

                text_center = (self.X0 + (x+0.5)*(self.SQ_WIDTH+self.GRID_THICKNESS), self.Y0 + (y+0.5)*(self.SQ_HEIGHT+self.GRID_THICKNESS))
                if self.original_board[x, y]:
                    text = self.font.render(n, True, App.FONT_COLOR)
                else:
                    text = self.font.render(n, True, App.USER_FONT_COLOR)
                text_rect = text.get_rect(center=text_center)
                self._display_surf.blit(text, text_rect) 

    def draw_outline(self, rect, color=(0,0,0), t=5):
        x1, y1 = (rect.topleft[0] + t, rect.topleft[1] + t)
        w = rect.width - 2*t
        h = rect.height - 2*t
        rect2 = pygame.Rect(x1, y1, w, h)
        
        pygame.draw.rect(self._display_surf, color, rect)
        pygame.draw.rect(self._display_surf, App.BG_COLOR, rect2)
        pygame.display.flip()

    def fill_number(self, pos):
        rect = self.get_square(pos)
        self.draw_outline(rect, color=App.INPUT_COLOR, t=5*App.GRID_THICKNESS)
        
        xi, yi = self.get_index(pos)
        
        return_to_events = False
        user_input = True
        input_value = None
        
        while user_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        user_input = False
                    elif event.key == pygame.K_DELETE:
                        self.sudoku.board[xi, yi] = 0
                        user_input = False
                    elif event.key in App.NUM_KEYS:
                        self.sudoku.board[xi, yi] = int(event.unicode)
                        user_input = False
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.update = True
                    user_input = False
                    return_to_events = event 
        self.update = True
        
        if return_to_events:
            self.on_render()
            self.on_event(return_to_events)           

    def new_board(self):
        self.sudoku.generateBoard()
        self.sudoku.removeNumbers()
        self.original_board = self.sudoku.board != 0 


if __name__ == '__main__':
    app = App()
    app.on_execute()
