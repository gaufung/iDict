"""
parse a word to word object
"""
import logging
from bs4 import BeautifulSoup
import requests
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
    def __init__(self, session, **options):
        self.session = session
        self.priority = options.get('priority', 1)
        self.successor = options.get('successor', None) 

    def parse(self, text):
        word = self.session.query(Word).filter(Word.name == text).first()
        try:
            if not word:
                raise ParserError('Cannot look up from database')
            word.priority = self.priority
            self.session.commit()
            return word
        except ParserError as err:
            logging.info(err)
            if self.successor:
                return self.successor.parse(text)
            else:
                raise ParserError('No successor')


class BingParser(Parser):

    url = 'http://cn.bing.com/dict/search?q={}'

    my_headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN, zh;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'cn.bing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/48.0.2564.116 Safari/537.36'
    }

    def __init__(self, session, successor, priority=1):
        self.session = session
        self.priority = priority
        self.successor = successor

    def _parse(self, body, text):
        soup = BeautifulSoup(body, 'lxml')
        definition_tags = soup.find_all(class_='def')
        word = Word(name=text, priority=self.priority)
        try:
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
        except Exception as err:
            logging.error(err)
            self.session.rollback()
        finally:
            self.session.close()

    def parse(self, text):
        query_url = self.url.format(text)
        response = requests.get(query_url, headers=self.my_headers)
        if response.status_code == 200:
            body = response.text
            self._parse(body, text)
            return self.successor.parse(text)
        else:
            raise ParserError('Can not query word from Internet')

