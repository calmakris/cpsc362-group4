#The purpose of this file is to act as the  driver for the pygame functions. 
#Essentially this will be where pygame is programmed and the other file will be where the chess 
#functions will be called.

import pygame, sys, time, math, copy, chess, os
from pprint import pprint # TODO: remove this on final

#These are varoables representing colors Brown and White for pygame applications. 
available_moves_tf = True
undo_moves_tf = True
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
PURPLE = (106, 90, 205)
BLUE = (28, 155, 188)
GREEN = (60, 179, 113)
RED = (255,0,0)
square1color = WHITE
square2color = BROWN
displayWidth = 800
displayHeight = 800
squareSize = displayHeight//8
COVERIMAGES = {}
IMAGES = {}
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pack = 'images/Originals'

#This calls pygame to exit the program.
def quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

#This class contains all the functions for the chess board having to do with pygame.
class Chess_Board(object):

    #python constructor for the Chess_Board class.
    def __init__(self):
        self.surface = pygame.display.set_mode((displayWidth,displayHeight))
        self.keys_pressed_down = list()
        self.game = chess.Chess() #Note not set up yet

        self.user_clicks = 0 # 0 = nothing selected, 1 = something selected
        self.select = { 'piece': -1, 'y': -1, 'x': -1 }
        self.target = { 'piece': -1, 'y': -1, 'x': -1 }
        self.prev_move = 0
        self.buttonclick = pygame.mixer.Sound('buttonClick.wav')
        self.movesound = pygame.mixer.Sound('ChessClick.wav')
        self.valid_moves = self.game.get_valid_moves()
        print(self.valid_moves)
    
    def setUp(self):
        #imports all available pygame modules
        
        pygame.display.set_caption('Chess')
        #Sets the parameter on how big the pygame screen will be
        

        for x in range(0,8):
            for y in range(0,8):
                if(y % 2 == 0 and x %2 == 0):
                    pygame.draw.rect(self.surface, square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                elif(y % 2 == 0 and x %2 == 1):
                    pygame.draw.rect(self.surface, square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                elif (y %2 == 1 and x%2 == 1):
                    pygame.draw.rect(self.surface, square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 0):
                    pygame.draw.rect(self.surface, square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
    
        self.load_Images(pack)
        self.drawPieces()

        # updates the pygame screen.
        pygame.display.update()
        
        # Creates an object to keep track of time taken.
        
        self.clock = pygame.time.Clock()
        #This function should set up the peices and be used to make changes to the pieces.

    def draw_board(self, square1color, square2color):
          for x in range(8):
            for y in range(8):
                if(y % 2 == 0 and x %2 == 0):
                    pygame.draw.rect(self.surface, square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                    
                elif(y % 2 == 0 and x %2 == 1):
                    pygame.draw.rect(self.surface, square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 1):
                    pygame.draw.rect(self.surface, square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 0):
                    pygame.draw.rect(self.surface, square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        #textrect.topleft = (x, y)
        textrect.center = (displayWidth//2, y+displayWidth//16)
        surface.blit(textobj, textrect)
    
    def main_Menu(self):
        
        resolution = (displayWidth, displayHeight)
        screen = pygame.display.set_mode(resolution)
        font = pygame.font.SysFont(None, displayHeight//4)
        button_font = pygame.font.SysFont(None, displayHeight//11)
        self.backgroundmusic()
        while True:
            screen.fill((0,0,0))

            self.draw_text('Main Menu', font, (255, 255, 255), screen, displayWidth//20, displayHeight//20)

            mx, my = pygame.mouse.get_pos()

            button1 = pygame.Rect(displayWidth//4, displayHeight//4, displayWidth/2,  displayHeight/8)
            button2 = pygame.Rect(displayWidth//4, displayHeight//2, displayWidth//2, displayHeight//8)

            pygame.draw.rect(screen, (255, 255, 255), button1)
            self.draw_text('Player vs Player', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//4)
            pygame.draw.rect(screen, (255, 255, 255), button2)
            self.draw_text('Exit', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//2)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button1.collidepoint((mx, my)):
                        self.buttonclick.play()
                        self.draw_board(square1color, square2color)
                        self.drawPieces()
                        pygame.display.update()
                        return None
                    elif button2.collidepoint((mx, my)):
                        self.buttonclick.play()
                        quit()

            pygame.display.update()


    def Pause_Screen(self):
        
        self.surface.fill((0,0,105))
        
        text1 = "Pause Menu:"
        font = pygame.font.SysFont('Helvetica', 36, 1, 0)
        text1 = font.render(text1, 1, (255, 215, 0))
        text_rect1 = text1.get_rect(center = (displayWidth// 2, displayHeight // 8))
        self.surface.blit(text1, text_rect1)

        
        
        button  = pygame.Rect(displayWidth//4, displayHeight//4, displayWidth/2,  displayHeight/8)
        button2 = pygame.Rect(displayWidth//4, displayHeight//2, displayWidth//2, displayHeight//8)
        button3 = pygame.Rect(displayWidth//4, displayHeight - displayHeight//4, displayWidth//2, displayHeight//8)
        pygame.draw.rect(self.surface, [211,211,211], button)
        pygame.draw.rect(self.surface, [211,211,211], button2)
        pygame.draw.rect(self.surface, [211,211,211], button3)

        text2 = "Continue"
        font = pygame.font.SysFont('Helvetica', 36, 1, 0)
        text2 = font.render(text2, 1, (0,0,0))
        text_rect2 = text2.get_rect(center = (displayWidth// 2, displayHeight // 4 + displayHeight//16))
        self.surface.blit(text2, text_rect2)

        text3 = "Options"
        font  = pygame.font.SysFont('Helvetica', 36, 1, 0)
        text3 = font.render(text3, 1, (0,0,0))
        text_rect3 = text3.get_rect(center = (displayWidth// 2, displayHeight // 2 + displayHeight//16))
        self.surface.blit(text3, text_rect3)


        text4 = "Quit Game"
        font  = pygame.font.SysFont('Helvetica', 36, 1, 0)
        text4 = font.render(text4, 1, (0,0,0))
        text_rect4 = text4.get_rect(center = (displayWidth// 2, displayHeight - displayHeight//4 + displayHeight//16))
        self.surface.blit(text4, text_rect4)

        
        
        while True:

            pygame.draw.rect(self.surface, [211,211,211], button)
            pygame.draw.rect(self.surface, [211,211,211], button2)
            pygame.draw.rect(self.surface, [211,211,211], button3)
            self.surface.blit(text2, text_rect2)
            self.surface.blit(text4, text_rect4)
            self.surface.blit(text3, text_rect3)

            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    quit()
                if button.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button)
                    self.surface.blit(text2, text_rect2)
                if button2.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button2)
                    self.surface.blit(text3, text_rect3)
                if button3.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, [255,255,255], button3)
                    self.surface.blit(text4, text_rect4)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and pygame.key.get_mods() and pygame.KMOD_CTRL:
                        self.draw_board(square1color, square2color)
                        self.drawPieces()
                        pygame.display.update()
                        return None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if button.collidepoint(mouse_pos):
                       self.buttonclick.play()
                       self.draw_board(square1color, square2color)
                       self.drawPieces()
                       pygame.display.update()
                       return None
                    elif button2.collidepoint(mouse_pos):
                       self.buttonclick.play()
                       self.Options_screen()
                       return None
                       
                    elif button3.collidepoint(mouse_pos):
                        self.buttonclick.play()
                        quit()
                
                
               
                pygame.display.update()
    """brenda's added stuff"""
    def changeStyles(self):
        imgOptionsurface = pygame.Surface([displayWidth, displayHeight])
        imgOptionsurface.fill((105,105,105))
        imgOptionsurface_rect = imgOptionsurface.get_rect(center = (displayWidth//2, displayHeight//2))
        self.surface.blit(imgOptionsurface, imgOptionsurface_rect)

        button1 = pygame.Rect(displayWidth//10, displayHeight//4, displayWidth//8, displayHeight//8)                           
        button2 = pygame.Rect(2*displayWidth//10 + displayWidth//8, displayHeight//4, displayWidth//8, displayHeight//8)
        button3 = pygame.Rect(3*displayWidth//10 + 2*displayWidth//8, displayHeight//4, displayWidth//8, displayHeight//8)
        button4 = pygame.Rect(4*displayWidth//10 + 3*displayWidth//8, displayHeight//4, displayWidth//8, displayHeight//8)
        
        button5 = pygame.Rect(displayWidth//10, displayHeight//1.6, displayWidth//8, displayHeight//8)
        button6 = pygame.Rect(2*displayWidth//10 + displayWidth//8, displayHeight//1.6, displayWidth//8, displayHeight//8)
        button7 = pygame.Rect(3*displayWidth//10 + 2*displayWidth//8, displayHeight//1.6, displayWidth//8, displayHeight//8)
        button8 = pygame.Rect(4*displayWidth//10 + 3*displayWidth//8, displayHeight//1.6, displayWidth//8, displayHeight//8)

        pygame.draw.rect(self.surface, [105,105,105], button1)
        pygame.draw.rect(self.surface, [105,105,105], button2)
        pygame.draw.rect(self.surface, [105,105,105], button3)
        pygame.draw.rect(self.surface, [105,105,105], button4)
        pygame.draw.rect(self.surface, [105,105,105], button5)
        pygame.draw.rect(self.surface, [105,105,105], button6)
        pygame.draw.rect(self.surface, [105,105,105], button7)
        pygame.draw.rect(self.surface, [105,105,105], button8)

        image1 = COVERIMAGES[1]
        image2 = COVERIMAGES[2]
        image3 = COVERIMAGES[3]
        image4 = COVERIMAGES[4]
        image5 = COVERIMAGES[5]
        image6 = COVERIMAGES[6]
        image7 = COVERIMAGES[7]
        image8 = COVERIMAGES[8]
        self.surface.blit(image1, button1)
        self.surface.blit(image2, button2)
        self.surface.blit(image3, button3)
        self.surface.blit(image4, button4)
        self.surface.blit(image5, button5)
        self.surface.blit(image6, button6)
        self.surface.blit(image7, button7)
        self.surface.blit(image8, button8)

        titlefont = pygame.font.SysFont('Helvetica', 40)
        font = pygame.font.SysFont('Helvetica', 18)
        text = titlefont.render("Customize Your Board", True, (0,0,0))
        
        ptext = titlefont.render("Piece Sets", True, (0,0,0))
        text1 = font.render("Original Set", True, (0,0,0))
        text2 = font.render("Gold & Silver Set", True, (0,0,0))
        text3 = font.render("Super Mario Bros Set", True, (0,0,0))
        text4 = font.render("Star Wars Set", True, (0,0,0))
        
        ctext = titlefont.render("Board Colors", True, (0,0,0))
        text5 = font.render("White / Brown", True, (0,0,0))
        text6 = font.render("White / Purple", True, (0,0,0))
        text7 = font.render("White / Blue", True, (0,0,0))
        text8 = font.render("White / Green", True, (0,0,0))

        text_rect = text.get_rect(center = (displayWidth//2.16, displayHeight//20))
        self.surface.blit(text, text_rect)

        ptext_rect = text.get_rect(center =(displayWidth//4, displayHeight//6.4))
        self.surface.blit(ptext, ptext_rect)

        text1_rect = text1.get_rect(center = (displayWidth//8 + displayWidth//26.6, displayHeight//2.5))
        self.surface.blit(text1, text1_rect)

        text2_rect = text2.get_rect(center = (2*displayWidth//8 + displayWidth//80 + displayWidth//8, displayHeight//2.5))
        self.surface.blit(text2, text2_rect)

        text3_rect = text3.get_rect(center = (displayWidth//2 + displayWidth//9, displayHeight//2.5))
        self.surface.blit(text3, text3_rect)

        text4_rect = text4.get_rect(center = (displayWidth//2 + 2*displayWidth//8 + displayWidth//11, displayHeight//2.5))
        self.surface.blit(text4, text4_rect)
        
        ctext_rect = ctext.get_rect(center = (displayWidth//6.8, displayHeight//2 + displayHeight//20))
        self.surface.blit(ctext, ctext_rect)
        
        text5_rect = text5.get_rect(center = (displayWidth//8 + displayWidth//26.6, displayHeight//2 + 2*displayHeight//8 + displayHeight//32))
        self.surface.blit(text5, text5_rect)
        
        text6_rect = text6.get_rect(center = (2*displayWidth//8 + displayWidth//80 + displayWidth//8, displayHeight//2 + 2*displayHeight//8 + displayHeight//32))
        self.surface.blit(text6, text6_rect)
        
        text7_rect = text7.get_rect(center = (displayWidth//2 + displayWidth//9, displayHeight//2 + 2*displayHeight//8 + displayHeight//32))
        self.surface.blit(text7, text7_rect)
        
        text8_rect = text8.get_rect(center = (displayWidth//2 + 2*displayWidth//8 + displayWidth//11, displayHeight//2 + 2*displayHeight//8 + displayHeight//32))
        self.surface.blit(text8, text8_rect)
        
        print("this runs")
        run = True
        pos2 = (0,0)
        
        while run == True:
            for event in pygame.event.get():
                pos2 = pygame.mouse.get_pos()
            
            print(pos2)
            click1 = False
            action1 = False
            if button1.collidepoint(pos2):
                print('hover')
                pygame.draw.rect(self.surface, [255,255,255], button1)
                self.surface.blit(text1, text1_rect)
                self.surface.blit(image1, button1)
                if pygame.mouse.get_pressed()[0] == 1:
                    click1 = True
                    action1 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button1)
                self.surface.blit(text1, text1_rect)
                self.surface.blit(image1, button1)
            if pygame.mouse.get_pressed()[0] == 0:
                    click1 = False
            if action1 == True:
                    run = False
            
            click2 = False
            action2 = False
            if button2.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button2)
                self.surface.blit(text2, text2_rect)
                self.surface.blit(image2, button2)
                if pygame.mouse.get_pressed()[0] == 1:
                    click2 = True
                    action2 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button2)
                self.surface.blit(text2, text2_rect)
                self.surface.blit(image2, button2)
            if pygame.mouse.get_pressed()[0] == 0:
                click2 = False
            if action2 == True:
                run = False

            click3 = False
            action3 = False
            if button3.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button3)
                self.surface.blit(text3, text3_rect)
                self.surface.blit(image3, button3)
                if pygame.mouse.get_pressed()[0] == 1:
                    click3 = True
                    action3 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button3)
                self.surface.blit(text3, text3_rect)
                self.surface.blit(image3, button3)
            if pygame.mouse.get_pressed()[0] == 0:
                click3 = False
            if action3 == True:
                run = False

            click4 = False
            action4 = False
            if button4.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button4)
                self.surface.blit(text4, text4_rect)
                self.surface.blit(image4, button4)
                if pygame.mouse.get_pressed()[0] == 1:
                    click4 = True
                    action4 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button4)
                self.surface.blit(text4, text4_rect)
                self.surface.blit(image4, button4)
            if pygame.mouse.get_pressed()[0] == 0:
                click4 = False
            if action4 == True:
                run = False
                
            click5 = False
            action5 = False
            if button5.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button5)
                self.surface.blit(text5, text5_rect)
                self.surface.blit(image5, button5)
                if pygame.mouse.get_pressed()[0] == 1:
                    click5 = True
                    action5 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button5)
                self.surface.blit(text5, text5_rect)
                self.surface.blit(image5, button5)
            if pygame.mouse.get_pressed()[0] == 0:
                click5 = False
            if action5 == True:
                run = False
                
            click6 = False
            action6 = False
            if button6.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button6)
                self.surface.blit(text6, text6_rect)
                self.surface.blit(image6, button6)
                if pygame.mouse.get_pressed()[0] == 1:
                    click4 = True
                    action4 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button6)
                self.surface.blit(text6, text6_rect)
                self.surface.blit(image6, button6)
            if pygame.mouse.get_pressed()[0] == 0:
                click6 = False
            if action6 == True:
                run = False
                
            click7 = False
            action7 = False
            if button7.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button7)
                self.surface.blit(text7, text7_rect)
                self.surface.blit(image7, button7)
                if pygame.mouse.get_pressed()[0] == 1:
                    click7 = True
                    action7 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button7)
                self.surface.blit(text7, text7_rect)
                self.surface.blit(image7, button7)
            if pygame.mouse.get_pressed()[0] == 0:
                click7 = False
            if action7 == True:
                run = False
                
            click8 = False
            action8 = False
            if button8.collidepoint(pos2):
                pygame.draw.rect(self.surface, [255,255,255], button8)
                self.surface.blit(text8, text8_rect)
                self.surface.blit(image8, button8)
                if pygame.mouse.get_pressed()[0] == 1:
                    click8 = True
                    action8 = True
            else:
                pygame.draw.rect(self.surface, [105,105,105], button8)
                self.surface.blit(text8, text8_rect)
                self.surface.blit(image8, button8)
            if pygame.mouse.get_pressed()[0] == 0:
                click8 = False
            if action8 == True:
                run = False
            
            pygame.display.update()
        
        if click1 == True:
            self.buttonclick.play()
            return 11
        elif click2 == True:
            self.buttonclick.play()
            return 2
        elif click3 == True:
            self.buttonclick.play()
            return 3
        elif click4 == True:
            self.buttonclick.play()
            return 4
        elif click5 == True:
            self.buttonclick.play()
            return 5
        elif click6 == True:
            self.buttonclick.play()
            return 6
        elif click7 == True:
            self.buttonclick.play()
            return 7
        elif click8 == True:
            self.buttonclick.play()
            return 8
        
        


    def Options_screen(self):
        global available_moves_tf
        global undo_moves_tf
        resolution = (displayWidth, displayHeight)
        screen = pygame.display.set_mode(resolution)
        font = pygame.font.SysFont(None, displayHeight//4)
        button_font = pygame.font.SysFont(None, displayHeight//11)

        while True:
            screen.fill((0,0,0))
            self.draw_text('Options', font, (255, 255, 255), screen, displayWidth//20, displayHeight//22)
            mx, my = pygame.mouse.get_pos()

            option1 = pygame.Rect(displayWidth//4, displayHeight//4.5, displayWidth/2,  displayHeight/8)
            option2 = pygame.Rect(displayWidth//4, displayHeight//2.25, displayWidth//2, displayHeight//8)
            option3 = pygame.Rect(displayWidth//4, displayHeight//1.5, displayWidth//2, displayHeight//8)

            if available_moves_tf:
                pygame.draw.rect(screen, (255, 255, 255), option1)
                self.draw_text('Highlight Moves', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//4.5)
            elif available_moves_tf is False:
                pygame.draw.rect(screen, (255, 0, 0), option1)
                self.draw_text('Highlight Moves', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//4.5)
            if undo_moves_tf:
                pygame.draw.rect(screen, (255, 255, 255), option2)
                self.draw_text('Undo Moves', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//2.25)
            elif undo_moves_tf is False:
                pygame.draw.rect(screen, (255, 0, 0), option2)
                self.draw_text('Undo Moves', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//2.25)
            pygame.draw.rect(screen, (255, 255, 255), option3)
            self.draw_text('Styles', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//1.5)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.Pause_Screen()
                        return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if option1.collidepoint((mx, my)):
                        self.buttonclick.play()
                        if available_moves_tf:
                            available_moves_tf = False
                        elif available_moves_tf == False:
                            available_moves_tf = True
                        pygame.display.update()
                    elif option2.collidepoint((mx, my)):
                        self.buttonclick.play()
                        if undo_moves_tf:
                            undo_moves_tf = False
                        elif undo_moves_tf == False:
                            undo_moves_tf = True
                        pygame.display.update()
                    elif option3.collidepoint((mx, my)):
                        self.buttonclick.play()
                        imgpack = self.changeStyles()
                        if imgpack == 11:
                            pack = 'images/Originals'
                            self.load_Images(pack)
                        elif imgpack == 2:
                            pack = 'images/Gold-Silver'
                            self.load_Images(pack)
                        elif imgpack == 3:
                            pack = 'images/Super Mario Bros'
                            self.load_Images(pack)
                        elif imgpack == 4:
                            pack = 'images/Star Wars'
                            self.load_Images(pack)
                        elif imgpack == 5:
                            square1color = WHITE
                            square2color = BROWN
                            self.draw_board(square1color, square2color)
                        elif imgpack == 6:
                            square1color = WHITE
                            square2color = PURPLE
                            self.draw_board(square1color, square2color)
                        elif imgpack == 7:
                            square1color = WHITE
                            square2color = BLUE
                            self.draw_board(square1color, square2color)
                        elif imgpack == 8:
                            square1color = WHITE
                            square2color = GREEN
                            self.draw_board(square1color, square2color)
                        
                        
                #elif option1.collidepoint((mx, my)):
                    #pygame.draw.rect(screen, (255, 0, 0), option1)
                    #self.draw_text('Highlight Moves: On', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//4)

            pygame.display.update()
            

    
    
    
    """end of stuff"""

    def end_screen(self, piece):
        second_surface = pygame.Surface([displayWidth//2,displayHeight//2])
        second_surface.fill((105,105,105))
        second_surface_rect = second_surface.get_rect(center = (displayWidth//2, displayHeight//2))
        self.surface.blit(second_surface, second_surface_rect)


        font = pygame.font.SysFont('Helvetica' , 36)
        font2 = pygame.font.SysFont('Helvetica', 36)
        if piece == 6:
            winner = "Black Wins!!!"
        if piece == 16:
            winner = "White Wins!!!"
        if piece == -1:
            winner = "Draw"
        startprompt = font2.render("Game Over, " + winner, True, (255, 215, 0)) #title font
        startprompt_rect = startprompt.get_rect(center = (displayWidth//2  , displayHeight//4 + displayHeight//8))
        self.surface.blit(startprompt, startprompt_rect)

        button1b = pygame.Rect(displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//6, displayWidth//4, displayHeight//16) # Replay button

        button2b = pygame.Rect(displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//3, displayWidth//4, displayHeight//16) # exit button
        pygame.draw.rect(self.surface, [211,211,211], button1b)
        pygame.draw.rect(self.surface, [211,211,211], button2b)

        restart1 = font.render("Replay" , True, (0,0,0))
        restart1_rect = restart1.get_rect(center = (displayWidth//2, displayHeight//4 +  displayHeight//5))
        self.surface.blit(restart1, restart1_rect)

        quit1 = font.render("Quit", True, (0,0,0))
        quit1_rect = quit1.get_rect(center = (displayWidth// 2, displayHeight//2 + displayHeight//8.5))
        self.surface.blit(quit1, quit1_rect)
        run = True
        while run:
            pos = pygame.mouse.get_pos()
            click1 = False
            action1 = False
            if button1b.collidepoint(pos):
                pygame.draw.rect(self.surface, [255,255,255], button1b)
                self.surface.blit(restart1, restart1_rect)
                if pygame.mouse.get_pressed()[0] == 1:   
                    click1 = True
                    action1 = True
                    print('CLICKED')
            else:
                pygame.draw.rect(self.surface, [211,211,211], button1b)
                self.surface.blit(restart1, restart1_rect)
            if pygame.mouse.get_pressed()[0] == 0:
                click1 = False
            if action1:
                run = False
                #print('replay')
            
            click2 = False
            action2 = False
            if button2b.collidepoint(pos):
                pygame.draw.rect(self.surface, [255,255,255], button2b)
                self.surface.blit(quit1, quit1_rect)
                if pygame.mouse.get_pressed()[0] == 1:
                    click2 = True
                    action2 = True
                    print('CLICKED')
            else:
                pygame.draw.rect(self.surface, [211,211,211], button2b)
                self.surface.blit(quit1, quit1_rect)
            if pygame.mouse.get_pressed()[0] == 0:
                click2 = False
            if action2:
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        if click2 == True:
            self.buttonclick.play()
            quit()
        if click1 == True:
            self.buttonclick.play()
            self.__init__()
            self.start_game()


        
    def load_Images(self, imgpack):
        pieces = [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16]
        for piece in pieces:
           IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), imgpack, str(piece) + '.png')).convert_alpha(), (squareSize, squareSize))
        covers = [1,2,3,4,5,6,7,8]
        for cover in covers:
            COVERIMAGES[cover] = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), 'coverImages', str(cover) + '.png')).convert_alpha(), (squareSize, squareSize))
    
    def drawPieces(self):
        self.game.board
        for x in range(8):
            for y in range(8):
                piece = self.game.board[y][x]
                if piece != 0 and (x,y) != (self.select['x'], self.select['y']):
                    self.surface.blit(IMAGES[piece], pygame.Rect(x*squareSize, y*squareSize, squareSize, squareSize))

    def key_pressed_down_event(self, event):
        self.keyboard_commands(event)

    def key_let_go_event(self, event):
        pass

    def handle_mousedown(self, event):
        select_x, select_y = pygame.mouse.get_pos()
        select_x = math.floor(select_x / squareSize)
        select_y = math.floor(select_y / squareSize)
        piece = self.game.board[select_y][select_x]

        print( (select_y, select_x) )

        # Checking if the user is just selecting a piece to move
        if self.user_clicks == 0:
            
            # Ensure players select their corresponding piece
            if ((self.game.player == 1 and 1 <= piece <= 6) or 
                (self.game.player == 2 and 11 <= piece <= 16)):
                    self.select['piece'] = piece
                    self.select['y'] = select_y
                    self.select['x'] = select_x
                    self.user_clicks = 1
                    #new stuff
                    
                    


        # Checks when user has already selected a piece
        elif self.user_clicks == 1:
            
            #if the player selects the tile with the selected piece let it go.
            if (select_x == self.select['x'] and select_y == self.select['y']):
                self.game.board[select_y][select_x] = self.select['piece']
                self.select['piece'] = -1
                self.select['y'] = -1
                self.select['x'] = -1
                self.user_clicks = 0
                self.draw_board(square1color, square2color)
                self.drawPieces()
                pygame.display.update()
            
            # if player still selects their piece, set that piece as new selected
            elif ((self.game.player == 1 and 1 <= piece <= 6) or 
                (self.game.player == 2 and 11 <= piece <= 16)):
                    self.select['piece'] = piece
                    self.select['y'] = select_y
                    self.select['x'] = select_x
                    self.user_clicks = 1
                    self.draw_board(square1color, square2color)
                    self.drawPieces()
                    pygame.display.update()
            else:
                self.target['piece'] = piece
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
                    print("Black King Moved!")
                    self.prev_move += 1
                    self.user_clicks = 2
                    self.movesound.play()
                

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
        
        elif event.key == pygame.K_ESCAPE and pygame.key.get_mods() and pygame.KMOD_CTRL:
            self.Pause_Screen()
        
        elif event.key == pygame.K_n and pygame.key.get_mods() and pygame.KMOD_CTRL:
            self.__init__()
            self.start_game()

        elif event.key == pygame.K_z and pygame.key.get_mods() and pygame.KMOD_CTRL and self.prev_move > 0:
            # CTRL + Z undos the move
            # TODO: consider castling
            self.game.undo_move( )
            self.prev_move -= 1
            self.user_clicks = 2
        # This function can be used to add more key commands later down the line.
    
    def new_game(self):
        self.game.__init__() #resets the entire game 

    
    #This function promotes the pawn 
    def pawnPromotion(self, player):
        if player == 2:
            second_surface = pygame.Surface([displayWidth//1.5, displayHeight//2])
            second_surface.fill((105,105,105))
            second_surface_rect = second_surface.get_rect(center = (displayWidth//2, displayHeight//2))
            self.surface.blit(second_surface, second_surface_rect)   
            
            button12 = pygame.Rect(displayWidth//4 , displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8) # Replay button
            button13 = pygame.Rect(displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
            button14 = pygame.Rect(displayWidth//4 + displayWidth//4, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
            button15 = pygame.Rect(displayWidth//4 + displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
            pygame.draw.rect(self.surface, [105,105,105], button12)
            pygame.draw.rect(self.surface, [105,105,105], button13)
            pygame.draw.rect(self.surface, [105,105,105], button14)
            pygame.draw.rect(self.surface, [105,105,105], button15)
            image12 = IMAGES[12]
            image13 = IMAGES[13]
            image14 = IMAGES[14]
            image15 = IMAGES[15]
            self.surface.blit(image12, button12)
            self.surface.blit(image13, button13)
            self.surface.blit(image14, button14)
            self.surface.blit(image15, button15) 
            titlefont = pygame.font.SysFont('Helvetica', 36)
            font = pygame.font.SysFont('Helvetica', 28)
            text = titlefont.render("Choose Piece to Promote to!", True, (0,0,0))
            text12 = font.render("Knight", True, (0,0,0))
            text13 = font.render("Rook", True, (0,0,0))
            text14 = font.render("Bishop", True, (0,0,0))
            text15 = font.render("Queen", True, (0,0,0))
            text_rect = text.get_rect(center = (displayWidth//2, displayHeight//32 + displayHeight//4))
            self.surface.blit(text, text_rect)
            text12_rect = text12.get_rect(center = (displayWidth//4 + displayWidth//16, displayHeight//2 + displayHeight//8))
            self.surface.blit(text12, text12_rect)
            text13_rect = text13.get_rect(center = (displayWidth//4 + displayWidth//16 + displayWidth//8, displayHeight//2 + displayHeight//8))
            self.surface.blit(text13, text13_rect)
            text14_rect = text14.get_rect(center = (displayWidth//2 + displayWidth//16, displayHeight//2 + displayHeight//8))
            self.surface.blit(text14, text14_rect)
            text15_rect = text15.get_rect(center = (displayWidth//2 + displayWidth//16 + displayWidth//8, displayHeight//2 + displayHeight//8))
            self.surface.blit(text15, text15_rect)

            run = True
            while run:
                pos = pygame.mouse.get_pos()
                click12 = False
                action12 = False
                if button12.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button12)
                    self.surface.blit(text12, text12_rect)
                    self.surface.blit(image12, button12)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click12 = True
                        action12 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button12)
                    self.surface.blit(text12, text12_rect)
                    self.surface.blit(image12, button12)
                if pygame.mouse.get_pressed()[0] == 0:
                    click12 = False
                if action12 == True:
                    run = False
                
                click13 = False
                action13 = False
                if button13.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button13)
                    self.surface.blit(text13, text13_rect)
                    self.surface.blit(image13, button13)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click13 = True
                        action13 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button13)
                    self.surface.blit(text13, text13_rect)
                    self.surface.blit(image13, button13)
                if pygame.mouse.get_pressed()[0] == 0:
                    click13 = False
                if action13 == True:
                    run = False
                
                click14 = False
                action14 = False
                if button14.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button14)
                    self.surface.blit(text14, text14_rect)
                    self.surface.blit(image14, button14)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click14 = True
                        action14 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button14)
                    self.surface.blit(text14, text14_rect)
                    self.surface.blit(image14, button14)
                if pygame.mouse.get_pressed()[0] == 0:
                    click14 = False
                if action14 == True:
                    run = False
                
                click15 = False
                action15 = False
                if button15.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button15)
                    self.surface.blit(text15, text15_rect)
                    self.surface.blit(image15, button15)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click15 = True
                        action15 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button15)
                    self.surface.blit(text15, text15_rect)
                    self.surface.blit(image15, button15)
                if pygame.mouse.get_pressed()[0] == 0:
                    click15 = False
                if action15 == True:
                    run = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                pygame.display.update()
            if click12 == True:
                self.buttonclick.play()
                return 12
            if click13 == True:
                self.buttonclick.play()
                return 13
            if click14 == True:
                self.buttonclick.play()
                return 14
            if click15 == True:
                self.buttonclick.play()
                return 15
            
        if player == 1:
            second_surface = pygame.Surface([displayWidth//1.5, displayHeight//2])
            second_surface.fill((105,105,105))
            second_surface_rect = second_surface.get_rect(center = (displayWidth//2, displayHeight//2))
            self.surface.blit(second_surface, second_surface_rect)   
            
            button2 = pygame.Rect(displayWidth//4 , displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8) # Replay button
            button3 = pygame.Rect(displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
            button4 = pygame.Rect(displayWidth//4 + displayWidth//4, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
            button5 = pygame.Rect(displayWidth//4 + displayWidth//4 + displayWidth//8, displayHeight//4 + displayHeight//16, displayWidth//8, displayHeight//4 + displayHeight//8)
            pygame.draw.rect(self.surface, [105,105,105], button2)
            pygame.draw.rect(self.surface, [105,105,105], button3)
            pygame.draw.rect(self.surface, [105,105,105], button4)
            pygame.draw.rect(self.surface, [105,105,105], button5)
            image2 = IMAGES[2]
            image3 = IMAGES[3]
            image4 = IMAGES[4]
            image5 = IMAGES[5]
            self.surface.blit(image2, button2)
            self.surface.blit(image3, button3)
            self.surface.blit(image4, button4)
            self.surface.blit(image5, button5) 
            font = pygame.font.SysFont('Helvetica', 36)
            text = font.render("Choose Piece to Promote to!", True, (0,0,0))
            text2 = font.render("Knight", True, (0,0,0))
            text3 = font.render("Rook", True, (0,0,0))
            text4 = font.render("Bishop", True, (0,0,0))
            text5 = font.render("Queen", True, (0,0,0))
            text_rect = text.get_rect(center = (displayWidth//2, displayHeight//32 + displayHeight//4))
            self.surface.blit(text, text_rect)
            text2_rect = text2.get_rect(center = (displayWidth//4 + displayWidth//16, displayHeight//2 + displayHeight//8))
            self.surface.blit(text2, text2_rect)
            text3_rect = text3.get_rect(center = (displayWidth//4 + displayWidth//16 + displayWidth//8, displayHeight//2 + displayHeight//8))
            self.surface.blit(text3, text3_rect)
            text4_rect = text4.get_rect(center = (displayWidth//2 + displayWidth//16, displayHeight//2 + displayHeight//8))
            self.surface.blit(text4, text4_rect)
            text5_rect = text5.get_rect(center = (displayWidth//2 + displayWidth//16 + displayWidth//8, displayHeight//2 + displayHeight//8))
            self.surface.blit(text5, text5_rect)

            run = True
            while run:
                pos = pygame.mouse.get_pos()
                click2 = False
                action2 = False
                if button2.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button2)
                    self.surface.blit(text2, text2_rect)
                    self.surface.blit(image2, button2)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click2 = True
                        action2 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button2)
                    self.surface.blit(text2, text2_rect)
                    self.surface.blit(image2, button2)
                if pygame.mouse.get_pressed()[0] == 0:
                    click2 = False
                if action2 == True:
                    run = False
                
                click3 = False
                action3 = False
                if button3.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button3)
                    self.surface.blit(text3, text3_rect)
                    self.surface.blit(image3, button3)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click3 = True
                        action3 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button3)
                    self.surface.blit(text3, text3_rect)
                    self.surface.blit(image3, button3)
                if pygame.mouse.get_pressed()[0] == 0:
                    click3 = False
                if action3 == True:
                    run = False
                
                click4 = False
                action4 = False
                if button4.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button4)
                    self.surface.blit(text4, text4_rect)
                    self.surface.blit(image4, button4)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click4 = True
                        action4 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button4)
                    self.surface.blit(text4, text4_rect)
                    self.surface.blit(image4, button4)
                if pygame.mouse.get_pressed()[0] == 0:
                    click4 = False
                if action4 == True:
                    run = False
                
                click5 = False
                action5 = False
                if button5.collidepoint(pos):
                    pygame.draw.rect(self.surface, [255,255,255], button5)
                    self.surface.blit(text5, text5_rect)
                    self.surface.blit(image5, button5)
                    if pygame.mouse.get_pressed()[0] == 1:
                        click5 = True
                        action5 = True
                else:
                    pygame.draw.rect(self.surface, [105,105,105], button5)
                    self.surface.blit(text5, text5_rect)
                    self.surface.blit(image5, button5)
                if pygame.mouse.get_pressed()[0] == 0:
                    click5 = False
                if action5 == True:
                    run = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                pygame.display.update()
            if click2 == True:
                self.buttonclick.play()
                return 2
            if click3 == True:
                self.buttonclick.play()
                return 3
            if click4 == True:
                self.buttonclick.play()
                return 4
            if click5 == True:
                self.buttonclick.play()
                return 5
            

    #This function checks if there is a pawn has reached the opposite side
    #If it has, it returns true. Else false
    def isPawnPromotion(self, y, x):
        #scan the board
        #self.game.board
        if (self.game.player == 1):
            if (self.select['piece'] == 1 and y == 0):
                return True
        
        elif (self.game.player == 2):
            if (self.select['piece'] == 11 and y == 7):
                return True

        return False

    # This function starts up the game and sets all the parameters of said game.
    # Not much now but more can be added later
    def backgroundmusic(self):
        pygame.mixer.music.load('Background.wav')
        pygame.mixer.music.set_volume(.30)
        pygame.mixer.music.play(-1)
    def start_game(self):

        self.setUp()
        self.main_Menu()
        
        
        self.ai = None
        
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
            
            if(self.user_clicks == 1):
                #code to generate possible moves and to animate moving the pawn
                select_x, select_y = pygame.mouse.get_pos()
                self.draw_board(square1color, square2color)
                available_moves = self.valid_moves
                selected_moves = []
                for x in available_moves:
                    if(x[0][0] == self.select['y'] and x[0][1] == self.select['x']):
                        selected_moves.append(x)
                for x in selected_moves:
                    #change this to color in the board
                    if(self.game.player == 1):
                        pygame.draw.rect(self.surface, RED, pygame.Rect((x[1][1] * squareSize) , (x[1][0]* squareSize) , squareSize  , squareSize ))
                    elif(self.game.player == 2):
                        pygame.draw.rect(self.surface, (255,255,0), pygame.Rect((x[1][1] * squareSize) , (x[1][0]* squareSize) , squareSize  , squareSize ))

                   
                self.drawPieces()
                self.surface.blit(IMAGES[self.select['piece']] , (select_x-50, select_y-50))
                pygame.display.update()
                self.clock.tick(60)
        
            # if user clicks is 2 then we know some sort of board state occured. Now we have to update the board.
            if (self.user_clicks == 2):

                #Checks if the player can validly make a pawn promotion
                if(self.isPawnPromotion(self.target['y'], self.target['x'])):
                    #update the board to show that the pawn moved to edge of board
                    self.draw_board(square1color, square2color)
                    self.drawPieces()
                    pygame.display.update()
                    #set pawn to player's selected piece
                    self.game.board[ self.target['y'] ][ self.target['x'] ] = self.pawnPromotion(self.game.player)
                    #this is to make pygame wait for user input.
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

                self.draw_board(square1color, square2color)
                self.drawPieces()
                pygame.display.update()
                moves = self.game.get_valid_moves()
                valid_moves = self.game.further_validation(moves)
                """Changed to add if len(valid_moves) == 0"""
                
                        
                if len(valid_moves) == 0 and self.game.check():
                    if (self.game.player == 1):
                        self.end_screen(6)
                    else:
                        self.end_screen(16)
                elif len(valid_moves) == 0:
                   if (self.game.player == 1):
                        self.end_screen(-1)
                   else:
                        self.end_screen(-1)
                self.valid_moves = moves
                #pprint(self.valid_moves)
                print("Black King Position, Row: " + str(self.game._black_king[0]) + " Column: " + str(self.game._black_king[1]) )
                print(str(len(valid_moves)))
                # print(self.game.board) debug purposes                 
    
            self.clock.tick(60)

        quit()