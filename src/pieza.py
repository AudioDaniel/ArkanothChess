from event import post_event
from exceptions.invalid_move import InvalidMoveException

class Pieza:
    available_direction = "Up"
    x_location : int = None
    y_location : int = None
    
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.ascii_symbol : chr = None

    def move(self, x,y):
        """
        Move the piece to a new position.
        :x: x index location
        :y: y index location
        """
        if not self.is_valid_move(x,y):
            raise InvalidMoveException("Invalid move.")
        self.x_location = x
        self.y_location = y
        post_event("piece_movement", self)

    def is_valid_move(self,x,y) -> bool:
        raise NotImplementedError("This method should be implemented in a subclass.")
    
    def is_valid_attack_move(self,x,y) -> bool:
        raise NotImplementedError("This method should be implemented in a subclass.")
    