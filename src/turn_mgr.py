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

    def __init__(self, gameboard: Gameboard, my_color="Green", network_manager=None):
        self.gameboard = gameboard
        self.current_turn_color = "Green"
        self.movs_per_turn: int = 1
        self.computer = Computer()
        self.winner = None
        self.my_color = my_color
        self.network_manager = network_manager

    def turn_loop(self):
        """
        The main game loop. Runs until a winner is determined.
        """
        while self.winner == None:
            self.start_turn()
            self.win_conditions()
        print(f"Player {self.winner} wins!")

    def local_turn_logic(self, color):
        """
        Executes the logic for the local player's turn.
        Handles piece selection and movement/attack.
        """
        print(f"{color}'s turn (You)")
        piece_coords = UserInteraction.select_square("Choose a piece to move (e.g. 'A1'): ")
        piece = self.gameboard.get_piece_by_coordinates(piece_coords[0],piece_coords[1])
        while not self.gameboard.is_valid_piece(color, piece):
            print("Invalid piece. Choose a correct piece.")
            piece_coords = UserInteraction.select_square("Choose a piece to move (e.g. 'A1'): ")
            piece = self.gameboard.get_piece_by_coordinates(piece_coords[0],piece_coords[1])

        piece.selected = True
        print(self.gameboard)

        # Save start coordinates for network transmission
        start_x, start_y = piece.x_location, piece.y_location

        destination_coords = UserInteraction.select_square("Choose where to move (e.g. 'A1'): ")

        action_result = self.move_or_attack(piece, destination_coords)
        while not action_result:
            print("Invalid move. Choose a correct destination.")
            destination_coords = UserInteraction.select_square("Choose where to move (e.g. 'A1'): ")
            action_result = self.move_or_attack(piece, destination_coords)

        piece.selected = False

        if self.network_manager:
            self.network_manager.send_action(action_result, (start_x, start_y), destination_coords)

    def network_turn_logic(self, color):
        """
        Waits for and executes a move from the network opponent.
        """
        print(f"{color}'s turn (Opponent)... Waiting for move.")
        action = self.network_manager.receive_action()
        if not action:
            print("Connection lost.")
            self.winner = "Disconnection" # Terminate loop
            return

        start = action["start"]
        end = action["end"]
        piece = self.gameboard.get_piece_by_coordinates(start[0], start[1])

        print(f"Opponent moved piece from {chr(ord('A') + start[0])}{start[1]+1} to {chr(ord('A') + end[0])}{end[1]+1}")

        if action["type"] == "attack":
             self.gameboard.attack_piece(piece, end[0], end[1])
        elif action["type"] == "move":
             self.gameboard.move_piece(piece, end[0], end[1])

    def move_or_attack(self, piece, destination_coords):
        """
        Attempts to move or attack with a piece.
        :param piece: The piece to move or attack with.
        :param destination_coords: The target coordinates.
        :return: "move", "attack" if successful, None otherwise.
        """
        x, y = destination_coords

        # Check if attack is valid
        if piece.is_valid_attack_move(x, y):
             try:
                 self.gameboard.attack_piece(piece, x, y)
                 return "attack"
             except InvalidMoveException:
                 pass

        # Check if move is valid
        if piece.is_valid_move(x, y):
            try:
                self.gameboard.move_piece(piece, x, y)
                return "move"
            except InvalidMoveException:
                pass

        return None

    def start_turn(self):
        """
        Starts a new turn, notifying listeners and executing turn logic for player or computer.
        """
        print("--------\n")
        print(self.gameboard)
        print("--------\n")

        event_manager.post_event("turn_start",self)

        for x in range(self.movs_per_turn):
            if self.network_manager:
                if self.current_turn_color == self.my_color:
                    self.local_turn_logic(self.current_turn_color)
                else:
                    self.network_turn_logic(self.current_turn_color)
            else:
                # Default Single Player: Green is user, Red is Computer
                if self.current_turn_color == "Green":
                    self.local_turn_logic("Green")
                else:
                    print("Computer's turn")
                    self.computer.turn_logic(self.gameboard)

        # Switch turn
        self.current_turn_color = "Red" if self.current_turn_color == "Green" else "Green"

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
