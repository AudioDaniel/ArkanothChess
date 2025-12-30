from event_manager import event_manager
from user_interaction import UserInteraction
from computer import Computer
from gameboard import Gameboard
from exceptions.invalid_move import InvalidMoveException

# Controls the game loop and turn order
class TurnManager():
    """
    Manages the game turns, including player and computer turns, and checking win conditions.
    """

    def __init__(self, gameboard: Gameboard):
        self.gameboard = gameboard
        self.player_turn : bool = True
        self.movs_per_turn: int = 1
        self.computer = Computer()  
        self.winner = None

    def turn_loop(self):
        """
        The main game loop. Runs until a winner is determined.
        """
        while self.winner == None:
            self.start_turn()
            self.win_conditions()
        print(f"Player {self.winner} wins!")

    def player_turn_logic(self):
        """
        Executes the logic for the player's turn.
        Handles piece selection and movement/attack.
        """
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

    def move_or_attack(self, piece, destination_coords) -> bool:
        """
        Attempts to move or attack with a piece.
        :param piece: The piece to move or attack with.
        :param destination_coords: The target coordinates.
        :return: True if the move or attack was successful, False otherwise.
        """
        x, y = destination_coords

        # Try attack first (assuming user intent based on context? Or checks validity)
        # Actually we should check what is valid.

        # Check if attack is valid
        if piece.is_valid_attack_move(x, y):
             try:
                 self.gameboard.attack_piece(piece, x, y)
                 return True
             except InvalidMoveException:
                 pass # Fall through to move check? Or just fail?

        # Check if move is valid
        if piece.is_valid_move(x, y):
            try:
                self.gameboard.move_piece(piece, x, y)
                return True
            except InvalidMoveException:
                pass

        return False

    def start_turn(self):
        """
        Starts a new turn, notifying listeners and executing turn logic for player or computer.
        """
        # We manually print the board for now, since we removed the event handler in Gameboard
        # Or we can post the event and have a View handle it.
        # But we haven't implemented a View class yet.
        # Let's print it here to keep behavior consistent.
        print("--------\n")
        print(self.gameboard)
        print("--------\n")

        event_manager.post_event("turn_start",self)
        for x in range(self.movs_per_turn):
            if self.player_turn:
                self.player_turn_logic()
            else:
                print("Computer's turn")
                self.computer.turn_logic(self.gameboard)
        self.player_turn = not self.player_turn

    def win_conditions(self) -> bool:
        """
        Checks if the win conditions are met.
        :return: True if a winner is found, False otherwise.
        """
        if len(self.gameboard.get_pieces_by_color("Red")) == 0:
            self.winner = "Green"
            return True
        if len(self.gameboard.get_pieces_by_color("Green")) == 0:
            self.winner = "Red"
            return True
        else: return False
