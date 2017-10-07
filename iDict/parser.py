"""
parse a word to word object
"""
import os
from bs4 import BeautifulSoup
from iDict.word import Word


class ParserError(Exception):
    pass


class Parser(object):
    """
    The base class of Parser
    """
    def parse(self, text):
        raise NotImplementedError("Please Implement the method")


class DbParser(Parser):
    def __init__(self, successor=None):
        self.successor = successor

    def parse(self, text):
        try:
            pass
        except ParserError:
            self.successor.parse(text)
        except Exception as err:
            raise err


class BingParser(Parser):

    url = 'http://cn.bing.com/dict/search?q={%s}'

    def __init__(self, successor=None):
        self.successor = successor

    def _parse(self, text):
        soup = BeautifulSoup(open('search?q=%s' % text, encoding='utf-8'), 'lxml')
        definition_tags = soup.find_all(class_='def')
        chinese = []
        for tag in definition_tags:
            chinese.append(tag.string)
        sentence_tags = soup.find_all(class_='sen_en')
        sentences = []
        for tag in sentence_tags:
            words = []
            for child in tag.children:
                words.append(child.string)
            sentences.append(''.join(words))
        return Word(text, ''.join(chinese), ''.join(sentences))

    def parse(self, text):
        try:
            query_url = self.url % text
            os.system('curl -O %s' % query_url)
            word = self._parse(text)
            os.remove('search?q=%s' % text)
            return word
        except ParserError:
            if self.successor is None:
                raise Exception('Having no handler')
            else:
                self.successor.parse(text)
        except Exception as err:
            raise err



def lookup(handler):
    def _parse(text):
        return handler.parse(text)
    return _parse

