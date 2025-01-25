from gameboard import Gameboard
from square import Square
from piece import Piece
from pawn import Pawn
from warrior import Warrior

# Entry point of the program

def main():
    tableroprincipal = Gameboard(8)
    peon = Pawn('Red')
    peon2 = Pawn('Green')
    tableroprincipal.place_piece(peon,0,0)
    tableroprincipal.place_piece(peon2,2,4)
    print(tableroprincipal)

    peon.move(0,1)
    
    print(tableroprincipal)
    print("-----")

if __name__ == "__main__":
    main()