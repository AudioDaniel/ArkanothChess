from pieces.piece import Piece
class Warrior(Piece):
    """
    Represents a Warrior piece.
    """
    def __init__(self, color):
        super().__init__('Warrior', color)
        self.ascii_symbol = 'G'