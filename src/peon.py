from pieza import Pieza
class Peon(Pieza):
    def __init__(self, color):
        super().__init__('Peon', color)
        self.ascii_symbol = 'X'
        self.available_direction = "Up"
    
    def is_valid_move(self,x,y) -> bool:
        movementvalue = 1
        if self.available_direction == "Down":
            movementvalue = -abs(movementvalue)
        if self.x_location == x and y == self.y_location + movementvalue:
            return True
        else: return False

