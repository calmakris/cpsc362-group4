

class Chess():

    def __init__(self):

        self.turn = 1
        self.player = 1
        # self.board_change = false could be used to determine if change occured? 
        #classification for differentiating pieces
        # White: Pawn = 1, Knight = 2, Rook = 3, Bishop = 4, Queen = 5, King = 6
        # Black: Pawn = 11, Knight = 12, Rook = 13, Bishop = 14, Queen = 15, King = 16
        self.board = [
            [13, 12, 14, 16, 15, 14, 12, 13],
            [11, 11, 11, 11, 11, 11, 11, 11],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 1,  1,  1,  1,  1,  1,  1,  1],
            [ 3,  2,  4,  6,  5,  4,  2,  3]
        ]
    #takes in the piece remove piece to calculate the score and the player to add the points to    
    def point_counter(self, piece, cur_score):
        piece_num = piece
        point_dict = {1:1, 2:3, 4:3, 3:5, 5:9}
        if piece_num > 10:
            piece_num = piece_num - 10
        cur_score = cur_score + point_dict[piece_num]
        return cur_score

    def make_move(self, x1, y1, x2, y2, piece):
        self.board[y1][x1] = 0
        self.board[y2][x2] = piece

    def get_available_moves(self, color, x, y):
        available_moves = list()
        if (color == 1 or color == 11):
            available_moves = available_moves + self.pawn_move(color, x, y)
        
        elif (color == 2 or color == 12):
            available_moves = available_moves + self.knight_move(color, x, y)
        
        elif (color == 3 or color == 13):
            available_moves = available_moves + self.rook_move(color, x, y)

        elif (color == 4 or color == 14):
            available_moves = available_moves + self.bishop_move(color, x, y)
        
        elif (color == 5 or color == 15):
            available_moves = available_moves + self.queen_move(color, x, y)

        elif (color == 6 or color == 16):
            available_moves = available_moves + self.king_move(color, x, y)
        
        return available_moves




    def pawn_move(self, color, x, y):
        available_moves = []

        #check color so we know if it needs to go up or down
        if (color == 1):

            #make sure that the pawn isn't at the otherend of the board.
            if(y != 0):

                if(self.board[y-1][x] == 0):
                    available_moves.append((y-1, x))
                    if (y == 6 and self.board[y-2][x] == 0):
                        available_moves.append((y-2, x))

                #This checks the case if the pawn is at the left edge of the board
                if(x != 0):
                    if(self.board[y-1][x-1] >= 11 and self.board[y-1][x-1] <= 16):
                        available_moves.append((y-1,x-1))
                #This checks the case if the pawn is at the right edge of the board
                if (x != 7):
                    if(self.board[y-1][x+1] >= 11 and self.board[y-1][x+1] <= 16):
                        available_moves.append((y-1,x+1))
        
        elif (color == 11):

            if(y != 7):
                if(self.board[y+1][x] == 0):
                    available_moves.append((y+1,x))

                    if (y == 1 and self.board[y+2][x] == 0):
                        available_moves.append((y+2, x))

                if (x != 0):
                    if (self.board[y+1][x-1] >= 1 and self.board[y+1][x-1] <= 6):
                        available_moves.append((y+1, x-1))

                if(x != 7):
                    if (self.board[y+1][x+1] >= 1 and self.board[y+1][x+1] <= 6):
                        available_moves.append((y+1, x+1))
        
        return available_moves
    
    def rook_move(self, color,  x, y):
        available_moves = list()

        #first check to see it's available moves for up
        if(y != 0):
            for i in range(y, -1, -1):
                if(self.board[i][x] == 0):
                    available_moves.append((i, x))
                elif((color == 3 or color == 5) and self.board[i][x] >= 11 and self.board[i][x] <= 16):
                   available_moves.append((i, x))
                   break
                
                elif((color == 13 or color == 15) and self.board[i][x] >= 1 and self.board[i][x] <= 6):
                    available_moves.append((i, x))
                    break
                
                elif (i == y):
                    continue
                else:
                    break
        
        #Now check down

        if(y != 7):
            for i in range(y, 8):
                if(self.board[i][x] == 0):
                   available_moves.append((i, x))
                elif((color == 3 or color == 5) and self.board[i][x] >= 11 and self.board[i][x] <= 16):
                    available_moves.append((i, x))
                    break
                
                elif((color == 13 or color == 15) and self.board[i][x] >= 1 and self.board[i][x] <= 6):
                   available_moves.append((i, x))
                   break
                
                elif (i == y):
                    continue
                else:
                    break

        #Now check the left side

        if(x != 0):
            for i in range(x, -1, -1):
                if(self.board[y][i] == 0):
                    available_moves.append((y, i))
                elif((color == 3 or color == 5) and self.board[y][i] >= 11 and self.board[y][i] <= 16):
                   available_moves.append((y, i))
                   break
                
                elif((color == 13 or color == 15) and self.board[y][i] >= 1 and self.board[y][i] <= 6):
                   available_moves.append((y, i))
                   break
                
                #
                elif (i == x):
                    continue
                else:
                    break
        
        #finally check right 
        if(x != 7):
            for i in range(x, 8):
                if(self.board[y][i] == 0):
                   available_moves.append((y, i))
                elif((color == 3 or color == 5) and self.board[y][i] >= 11 and self.board[y][i] <= 16):
                    available_moves.append((y, i))
                    break
                
                elif((color == 13 or color == 15) and self.board[y][i] >= 1 and self.board[y][i] <= 6):
                    available_moves.append((y, i))
                    break
                
                #
                elif (i == x):
                    continue
                else:
                    break
        return available_moves

            
    def bishop_move(self, color, x, y):
        available_moves = list()

        #check left-up
        if(y != 0 and x != 0):
            up = y-1
            left = x-1
            while(up != -1 and left != -1):
                if self.board[up][left] == 0:
                    available_moves.append((up,left))
                    up -=1
                    left -=1
                elif (color == 4 or color == 5) and self.board[up][left] >= 11 and self.board[up][left] <= 16:
                    available_moves.append((up,left))
                    up -=1
                    left -=1
                    break
                elif (color == 14 or color == 15) and self.board[up][left] >= 1 and self.board[up][left] <= 6:
                    up -=1
                    left -=1
                    available_moves.append((up,left))
                    break
                else:
                    break
        
        #check up-right
        if(y != 0 and x != 7):
            up = y-1
            right = x+1
            while(up != -1 and right != 8):
                if self.board[up][right] == 0:
                    available_moves.append((up,right))
                    up -=1
                    right +=1
                elif (color == 4 or color == 5) and self.board[up][right] >= 11 and self.board[up][right] <= 16:
                    available_moves.append((up,right))
                    up -=1
                    right +=1
                    break
                elif (color == 14 or color == 15) and self.board[up][right] >= 1 and self.board[up][right] <= 6:
                    up -=1
                    right +=1
                    available_moves.append((up,right))
                    break
                else:
                    break
        
        #check down-right
        if(y != 7 and x != 7):
            down = y+1
            right = x +1
            while(down != 8 and right != 8):
                if self.board[down][right] == 0:
                    available_moves.append((down,right))
                    down +=1
                    right +=1
                elif (color == 4 or color == 5) and self.board[down][right] >= 11 and self.board[down][right] <= 16:
                    available_moves.append((down,right))
                    down +=1
                    right +=1
                    break
                elif (color == 14 or color == 15) and self.board[down][right] >= 1 and self.board[down][right] <= 6:
                    available_moves.append((down,right))
                    down +=1
                    right +=1
                    break
                else:
                    break
        
        #check down-left
        if(y != 7 and x != 0):
            down = y+1
            left = x-1
            while(down != 8 and left != -1):
                if self.board[down][left] == 0:
                    available_moves.append((down,left))
                    down +=1
                    left -=1
                elif (color == 4 or color == 5) and self.board[down][left] >= 11 and self.board[down][left] <= 16:
                    available_moves.append((down,left))
                    down +=1
                    left -=1
                    break
                elif (color == 14 or color == 15) and self.board[down][left] >= 1 and self.board[down][left] <= 6:
                    available_moves.append((down,left))
                    down +=1
                    left -=1
                    break
                else:
                    break
        
        return available_moves
              

            

    
    
    def knight_move(self, color, x, y):
        #8 possible moves so 8 if statements.
        row = y
        column = x
        available_moves = list()
        if (row >1 and column != 0):

            if(self.board[row-2][column-1] == 0):
                available_moves.append((row-2, column-1))
            elif (color == 2 and self.board[row-2][column-1] >= 11 and self.board[row-2][column-1] <= 16):
                available_moves.append((row-2, column-1))
            elif (color == 12 and self.board[row-2][column-1] >= 1 and self.board[row-2][column-1] <= 6):
                available_moves.append((row-2, column-1))

        if (row > 1 and column != 7):

            if(self.board[row-2][column+1] == 0):
                available_moves.append((row-2, column+1))
            elif (color == 2 and self.board[row-2][column+1] >= 11 and self.board[row-2][column+1] <= 16):
                available_moves.append((row-2, column+1))
            elif (color == 12 and self.board[row-2][column+1] >= 1 and self.board[row-2][column+1] <= 6):
                available_moves.append((row-2, column+1))

        if (column > 1 and row != 7):

            if(self.board[row+1][column-2] == 0):
                available_moves.append((row+1, column-2))
            elif (color == 2 and self.board[row+1][column-2] >= 11 and self.board[row+1][column-2] <= 16):
                available_moves.append((row+1, column-2))
            elif (color == 12 and self.board[row+1][column-2] >= 1 and self.board[row+1][column-2] <= 6):
               available_moves.append((row+1, column-2))

        if (column > 1 and row != 0):

            if(self.board[row-1][column-2] == 0):
                available_moves.append((row-1, column-2))
            elif (color == 2 and self.board[row-1][column-2] >= 11 and self.board[row-1][column-2] <= 16):
                available_moves.append((row-1, column-2))
            elif (color == 12 and self.board[row-1][column-2] >= 1 and self.board[row-1][column-2] <= 6):
               available_moves.append((row-1, column-2))

        if (column <=5 and row != 0):
            
            if(self.board[row-1][column+2] == 0):
                available_moves.append((row-1, column+2))
            elif (color == 2 and self.board[row-1][column+2] >= 11 and self.board[row-1][column+2] <= 16):
                available_moves.append((row-1, column+2))
            elif (color == 12 and self.board[row-1][column+2] >= 1 and self.board[row-1][column+2] <= 6):
                available_moves.append((row-1, column+2))
        
        if (column <=5 and row < 7):
            if(self.board[row+1][column+2] == 0):
                available_moves.append((row+1, column+2))
            elif (color == 2 and self.board[row+1][column+2] >= 11 and self.board[row+1][column+2] <= 16):
                available_moves.append((row+1, column+2))
            elif (color == 12 and self.board[row+1][column+2] >= 1 and self.board[row+1][column+2] <= 6):
                available_moves.append((row+1, column+2))

        if (row <= 5 and column >= 1):
            if(self.board[row+2][column-1] == 0):
                available_moves.append((row+2, column-1))
            elif (color == 2 and self.board[row+2][column-1] >= 11 and self.board[row+2][column-1] <= 16):
                available_moves.append((row+2, column-1))
            elif (color == 12 and self.board[row+2][column-1] >= 1 and self.board[row+2][column-1] <= 6):
                available_moves.append((row+2, column-1))

        if (row <=5 and column <=6):
            if(self.board[row+2][column+1] == 0):
                available_moves.append((row+2, column+1))
            elif (color == 2 and self.board[row+2][column+1] >= 11 and self.board[row+2][column+1] <= 16):
                available_moves.append((row+2, column+1))
            elif (color == 12 and self.board[row+2][column+1] >= 1 and self.board[row+2][column+1] <= 6):
                available_moves.append((row+2, column+1))
    
        return available_moves
    
   
    def king_move(self, color, x, y):
        column = x
        row = y
        available_moves = list()

        #king can move in all directions one space.

        if (row != 0):
            if(self.board[row-1][column] == 0):
                available_moves.append((row-1, column))
            elif (color == 6 and self.board[row-1][column] >= 11 and self.board[row-1][column] <= 16):
                available_moves.append((row-1, column))
            elif (color == 16 and self.board[row-1][column] >= 1 and self.board[row-1][column] <= 6):
                available_moves.append((row-1, column))
        
        if (row != 0 and column != 0):
            if(self.board[row-1][column-1] == 0):
                available_moves.append((row-1, column-1))
            elif (color == 6 and self.board[row-1][column-1] >= 11 and self.board[row-1][column-1] <= 16):
                available_moves.append((row-1, column-1))
            elif (color == 16 and self.board[row-1][column-1] >= 1 and self.board[row-1][column-1] <= 6):
                available_moves.append((row-1, column-1))
        
        if (column != 0):
            if(self.board[row][column-1] == 0):
                available_moves.append((row, column-1))
            elif (color == 6 and self.board[row][column-1] >= 11 and self.board[row][column-1] <= 16):
                available_moves.append((row, column-1))
            elif (color == 16 and self.board[row][column-1] >= 1 and self.board[row][column-1] <= 6):
                available_moves.append((row, column-1))
        
        if (column != 7):
            if(self.board[row][column+1] == 0):
                available_moves.append((row, column+1))
            elif (color == 6 and self.board[row][column+1] >= 11 and self.board[row][column+1] <= 16):
                available_moves.append((row, column+1))
            elif (color == 16 and self.board[row][column+1] >= 1 and self.board[row][column+1] <= 6):
                available_moves.append((row, column+1))
        
        if (column != 0 and row != 7):
            if(self.board[row+1][column-1] == 0):
                available_moves.append((row+1, column-1))
            elif (color == 6 and self.board[row+1][column-1] >= 11 and self.board[row+1][column-1] <= 16):
                available_moves.append((row+1, column-1))
            elif (color == 16 and self.board[row+1][column-1] >= 1 and self.board[row+1][column-1] <= 6):
                available_moves.append((row+1, column-1))

        if (row != 7):
            if(self.board[row+1][column] == 0):
                available_moves.append((row+1, column))
            elif (color == 6 and self.board[row+1][column] >= 11 and self.board[row+1][column] <= 16):
                available_moves.append((row+1, column))
            elif (color == 16 and self.board[row+1][column] >= 1 and self.board[row+1][column] <= 6):
                available_moves.append((row+1, column))

        if (row!= 7 and column != 7):
            if(self.board[row+1][column+1] == 0):
                available_moves.append((row+1, column+1))
            elif (color == 6 and self.board[row+1][column+1] >= 11 and self.board[row+1][column+1] <= 16):
                available_moves.append((row+1, column+1))
            elif (color == 16 and self.board[row+1][column+1] >= 1 and self.board[row+1][column+1] <= 6):
                available_moves.append((row+1, column+1))
        
        if (row != 0 and column != 7):
            if(self.board[row-1][column+1] == 0):
                available_moves.append((row-1, column+1))
            elif (color == 6 and self.board[row-1][column+1] >= 11 and self.board[row-1][column+1] <= 16):
                available_moves.append((row-1, column+1))
            elif (color == 16 and self.board[row-1][column+1] >= 1 and self.board[row-1][column+1] <= 6):
                available_moves.append((row-1, column+1))
        
        return available_moves

    def queen_move(self, color, x, y):
        available_moves = list()
        available_moves = available_moves + self.rook_move(color, x, y)
        available_moves = available_moves + self.bishop_move(color, x, y)
        return available_moves

    ###################################################
    #                  IN PROGRESS                    #
    ###################################################
    def check_for_checkmate(self):
    #1.) get all moves
        moves = generate_moves() # to generate all moves
    #2.) make move
        for i in range(len(moves)-1,-1,-1): # iterating from list backwards
            self.do_the_move(moves[i]) # makes the moves in a list
    #3.) if in check remove all invalid moves
        if self.check():
            moves.remove(moves[i]) # removes all invalid moves
        if len(moves) == 0: # if list of valid moves is 0 then checkmate
            if self.check():
                self.checkmate = True
        else:
            self.checkmate = False
        return moves


    # checks to see if kings are under attack
    def check(self):
        if self.white_turn():
            if self.all_opponent_attacks(self.location_of_white_king[x], self.self.location_of_white_king[y]):
                return True
            else:
                return False    
        else:
            if self.all_opponent_attacks(self.location_of_black_king[x], self.self.location_of_black_king[y]): 
                return True
            else:
                return False 