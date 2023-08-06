# boggle_dice.py
"""
Library of classes for the magic Boggle dice and their container.
"""
from collections import Counter
import os
from random import choice, sample, seed
from re import sub


class Dice():
    """
    Represents the N sided dice.
    """

    def __init__(self, tokens=None):
        """
        Initialise the dice with tokens if they are provided.

        >>> ex = Dice()
        >>> ex.tiles is None
        True
        >>> ex.lastRoll is None
        True
        """
        self._tiles = None
        self._lastRoll = None
        if tokens is not None:
            self.makeDice(tokens)

    @property
    def tiles(self):
        """
        A tuple representing the tiles which make up the sides of the dice.

        >>> ex = Dice('ABC')
        >>> isinstance(ex.tiles, tuple)
        True
        >>> len(ex.tiles)
        3
        >>> ex.tiles
        ('A', 'B', 'C')
        """
        return self._tiles

    @property
    def lastRoll(self):
        """
        The result of the last roll of the dice.

        >>> ex = Dice('AAA')
        >>> isinstance(ex.lastRoll, str)
        True
        >>> ex.lastRoll
        'A'
        """
        return self._lastRoll

    def makeDice(self, tokens: str):
        """
        Make a dice from a tokens string and return the first roll result.

        Args:
            tokens: String of letters to appear on the dice.

        The dice is created by splitting the alphabetical elements of the
        token string into a tuple. If the token string is contiguous text
        it will be split into individual characters.

        >>> ex_1 = Dice()
        >>> ex_1.makeDice('AAA')
        'A'
        >>> ex_1.tiles
        ('A', 'A', 'A')
        >>> ex_2 = Dice()
        >>> ex_2.makeDice('B B B B B BB')
        'B'
        >>> ex_2.tiles
        ('B', 'B', 'B', 'B', 'B', 'BB')
        >>> ex_3 = Dice()
        >>> ex_3.makeDice('C, CC, C, C, C, C')
        'C'
        >>> ex_3.tiles
        ('C', 'CC', 'C', 'C', 'C', 'C')
        """
        seed()
        if tokens.isalpha():
            _tiles = tuple([t for t in tokens])
        else:
            _tiles = tuple((sub(r'\W+', ' ', tokens)).split())
        self._tiles = _tiles
        return self.roll()

    def roll(self):
        """
        Rolls the dice by randomly choosing an element and returns the result.

        >>> ex = Dice('B B B B B B')
        >>> ex.lastRoll
        'B'
        """
        if self._tiles is not None:
            self._lastRoll = choice(self._tiles)
        return self._lastRoll

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns next dice roll result.

        >>> ex = Dice('A A A A A A')
        >>> next(ex)
        'A'
        """
        if self._tiles:
            return [self.roll()].pop(0)
        raise StopIteration


class BoggleDice():
    """
    Represents the container which holds the game dice.
    """

    def __init__(self):
        """
        Initialise an empty dice container.

        >>> bd = BoggleDice()
        >>> isinstance(bd.dice, list)
        True
        >>> len(bd.dice)
        0
        >>> bd.letters
        Counter()
        >>> bd.lastRoll is None
        True
        """
        self._container = []
        self._letters = Counter()
        self._rolled = None

    def addDiceFromTokensString(self, tokens: str):
        """
        Adds a dice to the container from a string of tokens.

        Args:
            tokens: String of characters to be be converted into dice tiles.

        The string which is converted to uppercase before the dice is created.

        >>> bd = BoggleDice()
        >>> bd.addDiceFromTokensString('AAA')
        >>> len(bd.dice)
        1
        >>> isinstance(bd.dice[0], Dice)
        True
        """
        dice = Dice(tokens.upper())
        self._container.extend([dice])
        self._letters.update(set(dice.tiles))

    @property
    def dice(self):
        """
        The list of Dice objects which make up the container.
        """
        return self._container

    @property
    def letters(self):
        """
        A Counter object which is records the set of possible letters from
        each dice added to the container.

        This can be useful data for filtering a word dictionary for use
        with Boggle.
        """
        return self._letters

    @property
    def lastRoll(self):
        """
        A list containing the result of the container being shaken.
        """
        return self._rolled

    def loadFromFile(self, file_path: str):
        """
        Populates a dice container from the contents of a text file.

        Args:
            file_path: String containing the path to the text file

        Each line of the file is treated as a string of tokens for creating
        a new dice. The new dice is added to the container.
        """
        with open(file_path, 'r') as _file:
            for tokens in _file.readlines():
                self.addDiceFromTokensString(tokens.strip())

    def shake(self):
        """
        Shakes the container to randomize the dice inside.

        >>> bd = BoggleDice()
        >>> bd.addDiceFromTokensString('CCC')
        >>> bd.addDiceFromTokensString('C C C')
        >>> bd.addDiceFromTokensString('C, C, C')
        >>> bd.shake()
        ['C', 'C', 'C']
        """
        coll = self._container
        self._rolled = sample([next(d) for d in coll], len(coll))
        return self._rolled
