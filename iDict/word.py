"""
The class of word using SQLAlchemy orm framework
"""


class Word(object):
    def __init__(self, name, chinese, sentences, priority=0):
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


