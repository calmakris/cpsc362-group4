

class Chess():

    def __init__(self):
        black_points = 0
        white_points = 0
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
    
