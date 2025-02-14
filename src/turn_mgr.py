from event import subscribe
from event import post_event
from user_interaction import UserInteraction
from computer import Computer
from gameboard import Gameboard

# Controls the game loop and turn order
class TurnManager():

    def __init__(self, gameboard: Gameboard):
        self.gameboard = gameboard
        self.player_turn : bool = True
        self.movs_per_turn: int = 1
        self.computer = Computer()  
        self.winner = None

    def turn_loop(self):
        while self.winner == None:
            self.start_turn()
            self.win_conditions()
        print(f"Player {self.winner} wins!")

    def player_turn_logic(self):
        print("Players's turn")
        piece_coords = UserInteraction.select_square("Choose a piece to move (e.g. 'A1'): ")
        piece = self.gameboard.get_piece_by_coordinates(piece_coords[0],piece_coords[1])
        while not self.gameboard.is_valid_piece("Green",piece):
            print("Invalid piece. Choose a correct piece.")
            piece_coords = UserInteraction.select_square("Choose a piece to move (e.g. 'A1'): ")
            piece = self.gameboard.get_piece_by_coordinates(piece_coords[0],piece_coords[1])
        piece.selected = True
        print(self.gameboard)
        destination_coords = UserInteraction.select_square("Choose where to move (e.g. 'A1'): ")
        while not self.move_or_attack(piece,destination_coords):
            print("Invalid move. Choose a correct destination.")
            destination_coords = UserInteraction.select_square("Choose where to move (e.g. 'A1'): ")
        piece.selected = False

    def move_or_attack(self,piece,destination_coords) -> bool:
        if (piece.is_valid_attack_move(destination_coords[0],destination_coords[1])):
            piece.attack(destination_coords[0],destination_coords[1])
            return True
        if (piece.is_valid_move(destination_coords[0],destination_coords[1])):
            piece.move(destination_coords[0],destination_coords[1])
            return True
        else : return False

    def start_turn(self):
        post_event("turn_start",self)
        for x in range(self.movs_per_turn):
            if self.player_turn:
                self.player_turn_logic()
            else:
                print("Computer's turn")
                self.computer.turn_logic(self.gameboard)
        self.player_turn = not self.player_turn

    def win_conditions(self) -> bool:
        if len(self.gameboard.get_pieces_by_color("Red")) == 0:
            self.winner = "Green"
            return True
        if len(self.gameboard.get_pieces_by_color("Green")) == 0:
            self.winner = "Red"
            return True
        else: return False