from event import post_event
from exceptions.invalid_move import InvalidMoveException

class Piece:
    # +1 or -1 depdening on the direction of the piece (Green go up, Red go down)
    direction : int = 1
    x_location : int = None
    y_location : int = None
    
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.ascii_symbol : chr = None
        self.color_code = self.get_color_code(color)
        self.configure_direction()
        self.selected = False

    def configure_direction(self):
        if self.color == 'Green':
            self.direction = 1
        elif self.color == 'Red':
            self.direction = -1
        else:
            raise ValueError("Invalid color.")

    def get_color_code(self, color):
        # ANSI Color codes to print on the terminal
        if color == 'Green':
            return '\033[92m'  # Green
        elif color == 'Red':
            return '\033[91m'  # Red
        else:
            return '\033[0m'   # Default

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

    def attack(self, x,y):
        """
        Attack a piece in a position.
        :x: x index location
        :y: y index location
        """
        if not self.is_valid_attack_move(x,y):
            raise InvalidMoveException("Invalid attack move.")
        self.x_location = x
        self.y_location = y
        post_event("piece_attack", self)

    def is_valid_move(self,x,y) -> bool:
        raise NotImplementedError("This method should be implemented in a subclass.")
    
    def is_valid_attack_move(self,x,y) -> bool:
        raise NotImplementedError("This method should be implemented in a subclass.")

    def __repr__(self):
        if self.selected:
            return f"\033[93m{self.ascii_symbol}\033[0m"
        return f"{self.color_code}{self.ascii_symbol}\033[0m"