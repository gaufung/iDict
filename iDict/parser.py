"""
parse a word to word object
"""
import os
from bs4 import BeautifulSoup
from iDict.word import Word, Explain, Sentence


class ParserError(Exception):
    pass


class Parser(object):
    """
    The base class of Parser
    """
    def parse(self, text):
        raise NotImplementedError("Please Implement the method")


class DbParser(Parser):
    def __init__(self, session, priority=1):
        self.session = session
        self.priority = priority

    def parse(self, text):
        word = self.session.query(Word).filter(Word.name == text).first()
        if not word:
            raise ParserError('Cannot look up from database')
        word.priority = self.priority
        self.session.commit()
        return word


class BingParser(Parser):

    url = 'http://cn.bing.com/dict/search?q={%s}'

    def __init__(self, session, priority=1):
        self.session = session
        self.priority = priority

    def _parse(self, text):
        soup = BeautifulSoup(open('search?q=%s' % text, encoding='utf-8'), 'lxml')
        definition_tags = soup.find_all(class_='def')
        word = Word(name=text, priority=self.priority)
        if not definition_tags:
            raise ValueError('Can not find this word')
        for tag in definition_tags:
            self.session.add(Explain(content=tag.string, word=word))
        sentence_tags = soup.find_all(class_='sen_en')
        for tag in sentence_tags:
            words = []
            for child in tag.children:
                words.append(child.string)
            self.session.add(Sentence(content=''.join(words), word=word))
        self.session.add(word)
        self.session.commit()

    def parse(self, text):
        try:
            query_url = self.url % text
            os.system('curl -O %s' % query_url)
            if os.path.exists('search?q=%s' % text):
                self._parse(text)
                os.remove('search?q=%s' % text)
        except ParserError:
            if self.successor is None:
                raise Exception('Having no handler')
            else:
                self.successor.parse(text)
        except ValueError as err:
            if os.path.exists('search?q=%s' % text):
                os.remove('search?q=%s' % text)
            raise err
        except Exception as err:
            raise err

