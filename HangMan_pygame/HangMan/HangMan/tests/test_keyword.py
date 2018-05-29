import unittest
from unittest.mock import patch
from cls.keyword import *
import string
import requests


class TestKeyword(unittest.TestCase):

    def test_keyword_initialize_list_none(self):
        keyword = Keyword()
        keyword.initialize_list()
        self.assertTrue(len(keyword.keywords_list) > 1 )


    def test_keyword_initialize_list_custom(self):
        keyword = Keyword()
        keyword.initialize_list(['test kEYWord'])
        self.assertEqual(keyword.keywords_list, ['test kEYWord'])


    def test_keyword_assign_update(self):
        keyword = Keyword()
        keyword.assign_new(['test kEYWord'])
        self.assertEqual(keyword.keyword, "TEST KEYWORD")
        self.assertEqual(keyword.hidden, ".... .......")


    def test_keyword_update(self):
        keyword = Keyword()
        keyword.assign_new(['test kEYWord'])
        keyword.update('e')
        keyword.update('D')
        self.assertEqual(keyword.keyword, "TEST KEYWORD")
        self.assertEqual(keyword.hidden, ".E.. .E....D")
    

if __name__ == '__main__':
    unittest.main()