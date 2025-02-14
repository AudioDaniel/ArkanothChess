from gameboard import Gameboard
from random import random

class Computer:
    # Simple computer algorithm that moves a piece randomly
    def __init__(self):
        pass
    
    def move_piece_logic(self,gameboard : Gameboard) -> bool:
        computer_pieces = gameboard.get_pieces_by_color("Red")
        random_piece = computer_pieces[int(random()*len(computer_pieces))]
        available_moves = gameboard.get_available_moves(random_piece)
        if len(available_moves) == 0:
            return False
        random_move = available_moves[int(random()*len(available_moves))]
        random_piece.move(random_move[0],random_move[1])
        return True
    
    def attack_piece_logic(self,gameboard : Gameboard) -> bool:
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
        return not gameboard.is_square_empty(x,y) and not gameboard.is_piece_same_color(
            piece,gameboard.get_piece_by_coordinates(x,y))

    def turn_logic(self,gameboard : Gameboard) -> bool:
        # If not possible to eat a piece then move a piece, basic violent approach algorithm
        if not self.attack_piece_logic(gameboard):
            if (self.move_piece_logic(gameboard)):
                return True
        else: return False
