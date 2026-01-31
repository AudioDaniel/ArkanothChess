from gameboard import Gameboard
from square import Square
from pieces.piece import Piece
from pieces.pawn import Pawn
from pieces.warrior import Warrior
from turn_mgr import TurnManager
from network import NetworkManager

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

    tableroprincipal.move_piece(peonVerde, 0, 1)
    #peonRojo.move(2,3)

    print(tableroprincipal)

    tableroprincipal.attack_piece(peonVerde2, 1, 1)

    print(tableroprincipal)
    print(tableroprincipal.deleted_pieces)
    print("-----")

def test_b():
    tableroprincipal = Gameboard(8)
    tableroprincipal.load_standard_pieceset()

    print("---Arkanoth-Chess---\n")
    print(tableroprincipal)
    print("----------------\n")

def main():
    print("Welcome to Arkanoth Chess")
    print("1. Single Player (Vs Computer)")
    print("2. Host Multiplayer Game")
    print("3. Join Multiplayer Game")

    choice = input("Select mode: ").strip()

    tableroprincipal = Gameboard(8)
    tableroprincipal.load_standard_pieceset()

    turn_manager = None

    if choice == '1':
        turn_manager = TurnManager(tableroprincipal, my_color="Green", network_manager=None)
    elif choice == '2':
        net = NetworkManager()
        port_input = input("Enter port to listen on (default 5000): ").strip()
        port = int(port_input) if port_input else 5000
        net.host_game(port=port)
        # Host plays Green
        turn_manager = TurnManager(tableroprincipal, my_color="Green", network_manager=net)
    elif choice == '3':
        net = NetworkManager()
        host = input("Enter host IP (default localhost): ").strip()
        host = host if host else 'localhost'
        port_input = input("Enter port to connect to (default 5000): ").strip()
        port = int(port_input) if port_input else 5000
        net.join_game(host, port)
        # Client plays Red
        turn_manager = TurnManager(tableroprincipal, my_color="Red", network_manager=net)
    else:
        print("Invalid selection. Defaulting to Single Player.")
        turn_manager = TurnManager(tableroprincipal, my_color="Green", network_manager=None)

    try:
        turn_manager.turn_loop()
    except KeyboardInterrupt:
        print("\nGame exited.")
    finally:
        if turn_manager and turn_manager.network_manager:
            turn_manager.network_manager.close()

if __name__ == "__main__":
    main()
