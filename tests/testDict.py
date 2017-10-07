"""
test module
"""
import unittest
import shutil
from iDict import util
from iDict.word import Word
from iDict.parser import BingParser


class TestWord(unittest.TestCase):
    def testInsertQuery(self):
        word = Word('word', '字', 'a word here', 1)
        util.insert_word(word)
        query_word = util.query_word('word')
        self.assertEqual(query_word.name, word.name)

    def tearDown(self):
        shutil.rmtree(util.DEFAULT_PATH)


class TestBing(unittest.TestCase):
    def testQuery(self):
        parser = BingParser()
        word = parser.parse('fantastic')
        self.assertEqual(word.name, 'fantastic')


