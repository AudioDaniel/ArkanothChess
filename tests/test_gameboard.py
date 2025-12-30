import unittest
import sys
import os

# Ensure src is in path so we can import modules as if we were inside src
sys.path.append(os.path.join(os.getcwd(), 'src'))

from gameboard import Gameboard
from pieces.pawn import Pawn
from pieces.empty import Empty
from exceptions.invalid_move import InvalidMoveException

class TestGameboard(unittest.TestCase):
    def setUp(self):
        self.gameboard = Gameboard(8)

    def test_initialization(self):
        self.assertEqual(len(self.gameboard.board), 8)
        self.assertEqual(len(self.gameboard.board[0]), 8)
        # Verify it returns an instance of Empty.
        # Note: Since we fixed imports, isinstance should work if classes match.
        self.assertIsInstance(self.gameboard.get_piece_by_coordinates(0, 0), Empty)

    def test_place_piece(self):
        pawn = Pawn("Green")
        self.gameboard.place_piece(pawn, 0, 0)
        self.assertEqual(self.gameboard.get_piece_by_coordinates(0, 0), pawn)
        self.assertEqual(pawn.x_location, 0)
        self.assertEqual(pawn.y_location, 0)

    def test_move_piece_valid(self):
        pawn = Pawn("Green")
        self.gameboard.place_piece(pawn, 0, 1)
        # Green moves up (y + 1)
        self.gameboard.move_piece(pawn, 0, 2)

        self.assertIsInstance(self.gameboard.get_piece_by_coordinates(0, 1), Empty)
        self.assertEqual(self.gameboard.get_piece_by_coordinates(0, 2), pawn)
        self.assertEqual(pawn.y_location, 2)

    def test_move_piece_invalid_geometry(self):
        pawn = Pawn("Green")
        self.gameboard.place_piece(pawn, 0, 1)

        # Invalid move for Pawn (sideways)
        with self.assertRaises(InvalidMoveException):
            self.gameboard.move_piece(pawn, 1, 1)

    def test_move_piece_blocked(self):
        pawn1 = Pawn("Green")
        pawn2 = Pawn("Red")
        self.gameboard.place_piece(pawn1, 0, 1)
        self.gameboard.place_piece(pawn2, 0, 2)

        # Blocked by another piece
        with self.assertRaises(InvalidMoveException):
            self.gameboard.move_piece(pawn1, 0, 2)

    def test_attack_piece_valid(self):
        pawn = Pawn("Green")
        target = Pawn("Red")
        self.gameboard.place_piece(pawn, 0, 1)
        self.gameboard.place_piece(target, 1, 2)

        self.gameboard.attack_piece(pawn, 1, 2)

        self.assertIsInstance(self.gameboard.get_piece_by_coordinates(0, 1), Empty)
        self.assertEqual(self.gameboard.get_piece_by_coordinates(1, 2), pawn)
        self.assertIn(target, self.gameboard.deleted_pieces)

    def test_attack_empty_square(self):
        pawn = Pawn("Green")
        self.gameboard.place_piece(pawn, 0, 1)

        # Valid attack geometry but empty square
        with self.assertRaises(InvalidMoveException):
            self.gameboard.attack_piece(pawn, 1, 2)

    def test_attack_own_piece(self):
        pawn1 = Pawn("Green")
        pawn2 = Pawn("Green")
        self.gameboard.place_piece(pawn1, 0, 1)
        self.gameboard.place_piece(pawn2, 1, 2)

        with self.assertRaises(InvalidMoveException):
            self.gameboard.attack_piece(pawn1, 1, 2)

if __name__ == '__main__':
    unittest.main()
