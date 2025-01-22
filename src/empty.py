from pieza import Pieza
# Represents an empty square on the board.
class Empty(Pieza):
    def __init__(self):
        self.name = "Empty"
        self.color = "Empty"
        self.ascii_symbol = '□'