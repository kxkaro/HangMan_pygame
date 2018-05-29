import unittest
from unittest.mock import patch
from cls.alphabet import *
import string
import requests


class TestAlphabet(unittest.TestCase):

    def test_alphabet_reset(self):
        alphabet = Alphabet()
        alphabet.reset()
        self.assertEqual(alphabet.available, "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ")
        self.assertEqual(alphabet.used, "")


    def test_alphabet_update(self):
        alphabet = Alphabet()
        alphabet.reset()
        alphabet.update("d")
        alphabet.update("F")
        self.assertEqual(alphabet.available, "A B C E G H I J K L M N O P Q R S T U V W X Y Z ")
        self.assertEqual(alphabet.used, "dF")


if __name__ == '__main__':
    unittest.main()