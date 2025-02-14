from pieces.piece import Piece
from pieces.empty import Empty
class Square:
    current_piece : Piece

    def __init__(self,piece : Piece):
        self.current_piece = piece

    def is_occupied(self):
        if self.current_piece is not None:
            return True
        return False
    
    def __repr__(self):
        return f"{self.current_piece}"