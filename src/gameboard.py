from event import subscribe
from piece import Piece
from square import Square
from empty import Empty
from pawn import Pawn
from warrior import Warrior
class Gameboard:
    def __init__(self,tamanho):
        self.board : list[list[Piece]] = self.load_board(tamanho)
        self.setup_piece_movement_handlers()
        self.deleted_pieces : list = []
        self.setup_piece_attack_handlers()

    def load_board(self,tamanho):
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
        self.place_piece(Warrior("Green"), 0, 0)
        self.place_piece(Warrior("Green"), 7, 0)
        # Black pieces
        self.place_piece(Pawn("Red"), 0, 6)
        self.place_piece(Pawn("Red"), 1, 6)
        self.place_piece(Pawn("Red"), 2, 6)
        self.place_piece(Pawn("Red"), 3, 6)
        self.place_piece(Pawn("Red"), 4, 6)
        self.place_piece(Pawn("Red"), 5, 6)
        self.place_piece(Pawn("Red"), 6, 6)
        self.place_piece(Pawn("Red"), 7, 6)
        self.place_piece(Warrior("Red"), 0, 7)
        self.place_piece(Warrior("Red"), 7, 7)

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
        subscribe("piece_movement", self.handle_piece_movement)

    def setup_piece_attack_handlers(self):
        subscribe("piece_attack", self.handle_piece_attack)
        
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
        self.board[y][x].current_piece = piece
        piece.x_location = x
        piece.y_location = y

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