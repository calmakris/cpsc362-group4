import pygame, sys, time, math, copy, chess, os

#TODO: Create function for valid lateral & diagonal moves (given move limit)

# Given a selected piece and destination of move info (coord and piece at coord)
# Returns true/false if valid move
# x coord is left/right while y coord is top/bottom of the board
def IsValidMove(self, selected, destination):
    # TODO: need to pass a value for selected & destination to this function

    # Do not allow move if player's own piece is in destination
    # except castling (TODO)
    if selected['pieceID'] <= 6 and destination['pieceID'] <= 6:
        return False
    elif selected['pieceID'] >= 11 and destination['pieceID'] >= 11:
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
            (destination['x'] + 1 == selected['x'] or destination['x'] - 1 == selected['x'])):
            #TODO: check if there's something to attack on destination
            return True

    # Pawns (top)       --------------------------------------------------------------------------
    elif selected['pieceID'] == 11:

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
            (destination['x'] + 1 == selected['x'] or destination['x'] - 1 == selected['x'])):
            #TODO: check if there's something to attack on destination
            return True

    # Rooks             --------------------------------------------------------------------------
    elif selected['pieceID'] == 3 or selected['pieceID'] == 13:

        # up/down moves
        if destination['x'] == selected['x']:
            # check for obstruction
            start = min(destination['y'], selected['y'])
            end = max(destination['y'], selected['y'])

            for y in range(start + 1, end):
                if self.game.board[y][destination['x']] != 0:
                    return False

            return True
            
        # left/right moves
        elif destination['y'] == selected['y']:
            # check for obstruction
            start = min(destination['x'], selected['x'])
            end = max(destination['x'], selected['x'])

            for x in range(start + 1, end):
                if self.game.board[destination['y']][x] != 0:
                    return False

            #TODO: Castling :(

            return True

    # Bishops           --------------------------------------------------------------------------
    elif selected['pieceID'] == 2 or selected['pieceID'] == 12:

        # diagonal moves: x_movement == y_movement
        if (destination['x'] - selected['x']) == (destination['y'] - selected['y']):
            # TODO: check for obstruction
            return True

    # Kings             --------------------------------------------------------------------------
    elif selected['pieceID'] == 6 or selected['pieceID'] == 16:

        # movement in every direction should be 1
        if (abs(destination['x'] - selected['x']) == 1 and 
            abs(destination['x'] - selected['x']) == 1):
            return True

    # Queens            --------------------------------------------------------------------------
    elif selected['pieceID'] == 5 or selected['pieceID'] == 15:
        
        # up/down moves
        if destination['x'] == selected['x']:
            # check for obstruction
            start = min(destination['y'], selected['y'])
            end = max(destination['y'], selected['y'])

            for y in range(start + 1, end):
                if self.game.board[y][destination['x']] != 0:
                    return False

            return True
            
        # left/right moves
        elif destination['y'] == selected['y']:
            # check for obstruction
            start = min(destination['x'], selected['x'])
            end = max(destination['x'], selected['x'])

            for x in range(start + 1, end):
                if self.game.board[destination['y']][x] != 0:
                    return False

            #TODO: Castling :(

            return True

        # diagonal moves: x_movement == y_movement
        if (destination['x'] - selected['x']) == (destination['y'] - selected['y']):
            # TODO: check for obstruction
            return True

    # Knights           --------------------------------------------------------------------------
    elif selected['pieceID'] == 2 or selected['pieceID'] == 12:

        # 2-1 moves: 2x,1y or 2y,1x; obstruction check not necessary
        if ((abs(destination['x'] - selected['x']) == 2 and abs(destination['y'] - selected['y']) == 1) or
            (abs(destination['y'] - selected['y']) == 2 and abs(destination['x'] - selected['x']) == 1)):
            return True

    return False
