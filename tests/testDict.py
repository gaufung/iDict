"""
test module
"""
import unittest
import shutil
import os
from iDict import util
from iDict.word import Word
from iDict.parser import BingParser, lookup, DbParser


class TestWord(unittest.TestCase):
    def testInsertQuery(self):
        word = Word('word', '字', 'a word here', 1)
        print(word.display())
        util.insert_word(word)
        query_word = util.query_word('word')
        self.assertEqual(query_word.name, word.name)

    def tearDown(self):
        if os.path.exists(util.DEFAULT_PATH):
            shutil.rmtree(util.DEFAULT_PATH)


class TestBing(unittest.TestCase):
    def testQuery(self):
        parser = BingParser()
        word = parser.parse('fantastic')
        self.assertEqual(word.name, 'fantastic')


class TestParse(unittest.TestCase):
    def testParse(self):
        parser = lookup(DbParser(BingParser()))
        word = parser('fantastic')
        print(word.display())

    def tearDown(self):
        if os.path.exists(util.DEFAULT_PATH):
            shutil.rmtree(util.DEFAULT_PATH)

