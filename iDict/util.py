"""
util tools for word
"""
import os
import sys
import sqlite3
from iDict.word import  Word
CREATE_TABLE_WORD = '''
CREATE TABLE IF NOT EXIST Word
(
name        TEXT PRIMARY KEY,
chinese     TEXT,
sentences   TEXT,
priority    INT DEFAULT 1
)
'''

DEFAULT_PATH = os.path.join(os.path.expanduser('~'), '.iDict')


def _database_exist():
    return not os.path.exists(os.path.join(DEFAULT_PATH, 'word.db'))


def _create_database():
    if _database_exist():
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
    curs.execute('SELECT * From Word where name = "%s"' % word.name)
    res = curs.fetchall()
    if res:
        print(word, 'has existed')
        sys.exit()
    try:
        curs.execute('INSERT INTO Word(name, chinese, sentences, priority) values ("%s", "%s", "%s", "%s")'
                     % word.name, word.chinese, word.sentences, word.priority)
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
            print('word does not exist')
    else:
        print('database does not exist')
