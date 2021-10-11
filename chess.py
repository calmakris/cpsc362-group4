class Chess():

    def __init__(self):
        self.turn = 1
        self.player = 1
        # self.board_change = false could be used to determine if change occured? 
        # classification for differentiating pieces
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

    def make_move(self, from_dict, to_dict):
        self.board[ from_dict['y'] ][ from_dict['x'] ] = 0
        self.board[ to_dict['y'] ][ to_dict['x'] ] = from_dict['piece']

    def is_valid_move(self, select, targetTuple):

        target = { 'piece': self.board[ targetTuple[0] ][ targetTuple[1] ],
                   'y': targetTuple[0],
                   'x': targetTuple[1] }

        if 1 <= select['piece'] <= 6 and 1 <= target['piece'] <= 6:
            return False
        elif 11 <= select['piece'] <= 16 and 11 <= target['piece'] <= 16:
            return False
        
        # White Pawn        --------------------------------------------------------------------------
        if select['piece'] == 1:
            
            # forward moves
            if target['x'] == select['x']:
                if target['y'] + 1 == select['y']:
                    return True
                elif (target['y'] + 2 == select['y'] and select['y'] == 6 and
                      self.board[ select['y'] - 1 ][ select['x'] ] == 0):
                    return True

            # diagonal attacks
            elif target['y'] + 1 == select['y'] and 11 <= target['piece'] <= 16:
                if target['x'] - 1 == select['x']:
                    return True
                elif target['x'] + 1 == select['x']:
                    return True

        # Black Pawn        --------------------------------------------------------------------------
        if select['piece'] == 11:
            
            # forward moves
            if target['x'] == select['x']:
                if target['y'] - 1 == select['y']:
                    return True
                elif (target['y'] - 2 == select['y'] and select['y'] == 1 and
                      self.board[ select['y'] + 1 ][ select['x'] ] == 0):
                    return True

            # diagonal attacks
            elif target['y'] - 1 == select['y'] and 1 <= target['piece'] <= 6:
                if target['x'] - 1 == select['x']:
                    return True
                elif target['x'] + 1 == select['x']:
                    return True

        # Knights           --------------------------------------------------------------------------
        if select['piece'] in (2, 12):

            # 2-1 moves: 2x,1y or 2y,1x; obstruction check not necessary
            if ((abs(target['x'] - select['x']) == 2 and abs(target['y'] - select['y']) == 1) or
                (abs(target['y'] - select['y']) == 2 and abs(target['x'] - select['x']) == 1)):
                return True

        # Rooks & Queens    --------------------------------------------------------------------------
        if select['piece'] in (3, 13, 5, 15):

            # up/down moves
            if target['x'] == target['x']:
                return True
                
            # left/right moves
            elif target['y'] == target['y']:
                return True
        
        # Bishops & Queens  --------------------------------------------------------------------------
        if select['piece'] in (4, 14, 5, 15):

            # diagonal moves: x_movement == y_movement
            if abs(target['x'] - select['x']) == abs(target['y'] - select['y']):
                return True

        # Kings             --------------------------------------------------------------------------
        if select['piece'] in (6, 16):
            # movement in every direction should be 1
            if (abs(target['x'] - select['x']) == 1 or 
                abs(target['y'] - select['y']) == 1):
                return True

        return False

    # TODO: Castling
    def get_valid_moves(self):
        moves = []

        for y in range(8):
            for x in range(8):

                if self.board[y][x] != 0:

                    select = { 'piece': self.board[y][x], 'y': y, 'x': x }
                    up = (y-1) % 8
                    down = (y+1) % 8
                    right = (x+1) % 8
                    left = (x-1) % 8

                    # White Pawns
                    if select['piece'] == 1:
                        # forward moves
                        if self.is_valid_move( select, (up, x) ):
                            moves.append( ((select['y'], select['x']),
                                           (up, x)) )
                            
                            if y == 6 and self.is_valid_move( select, ((y-2)%8, x) ):
                                moves.append( ((select['y'], select['x']),
                                               ((y-2)%8, x)) )

                        # Diag-right capture
                        if self.is_valid_move( select, (up, right) ) and select['x'] < 7:
                            moves.append( ((select['y'], select['x']),
                                           (up, right)) )

                        # Diag-left capture
                        if self.is_valid_move( select, (up, left) ) and select['x'] > 0:
                            moves.append( ((select['y'], select['x']),
                                           (up, left)) )

                    # Black Pawns
                    if select['piece'] == 11:
                        # forward moves
                        if self.is_valid_move( select, (down, x) ):
                            moves.append( ((select['y'], select['x']),
                                           (down, x)) )
                            
                            if y == 1 and self.is_valid_move( select, ((y+2)%8, x) ):
                                moves.append( ((select['y'], select['x']),
                                               ((y+2)%8, x)) )

                        # Diag-right capture
                        if self.is_valid_move( select, (down, right) ) and select['x'] < 7:
                            moves.append( ((select['y'], select['x']),
                                           (down, right)) )

                        # Diag-left capture
                        if self.is_valid_move( select, (down, left) ) and select['x'] > 0:
                            moves.append( ((select['y'], select['x']),
                                           (down, left)) )

                    # Knights
                    if select['piece'] in (2, 12):
                        # Forward 2, left/right 1
                        new_y = (y-2) % 8
                        if self.is_valid_move( select, (new_y, right) ):
                            moves.append( ((select['y'], select['x']),
                                           (new_y, right)) )
                        if self.is_valid_move( select, (new_y, left) ):
                            moves.append( ((select['y'], select['x']),
                                           (new_y, left)) )

                        # Down 2, left/right 1
                        new_y = (y+2) % 8
                        if self.is_valid_move( select, (new_y, right) ):
                            moves.append( ((select['y'], select['x']),
                                           (new_y, right)) )
                        if self.is_valid_move( select, (new_y, left) ):
                            moves.append( ((select['y'], select['x']),
                                           (new_y, left)) )

                        # Right 2, up/down 1
                        new_x = (x+2) % 8
                        if self.is_valid_move( select, (up, new_x) ):
                            moves.append( ((select['y'], select['x']),
                                           (up, new_x)) )
                        if self.is_valid_move( select, (down, new_x) ):
                            moves.append( ((select['y'], select['x']),
                                           (down, new_x)) )

                        # Left 2, up/down 1
                        new_x = (x-2) % 8
                        if self.is_valid_move( select, (up, new_x) ):
                            moves.append( ((select['y'], select['x']),
                                           (up, new_x)) )
                        if self.is_valid_move( select, (down, new_x) ):
                            moves.append( ((select['y'], select['x']),
                                           (down, new_x)) )

                    # Rooks and Queens' lateral moves
                    if select['piece'] in (3, 13, 5, 15):

                        # vertical moves
                        for upOne in range(y, -1, -1):
                            if self.is_valid_move( select, (upOne, x) ):
                                moves.append( ((select['y'], select['x']),
                                               (upOne, x)) )
                            elif upOne == y:
                                continue
                            else:
                                break

                            # stop generating moves after capture move
                            if select['piece'] in (3, 5) and 11 <= self.board[upOne][x] <= 16:
                                break
                            elif select['piece'] in (13, 15) and 1 <= self.board[upOne][x] <= 6:
                                break
                    
                        for downOne in range(y, 8):
                            if self.is_valid_move( select, (downOne, x) ):
                                moves.append( ((select['y'], select['x']),
                                               (downOne, x)) )
                            elif downOne == y:
                                continue
                            else:
                                break

                            # stop generating moves after capture move
                            if select['piece'] in (3, 5) and 11 <= self.board[downOne][x] <= 16:
                                break
                            elif select['piece'] in (13, 15) and 1 <= self.board[downOne][x] <= 6:
                                break

                        # horizontal moves
                        for leftOne in range(x, -1, -1):
                            if self.is_valid_move( select, (y, leftOne)):
                                moves.append( ((select['y'], select['x']),
                                               (y, leftOne)) )
                            elif leftOne == x:
                                continue
                            else:
                                break

                            # stop generating moves after capture move
                            if select['piece'] in (3, 5) and 11 <= self.board[y][leftOne] <= 16:
                                break
                            elif select['piece'] in (13, 15) and 1 <= self.board[y][leftOne] <= 6:
                                break

                        for rightOne in range(x, 8):
                            if self.is_valid_move( select, (y, rightOne)):
                                moves.append( ((select['y'], select['x']),
                                               (y, rightOne)) )
                            elif rightOne == x:
                                continue
                            else:
                                break

                            # stop generating moves after capture move
                            if select['piece'] in (3, 5) and 11 <= self.board[y][rightOne] <= 16:
                                break
                            elif select['piece'] in (13, 15) and 1 <= self.board[y][rightOne] <= 6:
                                break
                    
                    # Bishops and Queens' diagonal moves
                    if select['piece'] in (4, 14, 5, 15):

                        # Towards top right
                        if select['y'] > 0 and select['x'] < 7:
                            new_y = up
                            new_x = right

                            while new_y >= 0 and new_x <= 7:
                                if self.is_valid_move( select, (new_y, new_x) ):
                                    moves.append( ((select['y'], select['x']),
                                                (new_y, new_x) ) )
                                else:
                                    break

                                # stop generating moves after capture move
                                if select['piece'] in (4, 5) and 11 <= self.board[new_y][new_x] <= 16:
                                    break
                                elif select['piece'] in (14, 15) and 1 <= self.board[new_y][new_x] <= 6:
                                    break

                                new_y -= 1
                                new_x += 1

                        # Towards bottom right
                        if select['y'] < 7 and select['x'] < 7:
                            new_y = down
                            new_x = right

                            while new_y <= 7 and new_x <= 7:
                                if self.is_valid_move( select, (new_y, new_x) ):
                                    moves.append( ((select['y'], select['x']),
                                                (new_y, new_x) ) )
                                else:
                                    break

                                # stop generating moves after capture move
                                if select['piece'] in (4, 5) and 11 <= self.board[new_y][new_x] <= 16:
                                    break
                                elif select['piece'] in (14, 15) and 1 <= self.board[new_y][new_x] <= 6:
                                    break

                                new_y += 1
                                new_x += 1

                        # Towards top left
                        if select['y'] > 0 and select['x'] > 0:
                            new_y = up
                            new_x = left
                            while new_y >= 0 and new_x >= 0:
                                if self.is_valid_move( select, (new_y, new_x) ):
                                    moves.append( ((select['y'], select['x']), 
                                                (new_y, new_x) ) )
                                else:
                                    break

                                # stop generating moves after capture move
                                if select['piece'] in (4, 5) and 11 <= self.board[new_y][new_x] <= 16:
                                    break
                                elif select['piece'] in (14, 15) and 1 <= self.board[new_y][new_x] <= 6:
                                    break

                                new_y -= 1
                                new_x -= 1

                        # Towards bottom left
                        if select['y'] < 7 and select['x'] > 0:
                            new_y = down
                            new_x = left
                            while new_y <= 7 and new_x >= 0:
                                if self.is_valid_move( select, (new_y, new_x) ):
                                    moves.append( ((select['y'], select['x']),
                                                (new_y, new_x) ) )
                                else:
                                    break

                                # stop generating moves after capture move
                                if select['piece'] in (4, 5) and 11 <= self.board[new_y][new_x] <= 16:
                                    break
                                elif select['piece'] in (14, 15) and 1 <= self.board[new_y][new_x] <= 6:
                                    break

                                new_y += 1
                                new_x -= 1

                    # Kings
                    if select['piece'] in (6, 16):
                        if self.is_valid_move( select, (up, x) ) and select['y'] > 0: # Up 1
                            moves.append( ((select['y'], select['x']),
                                           (up, x)) )
                        if self.is_valid_move( select, (down, x) ) and select['y'] < 7: # Down 1
                            moves.append( ((select['y'], select['x']), 
                                           (down, x)) )
                        if self.is_valid_move( select, (y, right) ) and select['x'] < 7: # Right 1
                            moves.append( ((select['y'], select['x']), 
                                           (y, right)) )
                        if self.is_valid_move( select, (y, left) ) and select['x'] > 0: # Left 1
                            moves.append( ((select['y'], select['x']), 
                                           (y, left)) )
                        if self.is_valid_move( select, (up, right) ) and select['y'] > 0 and select['x'] < 7: # Up-Right 1
                            moves.append( ((select['y'], select['x']), 
                                           (up, right)) )
                        if self.is_valid_move( select, (down, right) ) and select['y'] < 7 and select['x'] < 7: # Down-Right 1
                            moves.append( ((select['y'], select['x']), 
                                           (down, right)) ) 
                        if self.is_valid_move( select, (up, left) ) and select['y'] > 0 and select['x'] > 0: # Up-Left 1
                            moves.append( ((select['y'], select['x']), 
                                           (up, left)) )
                        if self.is_valid_move( select, (down, left) ) and select['y'] < 7 and select['x'] > 0: # Down-Left 1
                            moves.append( ((select['y'], select['x']), 
                                           (down, left)) )

        return moves
    
    ###################################################
    #                  IN PROGRESS                    #
    ###################################################
    def check_for_checkmate(self, moves):
    #1.) get all moves
        # moves = generate_moves() # to generate all moves
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