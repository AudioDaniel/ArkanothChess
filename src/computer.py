from gameboard import Gameboard
from random import random

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
        random_piece = computer_pieces[int(random()*len(computer_pieces))]
        available_moves = gameboard.get_available_moves(random_piece)
        if len(available_moves) == 0:
            return False
        random_move = available_moves[int(random()*len(available_moves))]
        random_piece.move(random_move[0],random_move[1])
        return True
    
    def attack_piece_logic(self,gameboard : Gameboard) -> bool:
        """
        Attempts to attack with a random piece.
        :param gameboard: The current gameboard.
        :return: True if an attack was successful, False otherwise.
        """
        computer_pieces = gameboard.get_pieces_by_color("Red")
        random_piece = computer_pieces[int(random()*len(computer_pieces))]
        available_moves = gameboard.get_available_attack_moves(random_piece)
        if len(available_moves) == 0:
            return False
        random_move = available_moves[int(random()*len(available_moves))]
        while not self.is_valid_attack_location(gameboard,random_move[0],random_move[1],random_piece):
            available_moves.remove(random_move)         
            if len(available_moves) == 0:
                return False
            random_move = available_moves[int(random()*len(available_moves))]
        random_piece.attack(random_move[0],random_move[1])
        return True
    
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
        else: return False
