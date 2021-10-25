#The purpose of this file is to act as the  driver for the pygame functions. 
#Essentially this will be where pygame is programmed and the other file will be where the chess 
#functions will be called.

import pygame, sys, time, math, copy, chess, os
from pprint import pprint # TODO: remove this on final

#These are varoables representing colors Brown and White for pygame applications. 
Brown = (139, 69, 19)
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

        self.user_clicks = 0 # 0 = nothing selected, 1 = something selected
        self.select = { 'piece': -1, 'y': -1, 'x': -1 }
        self.target = { 'y': -1, 'x': -1 }

        self.valid_moves = self.game.get_valid_moves()
        print(self.valid_moves)
    
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

        # updates the pygame screen.
        pygame.display.update()
        
        # Creates an object to keep track of time taken.
        
        self.clock = pygame.time.Clock()
        #This function should set up the peices and be used to make changes to the pieces.

    def draw_board(self):
          for x in range(8):
            for y in range(8):
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
        for x in range(8):
            for y in range(8):
                piece = self.game.board[y][x]
                if piece != 0:
                    self.surface.blit(IMAGES[piece], pygame.Rect(x*squareSize, y*squareSize, squareSize, squareSize))

    def key_pressed_down_event(self, event):
        self.keyboard_commands(event)

    def key_let_go_event(self, event):
        pass

    def handle_mousedown(self, event):
        select_x, select_y = pygame.mouse.get_pos()
        select_x = math.floor(select_x / 100)
        select_y = math.floor(select_y / 100)
        piece = self.game.board[select_y][select_x]

        print( (select_y, select_x) )

        # Checking if the user is just selecting a piece to move
        if self.user_clicks == 0:
            
            # Ensure player 1 selected white
            if ((self.game.player == 1 and 1 <= piece <= 6) or 
                (self.game.player == 2 and 11 <= piece <= 16)):
                    self.select['piece'] = piece
                    self.select['y'] = select_y
                    self.select['x'] = select_x
                    self.user_clicks = 1

        # Checks when user has already selected a piece
        elif self.user_clicks == 1:
            # if player still selects their piece, set that piece as new selected
            if ((self.game.player == 1 and 1 <= piece <= 6) or 
                (self.game.player == 2 and 11 <= piece <= 16)):
                    self.select['piece'] = piece
                    self.select['y'] = select_y
                    self.select['x'] = select_x
                    self.user_clicks = 1
            else:
                self.target['y'] = select_y
                self.target['x'] = select_x
                
                move = ( (self.select['y'], self.select['x']), 
                         (select_y, select_x) )

                # check if select-target combo is in available moves
                """ if self.game.is_valid_move( self.select, self.target ):
                    self.game.make_move( self.select, self.target )
                    self.user_clicks = 2 """
                
                if move in self.valid_moves:
                    self.game.make_move( self.select, self.target )
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
    
    #This function promotes the pawn 
    def draw_pawnPromotion(self, player):
        second_surface = pygame.Surface([displayWidth//1.5, displayHeight//2])
        second_surface.fill((105,105,105))
        second_surface_rect = second_surface.get_rect(center = (displayWidth//2, displayHeight//2))
        self.surface.blit(second_surface, second_surface_rect)

        font = pygame.font.SysFont('Helvetica', 36)
        txt = font.render('Choose Pawn To Promote To:', True, (0,0,0))
        ktext = font.render(("Knight"), True, (0,0,0))
        rtext = font.render(("Rook"), True, (0,0,0))
        btext = font.render(("Bishop"), True, (0,0,0))
        qtext = font.render(("Queen"), True, (0,0,0))

        txt_rect = txt.get_rect(center = (displayWidth//2, displayHeight //32 + displayHeight//4))
        self.surface.blit(txt, txt_rect)

        ktext_rect = ktext.get_rect(center = (displayWidth//4 + displayWidth//16, displayHeight//2 + displayHeight//8))
        self.surface.blit(ktext, ktext_rect)

        rtext_rect = rtext.get_rect(center = (displayWidth//4 + displayWidth//16 + displayWidth//8, displayHeight//2 + displayHeight//8))
        self.surface.blit(rtext, rtext_rect)

        btext_rect = btext.get_rect(center = (displayWidth//2 + displayWidth//16, displayHeight//2 + displayHeight//8))
        self.surface.blit(btext, btext_rect)

        qtext_rect = ktext.get_rect(center = (displayWidth//2 + displayWidth//16 + displayWidth//8, displayHeight//2 + displayHeight//8))
        self.surface.blit(qtext, qtext_rect)

        #load either white or black pawns depending on player 
        if player == 1:
            knight = IMAGES[2]
            rook   = IMAGES[3]
            bishop = IMAGES[4]
            queen  = IMAGES[5]
        elif player == 2:
            knight = IMAGES[12]
            rook   = IMAGES[13]
            bishop = IMAGES[14]
            queen  = IMAGES[15]

        button1 = pygame.Rect(displayWidth//4, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
        button2 = pygame.Rect(displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
        button3 = pygame.Rect(displayWidth//4 + displayWidth//4, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
        button4 = pygame.Rect(displayWidth//4 + displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
        pygame.draw.rect(self.surface, [105,105,105], button1)
        pygame.draw.rect(self.surface, [105,105,105], button2)
        pygame.draw.rect(self.surface, [105,105,105], button3)
        pygame.draw.rect(self.surface, [105,105,105], button4)

        #knight button
        k = knight
        k_rect = k.get_rect(center = (displayWidth//4 + displayWidth//16, displayHeight//2.5))
        self.surface.blit(k, k_rect)
        
        #rook button
        r = rook
        r_rect = r.get_rect(center = (displayWidth//4 + squareSize + displayWidth//16, displayHeight//2.5))
        self.surface.blit(r, r_rect)

        #bishop button
        b = bishop
        b_rect = b.get_rect(center = (displayWidth//4 + 2*squareSize + displayWidth//16, displayHeight//2.5))
        self.surface.blit(b, b_rect)

        #queen button
        q = queen
        q_rect = q.get_rect(center = (displayWidth//4 + 3*squareSize + displayWidth//16, displayHeight//2.5))
        self.surface.blit(q, q_rect)

        pygame.display.update()
        run = True
        while run:
            mouse_pos = pygame.mouse.get_pos()
            click1 = False
            action1 = False

            click2 = False
            action2 = False

            click3 = False
            action3 = False

            click4 = False
            action4 = False

            pygame.draw.rect(self.surface, [105,105,105], button1)
            pygame.draw.rect(self.surface, [105,105,105], button2)
            pygame.draw.rect(self.surface, [105,105,105], button3)
            pygame.draw.rect(self.surface, [105,105,105], button4)
            self.surface.blit(k, k_rect)
            self.surface.blit(r, r_rect)
            self.surface.blit(b, b_rect)
            self.surface.blit(q, q_rect)

            for event in pygame.event.get():
                #mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    quit()
                    
                if button1.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button1)
                    self.surface.blit(k, k_rect)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click1 = True
                        action1 = True
                    elif pygame.mouse.get_pressed()[0] == 0:
                        click1 = False

                    if action1 == True:
                        run = False

                elif button2.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button2)
                    self.surface.blit(r, r_rect)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click2 = True
                        action2 = True
                    elif pygame.mouse.get_pressed()[0] == 0:
                        click2 = False

                    if action2 == True:
                        run = False

                elif button3.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button3)
                    self.surface.blit(b, b_rect)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click3 = True
                        action3 = True
                    elif pygame.mouse.get_pressed()[0] == 0:
                        click3 = False

                    if action3 == True:
                        run = False

                elif button4.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button3)
                    self.surface.blit(q, q_rect)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click4 = True
                        action4 = True
                    elif pygame.mouse.get_pressed()[0] == 0:
                        click4 = False

                    if action4 == True:
                        run = False
                
                pygame.display.update()

                if click1 == True:
                    if player == 1:
                        return 2
                    elif player == 2:
                        return 12

                if click2 == True:
                    if player == 1:
                        return 3
                    elif player == 2:
                        return 13

                if click3 == True:
                    if player == 1:
                        return 4
                    elif player == 2:
                        return 14

                if click4 == True:
                    if player == 1:
                        return 5
                    elif player == 2:
                        return 15

    #This function checks if there is a pawn has reached the opposite side
    #If it has, it returns true. Else false
    def isPawnPromotion(self, y, x):
        print('hi')
        if(self.game.player == 1):
            if(self.select['piece'] == 1 and y == 0):
                print('y')
                return True

        elif (self.game.player == 2):
            if(self.select['piece'] == 11 and y == 7):
                print('y')
                return True
                
        return False

    # This function starts up the game and sets all the parameters of said game.
    # Not much now but more can be added later
    def start_game(self):
        self.ai = None
        self.setUp()
        
        # This is the main loop the game will run through until it ends or gets restarted.
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
          
            # if user clicks is 2 then we know some sort of board state occured. Now we have to update the board.
            if (self.user_clicks == 2):

                #Checks if the player can validly make a pawn promotion
                if(self.isPawnPromotion(self.target['y'], self.target['x'])):
                    #update the board to show that the pawn moved to edge of board
                    self.draw_board()
                    self.drawPieces()
                    pygame.display.update()
                    
                    #set piece to promotion choice
                    self.game.board[ self.target['y']] [self.target['x']] = self.draw_pawnPromotion(self.game.player)

                    #make pygame wait for user
                    evemt = pygame.event.wait()
                    pygame.display.update()

                #now we need to reset everything.
                if (self.game.player == 1):
                    self.game.player = 2
                elif (self.game.player == 2):
                    self.game.player = 1

                self.user_clicks = 0
                self.select = { 'piece': -1, 'y': -1, 'x': -1 }
                self.target = { 'y': -1, 'x': -1 }
                self.valid_moves.clear()

                self.draw_board()
                self.drawPieces()
                pygame.display.update()

                self.valid_moves = self.game.get_valid_moves()
                pprint(self.valid_moves)

                # print(self.game.board) debug purposes                 
    
            self.clock.tick(60)

        quit()