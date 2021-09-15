#The purpose of this file is to act as the  driver for the pygame functions. 
#Essentially this will be where pygame is programmed and the other file will be where the chess 
#functions will be called.

import pygame, sys, time, math, copy, chess, os

#These are varoables representing colors Brown and White for pygame applications. 
Brown = (139,69,19)
WHITE = (255, 255, 255)
displayWidth = 800
displayHeight = 800
squareSize = 100
IMAGES = {}

#This calls pygame to exit the program.
def quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

#This class contains all the functions for the chess board having to do with pygame.
class Chess_Board(object):

    #python constructor for the Chess_Board class.
    def __init__(self):
        self.keys_pressed_down = list()
        self.game = chess.Chess() #Note not set up yet
        #self.ai = None            Not applicable yet
    
    def setUp(self):
        #imports all available pygame modules
        pygame.init()
        pygame.display.set_caption('Chess')
        #Sets the parameter on how big the pygame screen will be
        self.surface = pygame.display.set_mode((displayWidth,displayHeight))

        for x in range(0,8):
            for y in range(0,8):
                if(y % 2 == 0 and x %2 == 0):
                    pygame.draw.rect(self.surface, WHITE, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                    
                elif(y % 2 == 0 and x %2 == 1):
                    pygame.draw.rect(self.surface, Brown, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 1):
                    pygame.draw.rect(self.surface, WHITE, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 0):
                    pygame.draw.rect(self.surface, Brown, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))

       
        self.load_Images()
        self.drawPieces()

       #updates the pygame screen.
        pygame.display.update()

        

         # Creates an object to keep track of time taken.
        
        self.clock = pygame.time.Clock()
        #This function should set up the peices and be used to make changes to the pieces.
        #self.draw_board()
    def load_Images(self):
        pieces = [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16]
        for piece in pieces:
           IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), 'images', str(piece) + '.png')).convert_alpha(), (squareSize, squareSize))
    def drawPieces(self):
        self.game.board
        for x in range(0,8):
            for y in range(0,8):
                piece = self.game.board[y][x]
                if piece != 0:
                    self.surface.blit(IMAGES[piece], pygame.Rect(x*squareSize, y*squareSize, squareSize, squareSize))

    def key_pressed_down_event(self, event):
        self.keyboard_commands(event)

    def key_let_go_event(self, event):
        pass

    def handle_mousedown(self, event):
        pass 
        #This event tracks the position where the user clicks the mouse
    def handle_mouseup(self, event):
        pass
        #This can be used to get the position where the user stopped clicking the mouse
    
    def handle_mousemove(self, event):
        pass 
        #Will be used when implementing animated piece movement.
    
    def keyboard_commands(self, event):
        if event.key == pygame.K_q and pygame.key.get_mods() and pygame.KMOD_CTRL:
            quit()
            sys.exit()
        # This function can be used to add more key commands later down the line.
    
    def new_game(self):
        self.game.__init__() #resets the entire game 
    
    #This function starts up the game and sets all the parameters of said game.
    #Not much now but more can be added later
    def start_game(self):
        self.ai = None
        self.setUp()
        
        #This is the main loop the game will run through until it ends or gets restarted.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.key_pressed_down_event(event)
                elif event.type == pygame.KEYUP:
                    self.key_let_go_event(event)
                else:
                    pass

    
            self.clock.tick(60)
        quit()
        
        



        