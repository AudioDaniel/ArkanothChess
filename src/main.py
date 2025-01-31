from gameboard import Gameboard
from square import Square
from pieces.piece import Piece
from pieces.pawn import Pawn
from pieces.warrior import Warrior

# Entry point of the program

def test():
    tableroprincipal = Gameboard(6)
    peonVerde = Pawn('Green')
    peonVerde2 = Pawn('Green')
    peonRojo = Pawn('Red')

    tableroprincipal.place_piece(peonVerde,0,0)
    tableroprincipal.place_piece(peonRojo,1,1)
    tableroprincipal.place_piece(peonVerde2,2,0)
    print(tableroprincipal)

    peonVerde.move(0,1)
    #peonRojo.move(2,3)

    print(tableroprincipal)

    peonVerde2.attack(1,1)

    print(tableroprincipal)
    print(tableroprincipal.deleted_pieces)
    print("-----")

def main():
    tableroprincipal = Gameboard(8)
    tableroprincipal.load_standard_pieceset()

    print("---Arkanoth-Chess---\n")
    print(tableroprincipal)
    print("----------------\n")

if __name__ == "__main__":
    test()