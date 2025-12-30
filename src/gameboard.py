from pieces.piece import Piece
from square import Square
from pieces.empty import Empty
from pieces.pawn import Pawn
from exceptions.invalid_move import InvalidMoveException

class Gameboard:
    def __init__(self,tamanho):
        """
        Initialize the gameboard.
        :param tamanho: Size of the board (tamanho x tamanho).
        """
        self.board : list[list[Piece]] = self.load_board(tamanho)
        self.deleted_pieces : list = []

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
        # Black pieces
        self.place_piece(Pawn("Red"), 0, 6)
        self.place_piece(Pawn("Red"), 1, 6)
        self.place_piece(Pawn("Red"), 2, 6)
        self.place_piece(Pawn("Red"), 3, 6)
        self.place_piece(Pawn("Red"), 4, 6)
        self.place_piece(Pawn("Red"), 5, 6)
        self.place_piece(Pawn("Red"), 6, 6)
        self.place_piece(Pawn("Red"), 7, 6)

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

    def move_piece(self, piece: Piece, x: int, y: int):
        """
        Move a piece to a new location if valid.
        """
        if not piece.is_valid_move(x, y):
            raise InvalidMoveException("Invalid move geometry.")

        # Check if destination is empty (basic check, could be more complex)
        if not self.is_square_empty(x, y):
             raise InvalidMoveException("Destination is not empty.")

        current_x, current_y = piece.x_location, piece.y_location

        # Update board
        self.board[current_y][current_x].current_piece = Empty()
        self.board[y][x].current_piece = piece

        # Update piece
        piece.x_location = x
        piece.y_location = y

    def attack_piece(self, piece: Piece, x: int, y: int):
        """
        Attack a location with a piece.
        """
        if not piece.is_valid_attack_move(x, y):
             raise InvalidMoveException("Invalid attack geometry.")

        # Check if there is a piece to attack
        if self.is_square_empty(x, y):
            raise InvalidMoveException("No piece to attack.")

        target_piece = self.get_piece_by_coordinates(x, y)
        if self.is_piece_same_color(piece, target_piece):
            raise InvalidMoveException("Cannot attack own piece.")

        current_x, current_y = piece.x_location, piece.y_location
        
        # Remove victim
        self.deleted_pieces.append(target_piece)

        # Move attacker
        self.board[current_y][current_x].current_piece = Empty()
        self.board[y][x].current_piece = piece

        # Update piece
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
                    # Check if destination is empty
                    if self.is_square_empty(j, i):
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
                    # Check if there is an enemy piece
                    if not self.is_square_empty(j, i):
                         target = self.get_piece_by_coordinates(j, i)
                         if not self.is_piece_same_color(piece, target):
                            moves.append((j, i))
        return moves
    
    def is_square_empty(self, x: int, y: int) -> bool:
        """
        Check if a square is empty.
        """
        if x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board):
            return False
        piece_at_square = self.board[y][x].current_piece.__class__
        return piece_at_square == Empty
    
    def is_valid_piece(self, player_color, piece) -> bool:
        """
        Check if a piece belongs to the player.
        """
        if isinstance(piece, Empty):
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
