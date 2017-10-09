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
from iDict.config import config


def display(word):
    title = colored(word.name, color='blue')
    print(title)
    print(colored('Definition: ', color='yellow'))
    for explain in word.explains:
        print(colored("*", color='red'), colored(explain.content, color='green'))
    print(colored('Sentences:', color='yellow'))
    for sentence in word.sentences:
        print(colored("*", color='red'), colored(sentence.content, color='green'))


logging.basicConfig(level=logging.ERROR,
                    filename='app.log',
                    format='%(message)s')


def main():
    parser = argparse.ArgumentParser(description="iDict")
    parser.add_argument('-w', dest='word',
                        help='the word which you want to look up')
    parser.add_argument('-p', '--priority', dest='priority',
                        action='store', help='set word priority')
    args = parser.parse_args(sys.argv[1:])
    con = config['production']
    engine = create_engine(con.DATABASE_URL)
    session = sessionmaker()
    session.configure(bind=engine)
    if not os.path.exists(os.path.join(con.DEFAULT_PATH, con.URL)):
        logging.info('Create the database')
        Base.metadata.create_all(engine)
    priority = int(args.priority) if args.priority else 1
    if args.word:
        try:
            parser = DbParser(session(), priority)
            word = parser.parse(args.word)
            display(word)
        except ParserError:
            try:
                parser = BingParser(session(), priority)
                parser.parse(args.word)
                parser = DbParser(session())
                display(parser.parse(args.word))
            except Exception as er:
                logging.info(er)
                print(colored('Cannot search this word', color='red'))
        except Exception as err:
            logging.info(err)
            print(colored('Cannot search this word', color='red'))




