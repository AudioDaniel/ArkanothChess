from pieza import Pieza
class Guerrero(Pieza):
    def __init__(self, color):
        super().__init__('Guerrero', color)
        self.ascii_symbol = 'G'