"""
The class of word using SQLAlchemy orm framework
"""
import os


class Word(object):
    def __init__(self, name, chinese, sentences, priority=1):
        self._name = name
        self._chinese = chinese
        self._sentences = sentences
        self._property = priority

    @property
    def name(self):
        return self._name

    @property
    def chinese(self):
        return self._chinese

    @property
    def sentences(self):
        return self._sentences

    @property
    def priority(self):
        return self._property

    def __str__(self):
        return self.name

    def display(self):
        shows = list()
        shows.append(os.linesep)
        shows.append(self.name)
        shows.append(os.linesep)
        shows.append('******Chinese definitions******')
        shows.append(os.linesep)
        shows.append(self.chinese)
        shows.append(os.linesep)
        shows.append('******Sentences********')
        shows.append(os.linesep)
        shows.append(self.sentences)
        shows.append(os.linesep)
        return ''.join(shows)




