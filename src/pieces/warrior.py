from pieces.piece import Piece
class Warrior(Piece):
    def __init__(self, color):
        super().__init__('Warrior', color)
        self.ascii_symbol = 'G'