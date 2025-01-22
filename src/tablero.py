from event import subscribe
from pieza import Pieza
from square import Square
from empty import Empty
class Tablero:
    def __init__(self,tamanho):
        self.board : list[list[Pieza]] = self.load_board(tamanho)
        self.setup_piece_movement_handlers()
        
    def load_board(self,tamanho):
        board = []
        for x in range(tamanho):
            row = []
            for y in range(tamanho):
                row.append(Square(Empty()))
            board.append(row)
        return board
    
    def setup_piece_movement_handlers(self):
        subscribe("piece_movement", self.handle_piece_movement)
        
    def handle_piece_movement(self, piece: Pieza):
        # Find the current position of the piece
        current_position = None
        for i, row in enumerate(self.board):
            for j, square in enumerate(row):
                if square.current_piece == piece:
                    current_position = (i, j)
                    break
            if current_position:
                break
    
        # Remove the piece from its current position
        if current_position:
            self.board[current_position[0]][current_position[1]].current_piece = Empty()

        # Place the piece at its new position
        self.board[piece.x_location][piece.y_location].current_piece = piece

    def place_piece(self, piece: Pieza, x: int, y: int):
        self.board[x][y].current_piece = piece
        piece.x_location = x
        piece.y_location = y

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        rep : str = ""
        x = 0
        y = 0 
        for row in self.board:
            for column in row:
                rep+=(column.current_piece.ascii_symbol) + " "
            rep+=('\n')
            y+=1
            x+=1
        return rep
        
    def __getitem__(self, x):
        return self.board[x]