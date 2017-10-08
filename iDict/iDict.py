"""
iDict is a command line tool for look up word
by local database or from bing dict
"""
import sys
import argparse
from iDict.parser import lookup, BingParser, DbParser
from iDict.util import insert_word


def main():
    parser = argparse.ArgumentParser(description="iDict")
    parser.add_argument(dest='word',
                        help='the word which you want to look up')
    parser.add_argument('-a', '--add', dest='add',
                        action='store', default=False,
                        help='add word to database')

    args = parser.parse_args(sys.argv[1:])
    looker = lookup(DbParser(BingParser()))
    if args.word and args.add:
        word = looker(args.word)
        print(word.display())
        insert_word(word)
    elif args.word:
        word = looker(args.word)
        print(word.display())
    else:
        print('Please input word to be searched')
