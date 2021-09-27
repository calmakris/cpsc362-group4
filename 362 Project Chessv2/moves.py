import pygame, sys, time, math, copy, chess, os

#TODO: Create function for valid lateral & diagonal moves (given move limit)

# Given a selected piece and destination of move info (coord and piece at coord)
# Returns true/false if valid move
# x coord is left/right while y coord is top/bottom of the board
def is_valid_move(self, selected, destination):
    # TODO: need to pass a value for selected & destination to this function

    # Do not allow move if player's own piece is in destination
    # except castling (TODO)
    destinationID = self.game.board[destination['y']][destination['x']]
    if 0 < selected['pieceID'] <= 6 and 0 < destinationID <= 6:
        return False
    elif selected['pieceID'] >= 11 and destinationID >= 11:
        return False

    # TODO: Do we need to check here if destination is within the board?

    # Pawns (bottom)    --------------------------------------------------------------------------
    if selected['pieceID'] == 1:

        # forward 1
        if destination['x'] == selected['x'] and destination['y'] + 1 == selected['y']:
            return True

        # forward 2 from 7th row of board
        elif (destination['x'] == selected['x'] and 
            destination['y'] + 2 == selected['y'] and selected['y'] == 6):
            if self.game.board[selected['y'] - 1][selected['x']] != 0:
                return False
            else:
                return True

        # diagonal attacks
        elif (destination['y'] + 1 == selected['y'] and
            (destination['x'] + 1 == selected['x'] or destination['x'] - 1 == selected['x']) and
            destinationID >= 11):
            return True

    # Pawns (top)       --------------------------------------------------------------------------
    if selected['pieceID'] == 11:

        # forward 1
        if destination['x'] == selected['x'] and destination['y'] - 1 == selected['y']:
            return True

        # forward 2 from 2nd row of board
        elif (destination['x'] == selected['x'] and 
            destination['y'] - 2 == selected['y'] and selected['y'] == 1):
            #TODO: check for obstruction
            if self.game.board[selected['y'] + 1][selected['x']] != 0:
                return False
            else:
                return True

        # diagonal attacks
        elif (destination['y'] - 1 == selected['y'] and
            (destination['x'] + 1 == selected['x'] or destination['x'] - 1 == selected['x']) and
            destinationID <= 6):
            return True

    # Rooks & Queens    --------------------------------------------------------------------------
    if (selected['pieceID'] == 3 or selected['pieceID'] == 13 or
        selected['pieceID'] == 5 or selected['pieceID'] == 15):

        # up/down moves
        if destination['x'] == selected['x']:
            return True
            
        # left/right moves
        elif destination['y'] == selected['y']:
            return True

    # Bishops & Queens  --------------------------------------------------------------------------
    if (selected['pieceID'] == 2 or selected['pieceID'] == 12 or
        selected['pieceID'] == 5 or selected['pieceID'] == 15):

        # diagonal moves: x_movement == y_movement
        if (destination['x'] - selected['x']) == (destination['y'] - selected['y']):
            return True

    # Kings             --------------------------------------------------------------------------
    if selected['pieceID'] == 6 or selected['pieceID'] == 16:

        # movement in every direction should be 1
        if (abs(destination['x'] - selected['x']) == 1 and 
            abs(destination['x'] - selected['x']) == 1):
            return True

    # Knights           --------------------------------------------------------------------------
    if selected['pieceID'] == 2 or selected['pieceID'] == 12:

        # 2-1 moves: 2x,1y or 2y,1x; obstruction check not necessary
        if ((abs(destination['x'] - selected['x']) == 2 and abs(destination['y'] - selected['y']) == 1) or
            (abs(destination['y'] - selected['y']) == 2 and abs(destination['x'] - selected['x']) == 1)):
            return True

    return False

