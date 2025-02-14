from pieces.piece import Piece
# Represents an empty square on the board.
class Empty(Piece):
    def __init__(self):
        self.name = "Empty"
        self.color = "Empty"
        self.ascii_symbol = '□'
        self.color_code = '\033[0m'
        self.selected = False