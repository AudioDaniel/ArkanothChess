from piece import Piece
class Warrior(Piece):
    def __init__(self, color):
        super().__init__('Guerrero', color)
        self.ascii_symbol = 'G'