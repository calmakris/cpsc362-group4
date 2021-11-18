#The purpose of this file is to act as the  driver for the pygame functions. 
#Essentially this will be where pygame is programmed and the other file will be where the chess 
#functions will be called.

import pygame, sys, time, math, copy, chess, os, random, numpy as np

#These are varoables representing colors BROWN and White for pygame applications.
available_moves_tf = True
undo_moves_tf = True
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
PURPLE = (106, 90, 205)
BLUE = (28, 155, 188)
GREEN = (60, 179, 113)
RED = (255,0,0)
clr_dict = { 			#change here
    "Red" : (255, 0, 0),
    "Lime" : (0, 255, 0),
    "Blue" : (0, 0, 255),
    "Yellow" : (255, 255, 0),
    "Cyan" : (0, 255, 255),
    "Magenta" : (255, 0, 255),
    "Green" : (0, 128, 0),
    "Purple" : (128, 0, 128),
    "Teal" : (0, 128, 128),
    "Navy" : (0, 0, 128),
}
Color2 = clr_dict["Yellow"]
Color1 = clr_dict["Red"]
displayWidth = 800
displayHeight = 800
squareSize = displayHeight//8
COVERIMAGES = {}
IMAGES = {}
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pack = 'images/Originals'
# start of declarations
hover_col = (75, 225, 255)
undo_button1 = pygame.Rect(775, 385, 25, 25) 
pos1 = pygame.mouse.get_pos()

