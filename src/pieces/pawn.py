from pieces.piece import Piece
class Pawn(Piece):
    """
    Represents a Pawn piece.
    """
    def __init__(self, color):
        super().__init__('Pawn', color)
        self.ascii_symbol = 'X'
    
    def is_valid_move(self,x,y) -> bool:
        """
        Check if the pawn move is valid.
        Pawns move one square forward.
        """
        movementvalue = 1 * self.direction
        if self.x_location == x and y == self.y_location + movementvalue:
            return True
        else: return False

    def is_valid_attack_move(self, x, y) -> bool:
        """
        Check if the pawn attack move is valid.
        Pawns attack diagonally forward.
        """
        movementvalue = 1 * self.direction
        if x == self.x_location + movementvalue and y == self.y_location + movementvalue:
            return True
        if x == self.x_location - movementvalue and y == self.y_location + movementvalue:
            return True        
        else: return False

