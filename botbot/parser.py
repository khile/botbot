"""Parses a single line at a time using a definition input"""
import re


class Parser(object):
    """Dynamic parser"""

    def __init__(self, bot, chan, definitions):
        """Give the class a parsing definitions"""
        self.bot = bot
        self.chan = chan
        self.definitions = definitions

    def parse(self, line):
        """Parse the line against definitions"""
        for k in self.definitions.keys():
            v = self.definitions[k]
            r = re.search(v[0], line, re.IGNORECASE)
            if r:
                v[1](r, line, self.bot, self.chan)