screen = pygame.display.set_mode((displayWidth,displayHeight))
undo_font = pygame.font.SysFont(None, 10)
# end of declarations                  

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

        self.ai = False
        self.ai_undo = False
        self.ai_mode = "alpha-beta"

        self.valid_moves = self.game.get_valid_moves()
        self.square1color = WHITE
        self.square2color = BROWN
    
    def setUp(self):
        #imports all available pygame modules
        
        pygame.display.set_caption('Chess')
        #Sets the parameter on how big the pygame screen will be
        

        for x in range(0,8):
            for y in range(0,8):
                if(y % 2 == 0 and x %2 == 0):
                    pygame.draw.rect(self.surface, self.square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                elif(y % 2 == 0 and x %2 == 1):
                    pygame.draw.rect(self.surface, self.square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                elif (y %2 == 1 and x%2 == 1):
                    pygame.draw.rect(self.surface, self.square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 0):
                    pygame.draw.rect(self.surface, self.square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
    
        self.load_Images(pack)
        self.drawPieces()

        # updates the pygame screen.
        pygame.display.update()
        
        # Creates an object to keep track of time taken.
        
        self.clock = pygame.time.Clock()
        #This function should set up the peices and be used to make changes to the pieces.

    def draw_board(self):
          for x in range(8):
            for y in range(8):
                if (y % 2 == 0 and x %2 == 0):
                   pygame.draw.rect(self.surface, self.square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                    
                elif (y % 2 == 0 and x %2 == 1):
                    pygame.draw.rect(self.surface, self.square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 1):
                    pygame.draw.rect(self.surface, self.square1color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))
                
                elif (y %2 == 1 and x%2 == 0):
                    pygame.draw.rect(self.surface, self.square2color, pygame.Rect(y * squareSize , x * squareSize , squareSize , squareSize ))

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

        clock = pygame.time.Clock()
        while True:
            screen.fill((0,0,0))

            self.draw_text('Main Menu', font, (255, 255, 255), screen, displayWidth//20, displayHeight//20)

            mx, my = pygame.mouse.get_pos()

            button1 = pygame.Rect(displayWidth//4, displayHeight//4, displayWidth/2,  displayHeight/8)
            button2 = pygame.Rect(displayWidth//4, displayHeight//2, displayWidth//2, displayHeight//8)
            button3 = pygame.Rect(displayWidth//4, (displayHeight//2) + (displayHeight//4), displayWidth//2, displayHeight//8)

            pygame.draw.rect(screen, (255, 255, 255), button1)
            self.draw_text('Player vs Player', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//4)
            pygame.draw.rect(screen, (255, 255, 255), button2)
            self.draw_text('Player vs Ai', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//2)
            pygame.draw.rect(screen, (255, 255, 255), button3)
            self.draw_text('Exit', button_font, (0, 0, 0), screen, displayWidth//4, (displayHeight//2) + (displayHeight//4))

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
                        self.draw_board()
                        self.drawPieces()
                        pygame.display.update()
                        return None
                    elif button2.collidepoint((mx, my)):
                        self.buttonclick.play()
                        self.ai = True
                        self.draw_board()
                        self.drawPieces()
                        pygame.display.update()
                        return None
                    elif button3.collidepoint((mx, my)):
                        self.buttonclick.play()
                        quit()

            pygame.display.update()

    def Ai_Menu(self):
        
        resolution = (displayWidth, displayHeight)
        screen = pygame.display.set_mode(resolution)
        font = pygame.font.SysFont(None, displayHeight//8)
        button_font = pygame.font.SysFont(None, 45)

        clock = pygame.time.Clock()
        while True:
            screen.fill((0,0,0))

            self.draw_text('Please Choose Your Ai:', font, (255, 255, 255), screen, displayWidth//20, displayHeight//20)

            mx, my = pygame.mouse.get_pos()

            button1 = pygame.Rect(displayWidth//4, displayHeight//4, displayWidth/2,  displayHeight/8)
            button2 = pygame.Rect(displayWidth//4, displayHeight//2, displayWidth//2, displayHeight//8)
            button3 = pygame.Rect(displayWidth//4, (displayHeight//2) + (displayHeight//4), displayWidth//2, displayHeight//8)

            pygame.draw.rect(screen, (255, 255, 255), button1)
            self.draw_text('Alpha Beta Pruning Ai', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//4)
            pygame.draw.rect(screen, (255, 255, 255), button2)
            self.draw_text('Random Ai', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//2)
            pygame.draw.rect(screen, (255, 255, 255), button3)
            self.draw_text('Exit', button_font, (0, 0, 0), screen, displayWidth//4, (displayHeight//2) + (displayHeight//4))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button1.collidepoint((mx, my)):
                        self.ai_mode = "alpha-beta"
                        self.draw_board()
                        self.drawPieces()
                        pygame.display.update()
                        return None
                    elif button2.collidepoint((mx, my)):
                        self.ai_mode = "random"
                        self.draw_board()
                        self.drawPieces()
                        pygame.display.update()
                        return None
                    elif button3.collidepoint((mx, my)):
                        quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                
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
                        self.draw_board()
                        self.drawPieces()
                        pygame.display.update()
                        return None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if button.collidepoint(mouse_pos):
                        self.buttonclick.play()
                        self.draw_board()
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
                if event.type == pygame.QUIT:
                    quit()
            
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
                    click6 = True
                    action6 = True
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
        if click6 == True:
            self.buttonclick.play()
            return 6
        if click7 == True:
            self.buttonclick.play()
            return 7
        if click8 == True:
            self.buttonclick.play()
            return 8

    def Options_screen(self):
        global available_moves_tf
        global undo_moves_tf
        global Color1
        global Color2
        resolution = (displayWidth, displayHeight)
        screen = pygame.display.set_mode(resolution)
        font = pygame.font.SysFont(None, displayHeight//4)
        button_font = pygame.font.SysFont(None, displayHeight//11)

        while True:
            screen.fill((0,0,0))
            self.draw_text('Options', font, (255, 255, 255), screen, displayWidth//20, displayHeight//22)
            mx, my = pygame.mouse.get_pos()

            option1 = pygame.Rect(displayWidth//4, displayHeight//4.5, displayWidth//2,  displayHeight//10)
            option2 = pygame.Rect(displayWidth//4, displayHeight//2.25, displayWidth//2, displayHeight//10)
            option3 = pygame.Rect(displayWidth//4, displayHeight//1.6, displayWidth//2, displayHeight//10)
            option4 = pygame.Rect(displayWidth//4, displayHeight//1.30, displayWidth//2, displayHeight//10)
            option5 = pygame.Rect(displayWidth//4, displayHeight//1.15, displayWidth//2, displayHeight//10)

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
            self.draw_text('Styles', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//1.6)

            pygame.draw.rect(screen, Color1, option4)
            self.draw_text('P1 [] Color', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//1.30)
            pygame.draw.rect(screen, Color2, option5)
            self.draw_text('P2 [] Color', button_font, (0, 0, 0), screen, displayWidth//4, displayHeight//1.15)
            
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
                            self.square1color = WHITE
                            self.square2color = BROWN
                            self.draw_board()
                            
                        elif imgpack == 6:
                            self.square1color = WHITE
                            self.square2color = PURPLE
                            self.draw_board()
                            
                        elif imgpack == 7:
                            self.square1color = WHITE
                            self.square2color = BLUE
                            print()
                            print()
                            self.draw_board()
                           
                        elif imgpack == 8:
                            self.square1color = WHITE
                            self.square2color = GREEN
                            self.draw_board()
    
                    elif option4.collidepoint((mx, my)):
                        if Color1 == clr_dict["Red"]:
                            Color1 = clr_dict["Blue"]
                        elif Color1 == clr_dict["Blue"]:
                            Color1 = clr_dict["Lime"]
                        elif Color1 == clr_dict["Lime"]:
                            Color1 = clr_dict["Cyan"]
                        elif Color1 == clr_dict["Cyan"]:
                            Color1 = clr_dict["Magenta"]
                        elif Color1 == clr_dict["Magenta"]:
                            Color1 = clr_dict["Red"] 
                        pygame.display.update()
                    elif option5.collidepoint((mx, my)):
                        if Color2 == clr_dict["Yellow"]:
                            Color2 = clr_dict["Purple"]
                        elif Color2 == clr_dict["Purple"]:
                            Color2 = clr_dict["Green"]
                        elif Color2 == clr_dict["Green"]:
                            Color2 = clr_dict["Navy"]
                        elif Color2 == clr_dict["Navy"]:
                            Color2 = clr_dict["Teal"]
                        elif Color2 == clr_dict["Teal"]:
                            Color2 = clr_dict["Yellow"]

            pygame.display.update()

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

        # Checking if the user is just selecting a piece to move
        if self.user_clicks == 0:
            
            # Ensure players select their corresponding piece
            if ((self.game.player == 1 and 1 <= piece <= 6) or 
                (self.game.player == 2 and 11 <= piece <= 16)):
                    self.select['piece'] = piece
                    self.select['y'] = select_y
                    self.select['x'] = select_x
                    self.user_clicks = 1

        # Checks when user has already selected a piece
        elif self.user_clicks == 1:
            
            # if the player selects the tile with the selected piece let it go.
            if (select_x == self.select['x'] and select_y == self.select['y']):
                self.game.board[select_y][select_x] = self.select['piece']
                self.select['piece'] = -1
                self.select['y'] = -1
                self.select['x'] = -1
                self.user_clicks = 0
                self.draw_board()
                self.drawPieces()
                pygame.display.update()

            # if player has rook selected then selects a king, this is a castling move input
            elif ((self.game.player == 1 and ((self.select['piece'] == 3 and piece == 6) or (self.select['piece'] == 6 and piece == 3))) or
                self.game.player == 2 and ((self.select['piece'] == 13 and piece == 16) or (self.select['piece'] == 16 and piece == 13))):

                move = ( (self.select['y'], self.select['x']),
                         (select_y, select_x) )

                if move in self.valid_moves:
                    self.target['piece'] = piece
                    self.target['y'] = select_y
                    self.target['x'] = select_x

                    if self.select['piece'] in (3, 13):
                        rook = self.select
                        king = {'piece': piece, 'y': select_y, 'x': select_x}
                    elif self.select['piece'] in (6, 16):
                        king = self.select
                        rook = {'piece': piece, 'y': select_y, 'x': select_x}

                    # Update before movement
                    self.update_castling_state(rook)
                    self.update_castling_state(king)

                    # Queenside castling
                    if rook['x'] < king['x']:
                        # Move rook
                        self.game.make_move( rook,
                                             {'piece': rook['piece'],
                                              'y': rook['y'],
                                              'x': rook['x'] + 3} )
                        
                        # Move king
                        self.game.make_move( king,
                                             {'piece': king['piece'],
                                              'y': king['y'],
                                              'x': king['x'] - 2})

                    # Kingside castling
                    elif rook['x'] > king['x']:
                        # Move rook
                        self.game.make_move( rook,
                                             {'piece': rook['piece'],
                                              'y': rook['y'],
                                              'x': rook['x'] - 2} )
                        
                        # Move king
                        self.game.make_move( king,
                                             {'piece': king['piece'],
                                              'y': king['y'],
                                              'x': king['x'] + 2})

                    self.movesound.play()
                    self.user_clicks = 2                    

            # if player still selects their piece, set that piece as new selected
            elif ((self.game.player == 1 and 1 <= piece <= 6) or 
                (self.game.player == 2 and 11 <= piece <= 16)):
                self.select['piece'] = piece
                self.select['y'] = select_y
                self.select['x'] = select_x
                self.user_clicks = 1
                self.draw_board()
                self.drawPieces()
                pygame.display.update()

            else:
                self.target['piece'] = piece
                self.target['y'] = select_y
                self.target['x'] = select_x
                
                move = ( (self.select['y'], self.select['x']), 
                         (select_y, select_x) )

                # check if select-target combo is in available moves
                if move in self.valid_moves:
                    self.game.make_move( self.select, self.target )
                    self.movesound.play()
                    self.update_castling_state(self.select)
                    self.prev_move += 1
                    self.user_clicks = 2

    # Keeps track rooks and kings for castling
    def update_castling_state(self, selected):
        if selected['piece'] == 13 and selected['y'] == 0 and selected['x'] == 0:
            self.game.track_castling['TopL'] = True
        elif selected['piece'] == 13 and selected['y'] == 0 and selected['x'] == 7:
            self.game.track_castling['TopR'] = True
        elif selected['piece'] == 3 and selected['y'] == 7 and selected['x'] == 0:
            self.game.track_castling['BotL'] = True
        elif selected['piece'] == 3 and selected['y'] == 7 and selected['x'] == 7:
            self.game.track_castling['BotR'] = True
        elif selected['piece'] == 6 and selected['y'] == 7 and selected['x'] == 4:
            self.game.track_castling['King1'] = True
        elif selected['piece'] == 16 and selected['y'] == 0 and selected['x'] == 4:
            self.game.track_castling['King2'] = True

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
            self.game.undo_move()
            self.prev_move -= 1
            self.user_clicks = 2

            if (self.ai == True):
                self.game.undo_move()
                self.prev_move -= 1
                self.ai_undo = True

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

    def prepare_next_turn(self):
        if (self.game.player == 1):
            self.game.player = 2
        elif (self.game.player == 2):
            self.game.player = 1

        self.select = { 'piece': -1, 'y': -1, 'x': -1 }
        self.target = { 'piece': -1, 'y': -1, 'x': -1 }
        self.valid_moves.clear()

        self.draw_board()
        self.drawPieces()
        pygame.display.update()

        # Make sure undo vs AI switches back to player's turn
        if self.ai_undo == True:
            self.game.player = 1
            self.ai_undo = False

        moves = self.game.get_valid_moves()
        valid_moves = self.game.further_validation(moves)
        if len(valid_moves) == 0 and self.game.check():
            if (self.game.player == 1):
                self.end_screen(6)
            else:
                self.end_screen(16)
        self.valid_moves = moves

    # This function starts up the game and sets all the parameters of said game.
    # Not much now but more can be added later
     # This function starts up the game and sets all the parameters of said game.
    # Not much now but more can be added later
    def backgroundmusic(self):
        pygame.mixer.music.load('Background.wav')
        pygame.mixer.music.set_volume(.30)
        pygame.mixer.music.play(-1)
        
    def start_game(self):

        self.setUp()
        self.main_Menu()
        if self.ai == True:
            self.Ai_Menu()
        
        # This is the main loop the game will run through until it ends or gets restarted.
        while True:
            if self.game.player == 2 and self.ai:
                if self.ai_mode == "random":
                    random_move = self.valid_moves[random.randrange(len(self.valid_moves))]
                    select = self.game.get_piece_dict(random_move[0][0], random_move[0][1])
                    target = self.game.get_piece_dict(random_move[1][0], random_move[1][1])
                    time.sleep(3) # slow it down

                elif self.ai_mode == "alpha-beta":
                    best_move = alpha_beta_cutoff_search(self.game)
                    if(best_move == None):
                        self.end_screen(16)
                    else:
                        target = self.game.get_piece_dict(best_move[1][0], best_move[1][1])
                        select = self.game.get_piece_dict(best_move[0][0], best_move[0][1])

                self.game.make_move(select, target)
                self.movesound.play()
                self.prepare_next_turn()

            else:
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

                    if event.type == pygame.MOUSEMOTION:
                        mouse_pos2 = event.pos
                        if(undo_button1.collidepoint(mouse_pos2)):
                            pygame.draw.rect(screen, hover_col, undo_button1)
                            pygame.display.update()    

                    if (len(self.game.prev_moves) != 0):
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            mouse_pos1 = event.pos  # gets mouse position
                            # checks if mouse position is over the button
                            if (undo_button1.collidepoint(mouse_pos1)):
                                #switch to player
                                self.user_clicks = 2
                                self.prev_move -= 1

                                if self.game.player == 1:
                                    self.game.undo_move()
                                    
                                elif self.game.player == 2:
                                    self.game.undo_move()

                                if self.ai == True:
                                    self.game.undo_move()
                                    self.prev_move -= 1
                                    self.ai_undo = True
                                    
                    pygame.draw.rect(screen, [0,238,238], undo_button1)  # draw button
                    text_surface_object = pygame.font.SysFont(None, 10).render('undo', True, [0,0,0])    
                    text_rect1 = text_surface_object.get_rect(center=undo_button1.center)   
                    screen.blit(text_surface_object, text_rect1)
                    pygame.display.update()

                if(self.user_clicks == 1):
                    #code to generate possible moves and to animate moving the pawn
                    select_x, select_y = pygame.mouse.get_pos()
                    self.draw_board()
                    available_moves = self.valid_moves
                    selected_moves = []
                    for x in available_moves:
                        if(x[0][0] == self.select['y'] and x[0][1] == self.select['x']):
                            selected_moves.append(x)
                    for x in selected_moves:
                        #change this to color in the board
                        if(self.game.player == 1):
                            pygame.draw.rect(self.surface, Color1, pygame.Rect((x[1][1] * squareSize) , (x[1][0]* squareSize) , squareSize  , squareSize ))
                        elif(self.game.player == 2):
                            pygame.draw.rect(self.surface, Color2, pygame.Rect((x[1][1] * squareSize) , (x[1][0]* squareSize) , squareSize  , squareSize ))

                    self.drawPieces()
                    self.surface.blit(IMAGES[self.select['piece']] , (select_x-50, select_y-50))
                    pygame.display.update()
                    self.clock.tick(60)
            
                # if user clicks is 2 then we know some sort of board state occured. Now we have to update the board.
                if (self.user_clicks == 2):

                    #Checks if the player can validly make a pawn promotion
                    if(self.isPawnPromotion(self.target['y'], self.target['x'])):
                        #update the board to show that the pawn moved to edge of board
                        self.draw_board()
                        self.drawPieces()
                        pygame.display.update()
                        #set pawn to player's selected piece
                        self.game.board[ self.target['y'] ][ self.target['x'] ] = self.pawnPromotion(self.game.player)
                        #this is to make pygame wait for user input.
                        evemt = pygame.event.wait()
                        pygame.display.update()

                    self.prepare_next_turn()
                    self.user_clicks = 0
    
                self.clock.tick(60)

        quit()

def alpha_beta_cutoff_search( game, d=3, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    
    cutoff_test = lambda depth: depth == 0 # You want to stop once it reaches depth d
    eval_fn = lambda : game.advanced_evaluation()
    best_score = -np.inf
    best_move = None
    depth = d
    
    for x in game.actions():
        from_square = game.get_piece_dict(x[0][0], x[0][1])
        to_square = game.get_piece_dict(x[1][0], x[1][1])
        game.make_move(from_square, to_square)
        value = min_value(-np.inf, np.inf, depth - 1, game, eval_fn)
        game.undo_move()
        if(value >= best_score):
            best_move = x
            best_score = value
            print(best_score)
            print(best_move)
    if (game.player == 1):
        game.player = 2
    return best_move

def min_value(alpha, beta, depth, game, eval_fn):

        if depth == 0:
            #print(eval_fn())
            return -eval_fn()
        best_min_score = np.inf
        if (game.player == 2):
            game.player = 1
        for move in game.actions():
            from_square = game.get_piece_dict(move[0][0], move[0][1])
            to_square = game.get_piece_dict(move[1][0], move[1][1])
            game.make_move(from_square, to_square)
            best_min_score = min(best_min_score, max_value(alpha, beta, depth - 1, game, eval_fn))
            game.undo_move()
            beta = min(beta, best_min_score)
            if (beta <= alpha):
                return best_min_score
        


        return best_min_score


def max_value(alpha, beta, depth, game, eval_fn):
        if depth == 0:
            return -eval_fn()
        best_max_score = -np.inf
        if(game.player == 1):
            game.player = 2
        for move in game.actions():
            from_square = game.get_piece_dict(move[0][0], move[0][1])
            to_square = game.get_piece_dict(move[1][0], move[1][1])
            game.make_move(from_square, to_square)
            best_max_score = max(best_max_score, min_value(alpha, beta, depth - 1, game, eval_fn))
            game.undo_move()
            alpha = max(alpha, best_max_score)
            #print(alpha)
            if (beta <= alpha):
                return best_max_score
        return best_max_score