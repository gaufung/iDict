"""
test module
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from iDict import BingParser, DbParser, config, Word, Explain, Sentence, Base


class TestWord(unittest.TestCase):

    def setUp(self):
        con = config['testing']
        self.engine = create_engine(con.DATABASE_URL)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def testInsertQuery(self):
        word = Word(name='word')
        explain1 = Explain(content='字', word=word)
        explain2 = Explain(content='字词', word=word)
        sentence1 = Sentence(content='A word here', word=word)
        sentence2 = Sentence(content='We find a word', word=word)
        s = self.session()
        s.add(word)
        s.add(explain1)
        s.add(explain2)
        s.add(sentence1)
        s.add(sentence2)
        s.commit()
        self.assertEqual(len(s.query(Word).all()), 1)
        word = s.query(Word).filter(Word.name == 'word').one()
        self.assertEqual(word.name, 'word')
        self.assertEqual(len(word.explains), 2)
        self.assertEqual(len(word.sentences), 2)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)


class TestBingDB(unittest.TestCase):
    def setUp(self):
        con = config['testing']
        self.engine = create_engine(con.DATABASE_URL)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def testBingDB(self):
        parser = DbParser(self.session(),
                          BingParser(self.session(),
                                     DbParser(self.session(), None, 3),
                                     3),
                          3)
        word = parser.parse('fantastic')
        print(word)
        self.assertEqual(word.name, 'fantastic')
        self.assertEqual(word.priority, 3)
        self.assertGreater(len(word.explains), 1)
        self.assertGreater(len(word.sentences), 1)


