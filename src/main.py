from gameboard import Gameboard
from square import Square
from piece import Piece
from pawn import Pawn
from warrior import Warrior

# Entry point of the program

def test():
    tableroprincipal = Gameboard(8)
    peon = Pawn('Red')
    peon2 = Pawn('Green')
    tableroprincipal.place_piece(peon,0,0)
    tableroprincipal.place_piece(peon2,2,4)
    print(tableroprincipal)

    peon.move(0,1)
    
    print(tableroprincipal)
    print("-----")

def main():
    tableroprincipal = Gameboard(8)
    tableroprincipal.load_standard_pieceset()
    print("\n\n\n\n")
    print("---Arkanoth-Chess---\n")
    print(tableroprincipal)
    print("----------------\n")

if __name__ == "__main__":
    main()