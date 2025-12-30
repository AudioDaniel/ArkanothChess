from pieces.piece import Piece

class Magician(Piece):
    """
    Represents a Magician piece.
    """
    def __init__(self, color):
        super().__init__('Magician', color)
        self.ascii_symbol = 'M'

    def is_valid_move(self, x, y) -> bool:
        """
        Check if the move is valid for a Magician.
        Magician moves in an L-shape like a Chess Knight.
        """
        dx = abs(x - self.x_location)
        dy = abs(y - self.y_location)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    def is_valid_attack_move(self, x, y) -> bool:
        """
        Check if the attack move is valid for a Magician.
        Magician attacks in an L-shape like a Chess Knight.
        """
        dx = abs(x - self.x_location)
        dy = abs(y - self.y_location)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
