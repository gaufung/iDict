"""
util tools for word
"""
import os
import sqlite3
import logging
from iDict.word import Word
CREATE_TABLE_WORD = '''
CREATE TABLE IF NOT EXISTS Word
(
name        TEXT PRIMARY KEY,
chinese     TEXT,
sentences   TEXT,
priority    INT DEFAULT 1
)
'''

DEFAULT_PATH = os.path.join(os.path.expanduser('~'), '.iDict')


def _database_exist():
    return os.path.exists(os.path.join(DEFAULT_PATH, 'word.db'))


def _create_database():
    if not _database_exist():
        logging.info('create database')
        os.mkdir(DEFAULT_PATH)
        conn = sqlite3.connect(os.path.join(DEFAULT_PATH, 'word.db'))
        curs = conn.cursor()
        curs.execute(CREATE_TABLE_WORD)
        conn.commit()
        curs.close()
        conn.close()


def insert_word(word):
    _create_database()
    conn = sqlite3.connect(os.path.join(DEFAULT_PATH, 'word.db'))
    curs = conn.cursor()
    curs.execute('Select * From Word where name = "%s"' % word.name)
    res = curs.fetchall()
    if res:
        print(word, 'has existed')
        return
    try:
        # curs.execute('Insert Into Word(name, chinese, sentences, priority) values ("%s", "%s", "%s", %d )'
        #              % (word.name, word.chinese, word.sentences, word.priority))
        curs.execute('Insert Into Word(name, chinese, sentences, priority) values ({0}, {1}, {2}, {3})'
                     .format(word.name, word.chinese, word.sentences, word.priority))
    except Exception as err:
        print('Cannot insert %s' % word.name)
        raise err
    else:
        conn.commit()
    finally:
        curs.close()
        conn.close()


def query_word(name):
    if _database_exist():
        conn = sqlite3.connect(os.path.join(DEFAULT_PATH, 'word.db'))
        curs = conn.cursor()
        curs.execute("Select * From Word where name = '%s' " % name)
        res = curs.fetchone()
        if res:
            return Word(res[0], res[1], res[2], res[3])
        else:
            print('Word does not exist')
    else:
        print('Database does not exist')
