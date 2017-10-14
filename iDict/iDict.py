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
from iDict.parser import BingParser, DbParser
from iDict.word import Base, Word
from iDict.config import config


def _display_word(word):
    title = colored(word.name, color='blue')
    print(title)
    print(colored('Definition: ', color='yellow'))
    for explain in word.explains:
        print(colored("*", color='red'), colored(explain.content, color='green'))
    print(colored('Sentences:', color='yellow'))
    for sentence in word.sentences:
        print(colored("*", color='red'), colored(sentence.content, color='green'))


def display_words(words):
    for idx, word in enumerate(words):
        if word.priority >= 3:
            word_display = colored(word.name, color='blue')
        elif 1 < word.priority < 3:
            word_display = colored(word.name, color='green')
        else:
            word_display = colored(word.name, color='yellow')
        print(colored(str(idx+1), color='red'), word_display)


logging.basicConfig(level=logging.DEBUG,
                    filename='dict.log',
                    format='%(message)s')


def main():
    parser = argparse.ArgumentParser(description="iDict")
    parser.add_argument('-w', dest='word',
                        help='the word which you want to look up')
    parser.add_argument('-p', '--priority', dest='priority',
                        action='store', help='set word priority')
    parser.add_argument('-s', action='store_true', default=False,
                        help='show words by priority')
    parser.add_argument('--delete', action='store', dest='delete_word')
    args = parser.parse_args(sys.argv[1:])
    con = config['production']
    engine = create_engine(con.DATABASE_URL)
    session = sessionmaker()
    session.configure(bind=engine)
    session = session()
    if not os.path.exists(os.path.join(con.DEFAULT_PATH, con.URL)):
        logging.info('Create the database')
        Base.metadata.create_all(engine)
    priority = int(args.priority) if args.priority else 1
    if args.word:
        try:
            parser = DbParser(session, successor=BingParser(session,
                                                            DbParser(session, priority=priority), priority),
                              priority=priority)
            word = parser.parse(args.word)
            _display_word(word)
        except Exception as err:
            logging.error(err)
            print(colored('Cannot search this word', color='red'))
    elif args.s:
            display_words(session.query(Word).order_by(Word.priority.desc()))
    elif args.delete_word:
        word = session.query(Word).filter(Word.name == args.delete_word).first()
        if word:
            try:
                session.delete(word)
                session.commit()
                print(colored('!', color="yellow"), colored('Word: %s has been deleted' % word.name, color='blue'))
            except Exception as err:
                print(colored('Delete fail', color='yellow'))
                logging.error(err)
                session.rollback()
            finally:
                session.close()
        else:
            print(colored('No such word in database', color='yellow'))
    else:
        pass

