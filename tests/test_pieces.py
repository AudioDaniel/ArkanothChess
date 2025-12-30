import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))

from pieces.pawn import Pawn
from pieces.warrior import Warrior

class TestPieces(unittest.TestCase):
    def test_pawn_green_movement(self):
        pawn = Pawn("Green")
        pawn.x_location = 1
        pawn.y_location = 1

        # Valid move: up 1
        self.assertTrue(pawn.is_valid_move(1, 2))

        # Invalid moves
        self.assertFalse(pawn.is_valid_move(1, 3)) # Move 2 spaces
        self.assertFalse(pawn.is_valid_move(2, 2)) # Diagonal
        self.assertFalse(pawn.is_valid_move(1, 0)) # Backward

    def test_pawn_red_movement(self):
        pawn = Pawn("Red")
        pawn.x_location = 1
        pawn.y_location = 6

        # Valid move: down 1
        self.assertTrue(pawn.is_valid_move(1, 5))

        # Invalid moves
        self.assertFalse(pawn.is_valid_move(1, 4)) # Move 2 spaces
        self.assertFalse(pawn.is_valid_move(1, 7)) # Backward

    def test_pawn_attack(self):
        pawn = Pawn("Green")
        pawn.x_location = 1
        pawn.y_location = 1

        # Valid attacks: diagonals forward
        self.assertTrue(pawn.is_valid_attack_move(0, 2))
        self.assertTrue(pawn.is_valid_attack_move(2, 2))

        # Invalid attacks
        self.assertFalse(pawn.is_valid_attack_move(1, 2)) # Forward straight
        self.assertFalse(pawn.is_valid_attack_move(1, 0)) # Backward

    def test_warrior_not_implemented(self):
        warrior = Warrior("Green")
        with self.assertRaises(NotImplementedError):
            warrior.is_valid_move(0, 0)

if __name__ == '__main__':
    unittest.main()