def generate_moves(self):
    moves = []

    for y in range(0, 8):
        for x in range(0, 8):

            piece = self.game.board[y][x]
            selected = (piece , (y, x))
            up = (y - 1) % 8
            down = (y + 1) % 8
            right = (x + 1) % 8
            left = (x - 1) % 8

            # White Pawns
            if piece == 1: 
                new_y = up
                # Forward 1 & 2 moves
                if is_valid_move( selected, (new_y, x) ):
                    moves.push( (piece, (new_y, x)) )

                    # Forward 2 move check on starting row
                    new_y = (y - 2) % 8
                    if y == 6 and is_valid_move( selected, (new_y, x) ):
                        moves.push( (piece , (new_y, x)) )

                # Diagonal captures
                if is_valid_move( selected, (up, left) ):
                    moves.push( (piece , (up, left) ) )
                if is_valid_move( selected, (up, right) ):
                    moves.push( (piece , (up, right) ) )

            # Black Pawns
            if piece == 11: 
                new_y = down
                # Forward 1 & 2 moves
                if is_valid_move( selected, (new_y, x) ):
                    moves.push( (piece, (new_y, x)) )

                    # Forward 2 move check on starting row
                    new_y = (y + 2) % 8
                    if y == 6 and is_valid_move( selected, (new_y, x) ):
                        moves.push( (piece , (new_y, x)) )

                # Diagonal captures
                if is_valid_move( selected, (down, left) ):
                    moves.push( (piece , (up, right) ) )
                if is_valid_move( selected, (down, right) ):
                    moves.push( (piece , (down, right) ) )

            # Rooks & Queens (lateral moves)
            if piece == 3 or piece == 13 or piece == 5 or piece == 15:
                # vertical moves
                for upOne in range(y, -1, -1):
                    if is_valid_move( selected, (upOne, x) ):
                        moves.push( (piece, (upOne, x)) )
                    else:
                        break

                for downOne in range(y, 8):
                    if is_valid_move( selected, (downOne, x) ):
                         moves.push( (piece, (downOne, x) ) )
                    else:
                        break
                
                # horizontal moves
                for leftOne in range(x, -1, -1):
                    if is_valid_move( selected, (y, leftOne)):
                        moves.push( (piece, (y, leftOne)) )
                    else:
                        break

                for rightOne in range(x, 8):
                    if is_valid_move( selected, (y, rightOne)):
                        moves.push( (piece, (y, rightOne)) )
                    else:
                        break
            
            # Bishops & Queens (diagonal moves)
            if piece == 2 or piece == 12 or piece == 5 or piece == 15:
                # Towards top right
                new_y = up
                new_x = right
                while new_y >= 0 and new_x < 8:
                    if is_valid_move( selected, (new_y, new_x) ):
                        moves.push( (piece, (new_y, new_x) ) )
                    else:
                        break

                    new_y -= 1
                    new_x += 1

                # Towards bottom right
                new_y = down
                new_x = right

                while new_y < 8 and new_x < 8:
                    if is_valid_move( selected, (new_y, new_x) ):
                        moves.push( (piece, (new_y, new_x) ) )
                    else:
                        break

                    new_y += 1
                    new_x += 1

                # Towards top left
                new_y = up
                new_x = left

                while new_y >= 0 and new_x >= 0:
                    if is_valid_move( selected, (new_y, new_x) ):
                        moves.push( (piece, (new_y, new_x) ) )
                    else:
                        break

                    new_y -= 1
                    new_x -= 1

                # Towards bottom left
                new_y = down
                new_x = left

                while new_y < 8 and new_x >= 0:
                    if is_valid_move( selected, (new_y, new_x) ):
                        moves.push( (piece, (new_y, new_x) ) )
                    else:
                        break

                    new_y += 1
                    new_x -= 1

            # Kings
            if piece == 6 or piece == 16:
                if is_valid_move( selected, (up, x) ): # Up 1
                    moves.push( (piece, (up, x)) )
                if is_valid_move( selected, (down, x) ): # Down 1
                    moves.push( (piece, (down, x)) )
                if is_valid_move( selected, (y, right) ): # Right 1
                    moves.push( (piece, (y, right)) )
                if is_valid_move( selected, (y, left) ): # Left 1
                    moves.push( (piece, (y, left)) )
                if is_valid_move( selected, (up, right) ): # Up-Right 1
                    moves.push( (piece, (up, right)) )
                if is_valid_move( selected, (down, right) ): # Down-Right 1
                    moves.push( (piece, (down, right)) )
                if is_valid_move( selected, (up, left) ): # Up-Left 1
                    moves.push( (piece, (up, left)) )
                if is_valid_move( selected, (down, left) ): # Down-Left 1
                    moves.push( (piece, (down, left)) )

            # Knights
            if piece == 2 or piece == 12:
                # Forward 2, left/right 1
                new_y = (y - 2) % 8
                if is_valid_move( selected, (new_y, right) ):
                    moves.push( (piece, (new_y, right)) )
                if is_valid_move( selected, (new_y, left) ):
                    moves.push( (piece, (new_y, left)) )
                
                # Down 2, left/right 1
                new_y = (y + 2) % 8
                if is_valid_move( selected, (new_y, right) ):
                    moves.push( (piece, (new_y, right)) )
                if is_valid_move( selected, (new_y, left) ):
                    moves.push( (piece, (new_y, left)) )

                # Right 2, up/down 1
                new_x = (x + 2) % 8
                if is_valid_move( selected, (up, new_x) ):
                    moves.push( (piece, (up, new_x)) )
                if is_valid_move( selected, (down, new_x) ):
                    moves.push( (piece, (down, new_x)) )

                # Left 2, up/down 1
                new_x = (x - 2) % 8
                if is_valid_move( selected, (up, new_x) ):
                    moves.push( (piece, (up, new_x)) )
                if is_valid_move( selected, (down, new_x) ):
                    moves.push( (piece, (down, new_x)) )

    return moves
