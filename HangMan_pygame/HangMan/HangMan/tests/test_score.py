import unittest
from cls.score import *
import string
import requests


class TestScore(unittest.TestCase):

    def test_score_decrease_current(self):
        score = Score(5)
        score.decrease_current()
        self.assertEqual(score.current_score, 4)


    def test_score_decrease_update(self):
        score = Score(5)
        score.decrease_current(2)
        score.update()
        self.assertEqual(score.current_score, 5)
        self.assertEqual(score.total_score, 3)
    

if __name__ == '__main__':
    unittest.main()