# boggle_words.py
"""
Library for building a word dictionary including prefixes for Boggle.
"""
from collections import UserDict
from re import sub


class NoneFieldDict(UserDict):
    """
    This dict subclass returns a None type instead of raising a KeyError.
    """

    def __missing__(self, key):
        "Returns the null object None."
        return None


class TrieNode:
    """
    Represents a Trie data structure used to build an efficient word search.

    The children container is implemented using the `NoneFieldDict`. It's use
    of the __missing__ method reduces the memory footprint of the Trie.

    Public attributes:
    - parent   : TrieNode - Link to parent node in the Trie.
    - children : NoneFieldDict of TrieNode - The key is the next letter.
    - isWord   : Boolean - Indicates this node is the last letter in a word.
    """

    def __init__(self, parent, value):
        """
        Initialise the TrieNode and link it with the parent node.
        """
        self._parent = parent
        self._children = NoneFieldDict()
        self._isWord = False
        if parent is not None:
            parent._children[value[0]] = self

    @property
    def parent(self):
        """
        Parent node in the Trie.
        TrieNode / None
        """
        return self._parent

    @property
    def children(self):
        """
        Children of the node.
        NoneFieldDict: key: character string, value: TrieNode
        """
        return self._children

    @property
    def isWord(self):
        """
        Indicates whether or not this node is the last letter in a word.
        """
        return self._isWord


class Trie:
    """
    Represents the root node of the Trie structure.

    Public attributes:
    root : TrieNode - The root element of the Trie.
    """

    def __init__(self):
        """
        Initialise the Trie with an empty node.
        """
        self._root = TrieNode(None, '')

    @property
    def root(self):
        """
        The root element of the Trie.
        """
        return self._root

    def node(self, prefix, start=None):
        """
        Returns the node which corresponds to the final character of the
        prefix.

        Returns None if the prefix is not present in the Trie.
        """
        node = start if start else self._root
        for ch in prefix:
            if node.children[ch] is not None:
                node = node.children[ch]
            else:
                node = None
                break
        return node


class BoggleWords():
    """
    Represents the words used in the game dictionary.

    Public attributes:
    minLength : int - The prefix string length.
    prefixes : dict - key: prefix string, value: TrieNode.
    words: Trie - The dictionary data structure.
    wordsRoot: TrieNode - The root node of the dictionary.
    """

    def __init__(self, minLength=3):
        """
        Initialise with a minimum word length of 3 if not specified.
        """
        self._minLength = minLength
        self._prefixes = dict()
        self._words = Trie()

    @property
    def minLength(self):
        """
        Word prefix length and minimum length word for the game.
        """
        return self._minLength

    @property
    def prefixes(self):
        """
        dict for dictionary word prefixes - key: prefix string, value: TrieNode.
        """
        return self._prefixes

    @property
    def words(self):
        """
        The dictionary Trie.
        """
        return self._words

    @property
    def wordsRoot(self):
        """
        TrieNode at the root of the dictionary.
        """
        return self._words.root

    def _cleanWord(self, word):
        """
        Returns word in uppercase with all non-alphabethic characters removed.

        Args:
            word: String of the word being added to the Trie.

        Returns:
            Uppercase string or False
        """
        cleaned = sub(r'[\W]', '', word)
        is_valid = cleaned.isalpha() and (len(cleaned) >= self.minLength)
        return cleaned.upper() if is_valid else False

    def _getWordStartNode(self, word):
        """
        Returns the node where the word insertion should begin.

        Looks ahead to see if word prefix is already present, this will allow
        the initial levels of the Trie to be skipped if the prefix is there.

        Args:
            word: String of the word being added to the Trie.

        Returns:
            tuple(start_node, word, prefix)
            start_node: TrieNode where to begin process.
            word: String to be added.
            prefix: String prefix if it's a new prefix, otherwise None.
        """
        prefix = word[:self._minLength]
        if (prefix not in self._prefixes):
            start_node = self.wordsRoot
        else:
            start_node = self.prefixes[prefix]
            prefix = None
            word = word[self._minLength:]
        return (start_node, word, prefix)

    def iteratorPopulateTrie(self, word_iter):
        """
        Populates the Trie structure from an iterator of words.
        """
        for word in word_iter:
            cleaned_word = self._cleanWord(word)
            if isinstance(cleaned_word, str):
                node, word_part, prefix = self._getWordStartNode(cleaned_word)
                for index, letter in enumerate(word_part, 1):
                    next_node = node.children[letter]
                    if next_node is None:
                        next_node = TrieNode(node, letter)
                    node = next_node
                    if prefix is not None and index == len(prefix):
                        self.prefixes[prefix] = node
                node._isWord = True

    def loadFromFile(self, file_path):
        """
        Reads the list of words from a file and passes the list to the
        iteratorPopulateTrie() method.

        Args:
            file_path: Path to the text file.
        """
        with open(file_path, 'r') as words_file:
            self.iteratorPopulateTrie(words_file.readlines())
