"""
iDict is a command line tool for look up word
by local database or from bing dict
"""
import sys
import argparse
import os
import logging
from termcolor import colored
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from iDict.parser import BingParser, DbParser, ParserError
from iDict.word import Base
from iDict.config import config, DEFAULT_PATH


def display(word):
    title = colored(word.name, color='blue')
    print(title)
    print(colored('Definition: ', color='yellow'))
    for explain in word.explains:
        print(colored("*", color='red'), colored(explain.content, color='green'))
    print(colored('Sentences:', color='yellow'))
    for sentence in word.sentences:
        print(colored("*", color='red'), colored(sentence.content, color='green'))


logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="iDict")
    parser.add_argument(dest='word',
                        help='the word which you want to look up')
    args = parser.parse_args(sys.argv[1:])
    con = config['production']
    engine = create_engine(con.DATABASE_URL)
    session = sessionmaker()
    session.configure(bind=engine)
    if not os.path.exists(os.path.join(DEFAULT_PATH, con.URL)):
        Base.metadata.create_all(engine)
    if args.word:
        try:
            parser = DbParser(session())
            word = parser.parse(args.word)
            display(word)
        except ParserError:
            try:
                parser = BingParser(session())
                parser.parse(args.word)
                parser = DbParser(session())
                display(parser.parse(args.word))
            except Exception as er:
                logging.error(er)
                print(colored('Cannot search this word', color='red'))
        except Exception as err:
            logging.error(err)
            print(colored('Cannot search this word', color='red'))




