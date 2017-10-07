"""
parse a word to word object
"""
import os
from bs4 import BeautifulSoup
from iDict import word


class ParserError(Exception):
    pass


class Parser(object):
    """
    The base class of Parser
    """
    def parse(self, text):
        raise NotImplementedError("Please Implement the method")


class DbParser(Parser):
    def __init__(self, engine, successor=None):
        self.successor = successor
        self.engine = engine

    def parse(self, text):
        try:
            pass
        except ParserError:
            self.successor.parse(text)
        except Exception as err:
            raise err


class BingParser(Parser):
    def __init__(self, url='http://cn.bing.com/dict/search?q={%s}', successor=None):
        self.successor = successor
        self.url = url

    def parse(self, text):
        try:
            pass
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


def _parse_bing_dict(url):
    """
    parse word from bing dict
    :param url: the get url from bing: http://cn.bing.com/dict/search?q={word}
    :return: the word's object
    """
    pass
