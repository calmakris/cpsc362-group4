import copy
import pygame

class Chess():

    def __init__(self):
        self.turn = 1
        self.player = 1
        self._white_king = (7,4)
        self._black_king = (0,4)
        self.check_mate = False
        self.Stale_Mate = False
        self.in_check = False
        self.player1 = 0
        self.player2 = 0
        self.prev_moves = []
        self.movesound = pygame.mixer.Sound('ChessClick.wav')
        # self.board_change = false could be used to determine if change occured? 
        # classification for differentiating pieces
        # White: Pawn = 1, Knight = 2, Rook = 3, Bishop = 4, Queen = 5, King = 6
        # Black: Pawn = 11, Knight = 12, Rook = 13, Bishop = 14, Queen = 15, King = 16
        self.board = [
            [13, 12, 14, 15, 16, 14, 12, 13],
            [11, 11, 11, 11, 11, 11, 11, 11],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 1,  1,  1,  1,  1,  1,  1,  1],
            [ 3,  2,  4,  5,  6,  4,  2,  3]
        ]
        self.white_pawn_position_values = [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]

        self.black_pawn_position_values = reverse_list(self.white_pawn_position_values)   

        self.white_knight_position_values = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]

        self.black_knight_position_values = reverse_list(self.white_knight_position_values)

        self.white_king_position_values =   [
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
        [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
        ]
        
        self.black_king_position_values = reverse_list(self.white_king_position_values)

        self.white_queen_position_values = [
        [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
        [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]

        self.black_queen_position_values = reverse_list(self.white_queen_position_values)

        self.white_rook_position_values = [
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
        ]

        # False = hasn't moved; [TopL, TopR, BotL, BotR]
        self.track_castling = {'TopL': False, 'TopR': False, 'BotL': False, 'BotR': False, 'King1': False, 'King2': False}  
        self.black_rook_position_values = reverse_list(self.white_rook_position_values)
        
        self.white_bishop_position_values = [
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
        [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
        ]
        self.black_bishop_position_values = reverse_list(self.white_bishop_position_values)    
    #takes in the piece remove piece to calculate the score and the player to add the points to

    def point_counter(self, piece, cur_score):
        piece_num = piece
        point_dict = {1:1, 2:3, 4:3, 3:5, 5:9}
        if piece_num > 10:
            piece_num = piece_num - 10
        cur_score = cur_score + point_dict[piece_num]
        return cur_score

    def make_move(self, from_dict, to_dict):
        #print(self.get_valid_moves())
        self.board[ from_dict['y'] ][ from_dict['x'] ] = 0
        self.board[ to_dict['y'] ][ to_dict['x'] ] = from_dict['piece']

        self.prev_moves.append((from_dict, to_dict, copy.deepcopy(self.track_castling)))

        #if kings move keep track where they move to.
        if(from_dict['piece'] == 6):
            self._white_king = ([to_dict['y'], to_dict['x']])
        if(from_dict['piece'] == 16):
            self._black_king = ([to_dict['y'], to_dict['x']])
        

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
                if target['y'] + 1 == select['y'] and target['piece'] == 0:
                    return True
                elif (target['y'] + 2 == select['y'] and select['y'] == 6 and
                      self.board[ select['y'] - 1 ][ select['x'] ] == 0 and target['piece'] == 0):
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
                if target['y'] - 1 == select['y'] and target['piece'] == 0:
                    return True
                elif (target['y'] - 2 == select['y'] and select['y'] == 1 and
                      self.board[ select['y'] + 1 ][ select['x'] ] == 0 and target['piece'] == 0):
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
                    if select['piece'] == 1 and self.player == 1:
                        # forward moves
                        if self.is_valid_move( select, (up, x) ):
                            moves.append(((select['y'], select['x']),
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
                    if select['piece'] == 11 and self.player == 2:
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
                    if select['piece'] is 2 and self.player == 1:
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

                    if select['piece'] is 12 and self.player == 2:
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
                    if select['piece'] in (3, 5) and self.player == 1:

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

                    if select['piece'] in ( 13, 15) and self.player == 2:

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
                    if select['piece'] in (14, 15) and self.player == 2:

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

                    # Bishops and Queens' diagonal moves
                    if select['piece'] in (4, 5 ) and self.player == 1:

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
                    if select['piece'] is 16 and self.player == 2:
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
                
                    # Kings
                    if select['piece'] is 6 and self.player == 1:
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

                    # Castling Rules:
                    # Cannot castle when in check (TODO)
                    # Cannot castle when result leads to a check (taken care of by further_validation)
                    # Rook and King never moved at all (checked below)
                    # Space between Rook and King are empty (checked below)
                    # Castling does not move through a check - so no enemy moves in spaces between Rook and King (can be added to further_validation)
                    can_castle = True
                    if self.player == 1:
                        if select['piece'] == 3 and self.track_castling['King1'] == False:
                            if self.track_castling['BotL'] == False:
                                # check if space between BotL rook and King1 is empty
                                can_castle = True
                                for x in range(1, 4):
                                    if self.board[7][x] != 0:
                                        can_castle = False
                                
                                if can_castle:
                                    # user drops rook on king or king on rook
                                    moves.append( ((7, 0), (7, 4)) )
                                    moves.append( ((7, 4), (7, 0)) )

                            if self.track_castling['BotR'] == False:
                                # check if space between King1 and BotR rook is empty
                                can_castle = True
                                for x in range(5, 7):
                                    if self.board[7][x] != 0:
                                        can_castle = False
                                
                                if can_castle:
                                    # user drops rook on king or king on rook
                                    moves.append( ((7, 4), (7, 7)) )
                                    moves.append( ((7, 7), (7, 4)) )

                    if self.player == 2:
                        if select['piece'] == 13 and self.track_castling['King2'] == False:
                            if self.track_castling['TopL'] == False:
                                # check if space between TopL rook and Top1 is empty
                                can_castle = True
                                for x in range(1, 4):
                                    if self.board[0][x] != 0:
                                        can_castle = False
                                
                                if can_castle:
                                    # user drops rook on king or king on rook
                                    moves.append( ((0, 0), (0, 4)) )
                                    moves.append( ((0, 4), (0, 0)) )

                            if self.track_castling['TopR'] == False:
                                # check if space between King2 and TopR rook is empty
                                can_castle = True
                                for x in range(5, 7):
                                    if self.board[0][x] != 0:
                                        can_castle = False
                                
                                if can_castle:
                                    # user drops rook on king or king on rook
                                    moves.append( ((0, 4), (0, 7)) )
                                    moves.append( ((0, 7), (0, 4)) )

        return moves

    def undo_move(self):
        self.board[self.prev_moves[-1][0]['y']][self.prev_moves[-1][0]['x']] = self.prev_moves[-1][0]['piece']
        self.board[self.prev_moves[-1][1]['y']][self.prev_moves[-1][1]['x']] = self.prev_moves[-1][1]['piece']

        self.track_castling = copy.deepcopy(self.prev_moves[-1][2])

        if(self.prev_moves[-1][0]['piece'] == 6):
            self._white_king = (self.prev_moves[-1][0]['y'], self.prev_moves[-1][0]['x'])
        if(self.prev_moves[-1][0]['piece']== 16):
            self._black_king = (self.prev_moves[-1][0]['y'], self.prev_moves[-1][0]['x'])
        
        self.prev_moves.pop()

    #This function takes the moves from get valid moves and further validates them.
    def further_validation(self, moves):
        for x in range(len(moves)-1, -1, -1):
            selected_piece = self.board[moves[x][0][0]][moves[x][0][1]]
            target_piece = self.board[moves[x][1][0]][moves[x][1][1]]
            selected = {
                'piece' : selected_piece,
                'y' : moves[x][0][0],
                'x' : moves[x][0][1]
            }
            targeted = {
                'piece' : target_piece,
                'y' : moves[x][1][0],
                'x' : moves[x][1][1]
            }
            self.make_move(selected, targeted)

            if self.check():
                moves.remove(moves[x])
            
            self.undo_move()

        return moves

    def find_king(self):
        for i in range(0,8):
            for j in range(0,8):
                if(self.board[i][j] == 6):
                    self._white_king = (i,j)
                elif self.board[i][j] == 16:
                    self._black_king = (i,j)

    def get_opponent_moves(self):
        # Get opponent's moves
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
        
        moves = self.get_valid_moves()

        # Switch back players
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

        return moves

    def check(self):
        moves = self.get_opponent_moves()

        if self.player == 1:
            king = self._white_king
        else:
            king = self._black_king

        for move in moves:
            if(move[1][0] == king[0] and move[1][1] == king[1]):
                return True
        
        return False

    def advanced_evaluation(self):
        
        evaluation = 0

        counter_row = 0
        for x in self.board:
            counter_column = 0
            for y in x:
                if y == 1:
                    value = 10 + self.white_pawn_position_values[counter_row][counter_column]
                    evaluation += value 
                    
                elif y == 11:
                    value = 10 + self.black_pawn_position_values[counter_row][counter_column]
                    evaluation -= value
                   
                elif y == 2:
                    value = 30 + self.white_knight_position_values[counter_row][counter_column]
                    evaluation += value
                    
                elif y == 12:
                    value = 30 + self.black_knight_position_values[counter_row][counter_column]
                    evaluation = evaluation - value
                   
                elif y == 3:
                    value = 50 + self.white_rook_position_values[counter_row][counter_column]
                    evaluation = evaluation + value 
                  
                elif y == 13:
                    value = 50 + self.black_rook_position_values[counter_row][counter_column]
                    evaluation = evaluation - value 
                  
                elif y == 4:
                    value = 30 + self.white_bishop_position_values[counter_row][counter_column]
                    evaluation = evaluation + value
                    
                elif y == 14:
                    value = 30 + self.black_bishop_position_values[counter_row][counter_column]
                    evaluation = evaluation - value 
                  
                elif y == 5:
                    value = 90 + self.white_queen_position_values[counter_row][counter_column]
                    evaluation = evaluation + value
                   
                elif y == 15:
                    value = 90 + self.black_queen_position_values[counter_row][counter_column]
                    evaluation = evaluation - value
                   
                elif y == 6:
                    value = 900 + self.white_king_position_values[counter_row][counter_column]
                    evaluation = evaluation + value 
                   
                elif y == 16:
                    value = 900 + self.black_king_position_values[counter_row][counter_column]
                    evaluation = evaluation - value 
                    
                counter_column += 1
            counter_row += 1
        return evaluation
    

    def actions(self):
        actions = self.get_valid_moves()
        actions = self.further_validation(actions)
        return actions


    def terminal_test(self):
        available_moves = self.get_valid_moves()
        available_moves = self.further_validation(available_moves)
        if self.check() == True:
            
            if(len(available_moves) == 0):
                return True
        
        if(len(available_moves) == 0):
                return True
        
        return False
        
    def get_piece_dict(self, row, column):
        piece = self.board[row][column]
        piece_dict = {
            'piece' : piece,
            'y'     : row,
            'x'     : column   
        }
        return piece_dict

def reverse_list(state):
    reverse = []
    for x in range(len(state)-1, -1, -1 ):
        reverse.append(state[x])
    return reverse