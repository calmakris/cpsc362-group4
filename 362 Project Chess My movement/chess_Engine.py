#The purpose of this file is to act as the  driver for the pygame functions. 
#Essentially this will be where pygame is programmed and the other file will be where the chess 
#functions will be called.

import pygame, sys, time, math, copy, chess, os

#These are varoables representing colors Brown and White for pygame applications. 
Brown = (139,69,19)
WHITE = (255, 255, 255)
RED = (255,0,0)
YELLOW = (255,255,0)
displayWidth = 800
displayHeight = 900
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
        
        self.selected_piece = -1
        self.selected_square = ()
        self.target_square = ()
        self.user_clicks = 0

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

        pygame.draw.rect(self.surface,RED,pygame.Rect(800,100,100,800))
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render("player 1: " + str(self.game.point_counter(0,self.game.player1))+" player 2: "+str(self.game.point_counter(0,self.game.player2)), True, YELLOW)
        self.surface.blit(text,(90,820))
        self.load_Images()
        self.drawPieces()

       #updates the pygame screen.
        pygame.display.update()

        

         # Creates an object to keep track of time taken.
        
        self.clock = pygame.time.Clock()
        #This function should set up the peices and be used to make changes to the pieces.
    
    def draw_board(self):
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

    #This is handling movement of pieces.
    def handle_mousedown(self, event):
        
        select_x, select_y = pygame.mouse.get_pos()
        select_x = math.floor(select_x / 100)
        select_y = math.floor(select_y / 100)    
        pos = (select_x, select_y)
        print(pos)

        #checking if the user is just selecting a piece to move
        if self.user_clicks == 0:

            #This is needed to make sure the saved selected piece is actually the player's piece  
            if self.game.player == 1:
                if self.game.board[select_y][select_x] >= 1 and self.game.board[select_y][select_x] <= 6:
                    self.selected_square = (select_x, select_y)
                    self.selected_piece = self.game.board[select_y][select_x]
                    self.user_clicks = 1
                    available_moves = self.game.get_available_moves(self.selected_piece, self.selected_square[0], self.selected_square[1])
                    for index, tuple in enumerate(available_moves):
                        #change this to color in the board
                        print(tuple)
                        pygame.draw.rect(self.surface, RED, pygame.Rect(tuple[1] * squareSize , tuple[0]* squareSize , squareSize , squareSize ))
                        self.drawPieces()
                        pygame.display.update()
            
            #This is the same as above but for player 2.
            elif self.game.player == 2:
                if self.game.board[select_y][select_x] >= 11 and self.game.board[select_y][select_x] <= 16:
                    self.selected_square = (select_x, select_y)
                    self.selected_piece = self.game.board[select_y][select_x]
                    self.user_clicks = 1
                    available_moves = self.game.get_available_moves(self.selected_piece, self.selected_square[0], self.selected_square[1])
                    for index, tuple in enumerate(available_moves):
                        #change this to color in the board
                        pygame.draw.rect(self.surface, YELLOW, pygame.Rect(tuple[1] * squareSize , tuple[0]* squareSize , squareSize , squareSize ))
                        self.drawPieces()
                        pygame.display.update()

            #Not needed      
            else:
                if self.game.board[select_y][select_x] >= 11 and self.game.board[select_y][select_x] <= 16:
                    self.selected_square = (select_x, select_y)
                    self.selected_piece = self.game.board[select_y][select_x]
                    self.user_clicks = 1

        
        #this covers selecting a space to move the selected piece to.        
        elif self.user_clicks == 1:
            
            #player one
            if self.game.player == 1:
                 #If the player selects another piece he owns then set that piece to selected
                if self.game.board[select_y][select_x] >= 1 and self.game.board[select_y][select_x] <= 6:
                    self.selected_square = (select_x, select_y)
                    self.selected_piece = self.game.board[select_y][select_x]
                    self.user_clicks = 1
                    #Player 1 selects another piece so we generated the moves for that piece
                    print("Generate player 1 piece moves")
                    available_moves = self.game.get_available_moves(self.selected_piece, self.selected_square[0], self.selected_square[1])
                    self.draw_board()
                    for index, tuple in enumerate(available_moves):
                        #change this to color in the board
                        pygame.draw.rect(self.surface, RED, pygame.Rect(tuple[1] * squareSize , tuple[0]* squareSize , squareSize , squareSize ))
                        self.drawPieces()
                        pygame.display.update()
               
                #if its a piece he does not own then get all the available moves that the selected piece can make and check to see if the target space is valid. If it is then the player commits to the move.
                else:
                    self.target_square = (select_y, select_x)
                   
                    available_moves = self.game.get_available_moves(self.selected_piece, self.selected_square[0], self.selected_square[1])
                    print(len(available_moves))
                    print(available_moves)
                    for index, tuple in enumerate(available_moves):
                        #Player 1 does not select another piece
                        pygame.draw.rect(self.surface, RED, pygame.Rect(tuple[1] * squareSize , tuple[0]* squareSize , squareSize , squareSize ))
                        self.drawPieces()
                    for x in available_moves:
                        if x == self.target_square:
                            self.game.make_move(self.selected_square[0], self.selected_square[1], select_x, select_y, self.selected_piece)
                            self.user_clicks = 2
            #player 2
            elif self.game.player == 2:
                #If the player selects another piece he owns then set that piece to selected
                if self.game.board[select_y][select_x] >= 11 and self.game.board[select_y][select_x] <= 16:
                    self.selected_square = (select_x, select_y)
                    self.selected_piece = self.game.board[select_y][select_x]
                    self.user_clicks = 1
                    #Player 2 selected another pieces so we change the color of the rectangle here
                    available_moves = self.game.get_available_moves(self.selected_piece, self.selected_square[0], self.selected_square[1])
                    self.draw_board()
                    for index, tuple in enumerate(available_moves):
                        #change this to color in the board
                        pygame.draw.rect(self.surface, YELLOW, pygame.Rect(tuple[1] * squareSize , tuple[0]* squareSize , squareSize , squareSize ))
                        self.drawPieces()
                        pygame.display.update()
                #if its a piece he does not own then get all the available moves that the selected piece can make and check to see if the target space is valid. If it is then the player commits to the move.
                else:
                    self.target_square = (select_y, select_x)
                   
                    available_moves = self.game.get_available_moves(self.selected_piece, self.selected_square[0], self.selected_square[1])
                    print(len(available_moves))
                    print(available_moves)
                    print("Generate player 2 piece moves")
                    for index, tuple in enumerate(available_moves):
                        #change this to color in the board
                        pygame.draw.rect(self.surface, YELLOW, pygame.Rect(tuple[1] * squareSize , tuple[0]* squareSize , squareSize , squareSize ))
                        self.drawPieces()
                        pygame.display.update()
                    for x in available_moves:
                        if x == self.target_square:
                            self.game.make_move(self.selected_square[0], self.selected_square[1], select_x, select_y, self.selected_piece)
                            self.user_clicks = 2

                                        

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

    def pawnPromotion(self, player):
        if player == 2:
            print('12: Knight')
            print('13: Rook')
            print('14: Bishop')
            print('15: Queen')
            piece = int(input('Choose a piece to promote your pawn to: '))
            return piece
        if player == 1:
            print('2: Knight')
            print('3: Rook')
            print('4: Bishop')
            print('5: Queen')
            piece = int(input('Choose a piece to promote your pawn to: '))
            return piece

    #This function checks if there is a pawn has reached the opposite side
    #If it has, it returns true. Else false
    def isPawnPromotion(self):
        #scan the board
        #self.game.board
        for y in range(0,8):
            for x in range(0,8):
                piece = self.game.board[y][x] 
                #check if pawn is white (1) and has reached the opposite side
                if piece == 1 and y == 0:
                    return True
                #check if pawn is black (11) and has reached the opposite side
                elif piece == 11 and y == 7:
                    return True
        return False
    
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

                elif pygame.mouse.get_pressed()[0]:
                    self.handle_mousedown(event)
                else:
                    pass
            
            #if user clicks is 2 then we know some sort of board state occured. Now we have to update the board.
            if (self.user_clicks == 2):

                #Checks if the player can validly make a pawn promotion
                if(self.isPawnPromotion()):
                    #update the board to show that the pawn moved to edge of board
                    self.draw_board()
                    self.drawPieces()
                    pygame.display.update()
                    #set pawn to player's selected piece
                    self.game.board[self.target_square[0]][self.target_square[1]] = self.pawnPromotion(self.game.player)
                    #this is to make pygame wait for user input.
                    evemt = pygame.event.wait()
                    pygame.display.update()

                #now we need to reset everything.
                if (self.game.player == 1):
                    self.game.player = 2
                elif (self.game.player == 2):
                    self.game.player = 1
                self.user_clicks = 0
                self.selected_piece = -1
                self.selected_square = ()
                self.target_square = ()
                self.draw_board()
                self.drawPieces()
                pygame.display.update()

               # print(self.game.board) debug purposes                 

    
            self.clock.tick(60)
        quit()
        
        



        