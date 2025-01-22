from pieza import Pieza
from empty import Empty
class Square:
    current_piece : Pieza

    def __init__(self,piece : Pieza):
        self.current_piece = piece

    def is_occupied(self):
        if self.current_piece is not None:
            return True
        return False
    
    def __repr__(self):
        return self.current_piece.ascii_symbol
    
