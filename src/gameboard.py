from event import subscribe
from pieces.piece import Piece
from square import Square
from pieces.empty import Empty
from pieces.pawn import Pawn
from pieces.warrior import Warrior
class Gameboard:
    def __init__(self,tamanho):
        """
        Initialize the gameboard.
        :param tamanho: Size of the board (tamanho x tamanho).
        """
        self.board : list[list[Piece]] = self.load_board(tamanho)
        self.setup_piece_movement_handlers()
        self.setup_turn_handlers()
        self.deleted_pieces : list = []
        self.setup_piece_attack_handlers()

    def load_board(self,tamanho):
        """
        Create the board grid with empty squares.
        :param tamanho: Size of the board.
        :return: A 2D list representing the board.
        """
        board = []
        for x in range(tamanho):
            row = []
            for y in range(tamanho):
                row.append(Square(Empty()))
            board.append(row)
        return board
    
    def load_standard_pieceset(self):
        """
        Loads the standard set of pieces for a chess game.
        """
        # White pieces
        self.place_piece(Pawn("Green"), 0, 1)
        self.place_piece(Pawn("Green"), 1, 1)
        self.place_piece(Pawn("Green"), 2, 1)
        self.place_piece(Pawn("Green"), 3, 1)
        self.place_piece(Pawn("Green"), 4, 1)
        self.place_piece(Pawn("Green"), 5, 1)
        self.place_piece(Pawn("Green"), 6, 1)
        self.place_piece(Pawn("Green"), 7, 1)
        #self.place_piece(Warrior("Green"), 0, 0)
        #self.place_piece(Warrior("Green"), 7, 0)
        # Black pieces
        self.place_piece(Pawn("Red"), 0, 6)
        self.place_piece(Pawn("Red"), 1, 6)
        self.place_piece(Pawn("Red"), 2, 6)
        self.place_piece(Pawn("Red"), 3, 6)
        self.place_piece(Pawn("Red"), 4, 6)
        self.place_piece(Pawn("Red"), 5, 6)
        self.place_piece(Pawn("Red"), 6, 6)
        self.place_piece(Pawn("Red"), 7, 6)
        #self.place_piece(Warrior("Red"), 0, 7)
        #self.place_piece(Warrior("Red"), 7, 7)

    def find_piece_location(self, piece: Piece):
        """
        Find the position of a piece on the board.
        """
        for i, row in enumerate(self.board):
            for j, square in enumerate(row):
                if square.current_piece == piece:
                    return (i, j)
        return None
    
    def setup_piece_movement_handlers(self):
        """
        Subscribe to piece movement events.
        """
        subscribe("piece_movement", self.handle_piece_movement)

    def setup_piece_attack_handlers(self):
        """
        Subscribe to piece attack events.
        """
        subscribe("piece_attack", self.handle_piece_attack)

    def setup_turn_handlers(self):
        """
        Subscribe to turn start events.
        """
        subscribe("turn_start", self.handle_turn_start)

    def handle_turn_start(self,turn_manager):
        """
        Handle the start of a turn by printing the board.
        :param turn_manager: The turn manager instance (unused in this method but passed by event).
        """
        print("--------\n")
        print(self)
        print("--------\n")
    
    def handle_piece_movement(self, piece: Piece):
        """
        Reacts to a piece movement event.
        """
        # Find the current position of the piece
        current_position = self.find_piece_location(piece)
    
        # Remove the piece from its current position
        if current_position:
            self.board[current_position[0]][current_position[1]].current_piece = Empty()

        # Place the piece at its new position
        self.board[piece.y_location][piece.x_location].current_piece = piece
    
    def handle_piece_attack(self, piece: Piece):
        """
        Reacts to a piece attack event.
        """
        # Find the current position of the piece
        current_position = self.find_piece_location(piece)

        # Remove the piece from its current position
        if current_position:
            self.board[current_position[0]][current_position[1]].current_piece = Empty()
        
        # Place the piece at its new position
        self.deleted_pieces.append(self.board[piece.y_location][piece.x_location].current_piece)

        self.board[piece.y_location][piece.x_location].current_piece = piece

    def place_piece(self, piece: Piece, x: int, y: int):
        """
        Place a piece at a specific coordinate.
        :param piece: The piece to place.
        :param x: The x coordinate.
        :param y: The y coordinate.
        """
        self.board[y][x].current_piece = piece
        piece.x_location = x
        piece.y_location = y

    def get_pieces_by_color(self, color: str) -> list[Piece]:
        """
        Get all the pieces of a given color.
        """
        pieces = []
        for row in self.board:
            for square in row:
                if square.current_piece.color == color:
                    pieces.append(square.current_piece)
        return pieces
    
    def get_available_moves(self, piece: Piece) -> list[tuple[int, int]]:
        """
        Get all the available moves for a piece.
        """
        moves = []
        for i, row in enumerate(self.board):
            for j, square in enumerate(row):
                if piece.is_valid_move(j, i):
                    moves.append((j, i))
        return moves
    
    def get_available_attack_moves(self, piece: Piece) -> list[tuple[int, int]]:
        """
        Get all the available attack moves for a piece.
        """
        moves = []
        for i, row in enumerate(self.board):
            for j, square in enumerate(row):
                if piece.is_valid_attack_move(j, i):
                    moves.append((j, i))
        return moves
    
    def is_square_empty(self, x: int, y: int) -> bool:
        """
        Check if a square is empty.
        """
        piece_at_square = self.board[y][x].current_piece.__class__
        return piece_at_square == Empty
    
    def is_valid_piece(self, player_color,piece) -> bool:
        """
        Check if a piece belongs to the player.
        :param player_color: The color of the player.
        :param piece: The piece to check.
        :return: True if the piece belongs to the player, False otherwise.
        """
        if piece == Empty:
            return False
        if piece.color != player_color:
            return False
        else:
            return True
        
    def is_piece_same_color(self, piece1: Piece, piece2: Piece) -> bool:
        """
        Check if two pieces are the same color.
        """
        return piece1.color == piece2.color

    def get_piece_by_coordinates(self, x: int, y: int) -> Piece:
        """
        Get the piece at a specific coordinate.
        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: The piece at the given coordinates.
        """
        return self.board[y][x].current_piece

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        rep : str = ""
        for row in reversed(self.board):
            for column in row:
                rep+=(column.__repr__()) + " "
            rep+=('\n')
        return rep
        
    def __getitem__(self, x):
        return self.board[x]