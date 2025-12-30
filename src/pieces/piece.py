class Piece:
    """
    Abstract base class for all pieces.
    """
    # +1 or -1 depdening on the direction of the piece (Green go up, Red go down)
    direction : int = 1
    x_location : int = None
    y_location : int = None
    
    def __init__(self, name, color):
        """
        Initialize the piece.
        :param name: Name of the piece.
        :param color: Color of the piece ('Green' or 'Red').
        """
        self.name = name
        self.color = color
        self.ascii_symbol : chr = None
        self.color_code = self.get_color_code(color)
        self.configure_direction()
        self.selected = False

    def configure_direction(self):
        """
        Set the direction of movement based on color.
        Green moves up (1), Red moves down (-1).
        """
        if self.color == 'Green':
            self.direction = 1
        elif self.color == 'Red':
            self.direction = -1
        else:
            raise ValueError("Invalid color.")

    def get_color_code(self, color):
        """
        Get the ANSI color code for the piece.
        :param color: The color of the piece.
        :return: The ANSI color code string.
        """
        # ANSI Color codes to print on the terminal
        if color == 'Green':
            return '\033[92m'  # Green
        elif color == 'Red':
            return '\033[91m'  # Red
        else:
            return '\033[0m'   # Default

    def is_valid_move(self,x,y) -> bool:
        """
        Check if a move is valid for this piece.
        :param x: Target x coordinate.
        :param y: Target y coordinate.
        :return: True if valid, False otherwise.
        """
        raise NotImplementedError("This method should be implemented in a subclass.")
    
    def is_valid_attack_move(self,x,y) -> bool:
        """
        Check if an attack move is valid for this piece.
        :param x: Target x coordinate.
        :param y: Target y coordinate.
        :return: True if valid, False otherwise.
        """
        raise NotImplementedError("This method should be implemented in a subclass.")

    def __repr__(self):
        if self.selected:
            return f"\033[93m{self.ascii_symbol}\033[0m"
        return f"{self.color_code}{self.ascii_symbol}\033[0m"
