from gameboard import Gameboard
from random import random
from exceptions.invalid_move import InvalidMoveException

class Computer:
    """
    Implements a simple computer opponent.
    """
    # Simple computer algorithm that moves a piece randomly
    def __init__(self):
        pass
    
    def move_piece_logic(self,gameboard : Gameboard) -> bool:
        """
        Attempts to move a random piece to a random valid location.
        :param gameboard: The current gameboard.
        :return: True if a move was successful, False otherwise.
        """
        computer_pieces = gameboard.get_pieces_by_color("Red")
        if not computer_pieces:
            return False

        # Shuffle pieces to try random ones
        import random as rand
        rand.shuffle(computer_pieces)

        for random_piece in computer_pieces:
            available_moves = gameboard.get_available_moves(random_piece)
            if len(available_moves) == 0:
                continue

            random_move = available_moves[int(random()*len(available_moves))]
            try:
                gameboard.move_piece(random_piece, random_move[0], random_move[1])
                return True
            except InvalidMoveException:
                continue

        return False
    
    def attack_piece_logic(self,gameboard : Gameboard) -> bool:
        """
        Attempts to attack with a random piece.
        :param gameboard: The current gameboard.
        :return: True if an attack was successful, False otherwise.
        """
        computer_pieces = gameboard.get_pieces_by_color("Red")
        if not computer_pieces:
            return False

        import random as rand
        rand.shuffle(computer_pieces)

        for random_piece in computer_pieces:
            available_moves = gameboard.get_available_attack_moves(random_piece)
            if len(available_moves) == 0:
                continue

            random_move = available_moves[int(random()*len(available_moves))]

            # The get_available_attack_moves already filters for enemy pieces in our new Gameboard logic?
            # Let's check. Yes, I added checks there. But let's be safe.

            try:
                gameboard.attack_piece(random_piece, random_move[0], random_move[1])
                return True
            except InvalidMoveException:
                continue

        return False
    
    def is_valid_attack_location(self,gameboard : Gameboard, x : int, y : int,piece) -> bool:
        """
        Checks if a location is a valid target for an attack.
        :param gameboard: The current gameboard.
        :param x: x coordinate of the target.
        :param y: y coordinate of the target.
        :param piece: The attacking piece.
        :return: True if the location contains an enemy piece, False otherwise.
        """
        return not gameboard.is_square_empty(x,y) and not gameboard.is_piece_same_color(
            piece,gameboard.get_piece_by_coordinates(x,y))

    def turn_logic(self,gameboard : Gameboard) -> bool:
        """
        Executes the computer's turn logic.
        Prioritizes attacking over moving.
        :param gameboard: The current gameboard.
        :return: True if the computer took an action.
        """
        # If not possible to eat a piece then move a piece, basic violent approach algorithm
        if not self.attack_piece_logic(gameboard):
            if (self.move_piece_logic(gameboard)):
                return True
        else: return True
