import unittest
import threading
import time
import sys
import os
from unittest.mock import MagicMock, patch

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from network import NetworkManager
from turn_mgr import TurnManager
from gameboard import Gameboard

class TestNetworkIntegration(unittest.TestCase):
    def setUp(self):
        self.port = 5005
        self.host_net = NetworkManager()
        self.client_net = NetworkManager()
        self.host_board = Gameboard(8)
        self.client_board = Gameboard(8)
        self.host_board.load_standard_pieceset()
        self.client_board.load_standard_pieceset()

    def tearDown(self):
        self.host_net.close()
        self.client_net.close()

    def test_move_exchange(self):
        # 1. Setup connection
        server_ready = threading.Event()

        def start_server():
            self.host_net.host_game(port=self.port)
            server_ready.set()

        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        # Give server a moment to bind
        time.sleep(0.5)

        self.client_net.join_game('localhost', self.port)
        server_ready.wait()
        server_thread.join()

        # 2. Setup TurnManagers
        host_tm = TurnManager(self.host_board, my_color="Green", network_manager=self.host_net)
        client_tm = TurnManager(self.client_board, my_color="Red", network_manager=self.client_net)

        # 3. Simulate Host Turn (Green)
        # Host moves Pawn at (0,1) to (0,2)
        # We mock UserInteraction for the host

        with patch('user_interaction.UserInteraction.select_square') as mock_input:
            # Host inputs: Select piece at (0,1), Move to (0,2)
            # The logic calls select_square twice per turn (piece, dest)
            mock_input.side_effect = [(0, 1), (0, 2)]

            # Run Host Logic
            # Green Turn on Host (Local)
            host_tm.local_turn_logic("Green")

            # Check Host Board
            p = self.host_board.get_piece_by_coordinates(0, 2)
            self.assertEqual(p.color, "Green")

            # Client Logic: Receive Move
            # Green Turn on Client (Network)
            client_tm.network_turn_logic("Green")

            # Check Client Board
            p_client = self.client_board.get_piece_by_coordinates(0, 2)
            self.assertEqual(p_client.color, "Green")

        # 4. Simulate Client Turn (Red)
        # Client moves Pawn at (0,6) to (0,5)

        with patch('user_interaction.UserInteraction.select_square') as mock_input:
            mock_input.side_effect = [(0, 6), (0, 5)]

            # Run Client Logic
            # Red Turn on Client (Local)
            client_tm.local_turn_logic("Red")

            # Check Client Board
            p_client = self.client_board.get_piece_by_coordinates(0, 5)
            self.assertEqual(p_client.color, "Red")

            # Host Logic: Receive Move
            # Red Turn on Host (Network)
            host_tm.network_turn_logic("Red")

            # Check Host Board
            p_host = self.host_board.get_piece_by_coordinates(0, 5)
            self.assertEqual(p_host.color, "Red")

if __name__ == '__main__':
    unittest.main()
