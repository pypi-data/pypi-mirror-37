import unittest
from model import *
from itertools import repeat


class TestAI(unittest.TestCase):
    def test_block(self):
        b = Board.from_moves(exec_road("a", 4, False)[:-1], 4)
        ai = MinimaxAI(b, Colors.BLACK)
        self.assertEqual(str(ai.pick_move(4)), "a4", "Error: AI did not block road threat A")

    def test_take(self):
        b = Board.from_moves(exec_road("a", 4, False)[:-1], 4)
        ai = MinimaxAI(b, Colors.WHITE)
        self.assertEqual(str(ai.pick_move(4)), "a4", "Error: AI did not take road threat A")



if __name__ == '__main__':
    unittest.main()
