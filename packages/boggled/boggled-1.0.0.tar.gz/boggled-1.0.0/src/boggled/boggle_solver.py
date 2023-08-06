# boggle_solver.py
"""
Library for solving a provided Boggle puzzle using a word dictionary.
"""
from boggled.boggle_board import BoggleBoard
from boggled.boggle_dice import BoggleDice
from boggled.boggle_words import BoggleWords, TrieNode


class BoggleSolver():
    """
    Represents the all singing and dancing Boggle puzzle solver.
    """

    def __init__(self, board, dictionary):
        """
        Initialise the solver with the provided board and dictionary.
        """
        self._board = board
        self._dictionary = dictionary.words
        self._minWordLength = dictionary.minLength
        self._prefixes = dictionary.prefixes
        self._found = dict()

    @property
    def board(self):
        """
        The board created from the provided letters.
        """
        return self._board

    @property
    def boardNeighbors(self):
        """
        Retrieve the neighbors grid from the BoggleBoard instance.
        """
        return self._board.neighbors

    @property
    def boardRangeLimit(self):
        """
        The upper range limit of the BoggleBoard instance.
        """
        return self._board.rangeLimit

    @property
    def boardTiles(self):
        """
        The letter tiles on the board.
        """
        return self._board.tiles

    @property
    def dictionary(self):
        """
        The Trie data structure used to find words on the board.
        """
        return self._dictionary

    @property
    def minWordLength(self):
        """
        The minimum length word to find when solving the board.
        """
        return self._minWordLength

    @property
    def prefixes(self):
        """
        The word prefixes found in the dictionary.
        """
        return self._prefixes

    @property
    def found(self):
        """
        A dict of tuples containing each word found as the key and a list of
        paths on the board where the word was found. There may be duplicate
        paths in the list as there can be mor than one way to make up the same
        word.

        For example in the following board fragment, the word 'BOOK' is found
        by following two different paths, 2->1->5->6 and 2->5->1->6.

        +---+---+---+---+
        |1  |2  |3  |4  |
        | O | B | Z | Q |
        +---+---+---+---+
        |5  |6  |7  |8  |
        | O | K | N | H |
        +---+---+---+---+

        In this case the list will contain two path tuples for the same word:

        {'BOOK': [(2, 1, 5, 6), (2, 5, 1, 6)]

        Each tuple in the list will always be unique.
        """
        return self._found

    @property
    def foundWords(self):
        """
        A sorted list of the words found on the board.
        """
        return sorted([word for word in self._found.keys()])

    def _addFoundWord(self, details: tuple):
        """
        Adds the details of the word found to the collection.

        Args:
            details: Tuple - the word and the path followed to create it.
        """
        word, path = details
        if self._found.get(word, None) is None:
            self._found[word] = [path]
        else:
            self._found[word].extend([path])

    def _getNode(self, prefix: str, start=None):
        """
        A helper method to retrieve the node from the dictionary's trie
        structure which corresponds to the prefix string value.
        """
        return self._dictionary.node(prefix, start)

    def _hasValidPrefix(self, prefix: str, path: list):
        """
        Indicates if the prefix string and the path used to construct it are
        valid.

        Args:
            prefix: String to match in the Trie structure.
            path: List of positions used to compose the string.

        Returns:
            Boolean indicating if the prefix meets the requirements.

        A prefix is valid if it contains the minimum word length number of
        letters and can be found in the prefixes dictionary.
        """
        return (len(path) <= self.minWordLength
                and prefix in self.prefixes)

    def _findPrefixPaths(self, prefix: str, path: list):
        """
        Yields each prefix found in the path as a tuple with three elements.

        Args:
            prefix: String to match in the Trie structure.
            path: List of neighbors used to compose the string.

        Returns:
            tuple(prefix, path, node)
            prefix: String containing the prefix.
            path: List of neighbors used to compose the string.
            node: TrieNode that corresponds to the last letter in the string.
        """
        minLength = self.minWordLength
        next_neighbors = self._findNeighborsToVisit(path)
        tiles = self.boardTiles
        if self._hasValidPrefix(prefix, path):
            yield (prefix, path, self.prefixes[prefix[:minLength]])
        for neighbor in next_neighbors:
            if len(path) < minLength:
                next_prefix = ''.join([prefix, tiles[neighbor]])
                next_path = path + [neighbor]
                for result in self._findPrefixPaths(next_prefix, next_path):
                    yield result

    def _findNeighborsToVisit(self, path):
        """
        Returns the list of neighbors not present in the path.

        Args:
            path: List of positions already visited.

        Returns:
            List of neighbor positions not visited.
        """
        position_neighbors = self.boardNeighbors[path[-1]]
        return [position for position in position_neighbors if position not in path]

    def _findWords(self, prefix: str, path: list, node: TrieNode=None):
        """
        A recursive method which finds all words in the dictionary beginning
        with the prefix string and extending from the path on the board.

        Args:
            prefix: String to match in the Trie structure.
            path: List of neighbors used to compose the string.
            node: TrieNode that corresponds to the last letter in the string.

        Algorithm:
        If the prefix string corresponds with a word in the dictionary:
            Add the tuple (prefix, path) to the list for words already found.
        For each neighboring position not yet visited:
            Make a new prefix by appending the position's value to the prefix.
            Make a new path by appending the position to the path.
            Call the method with the updated prefix and path values.
        """
        if node is None:
            node = self._getNode(prefix)
        if node is not None:
            if node.isWord:
                self._addFoundWord((prefix, tuple(path)))
            next_neighbors = self._findNeighborsToVisit(path)
            tiles = self.boardTiles
            for neighbor in next_neighbors:
                next_prefix = ''.join([prefix, tiles[neighbor]])
                next_path = path + [neighbor]
                next_node = self._getNode(tiles[neighbor], node)
                if next_node is not None:
                    self._findWords(next_prefix, next_path, next_node)

    def solve(self):
        """
        Solves the board in a two step process.

        First the list of word prefixes along with their neighbor path on the
        board is identified.

        Each prefix found is then used as a starting point for finding a
        dictionary word.
        """
        tiles = self.boardTiles
        paths = [path for position in range(1, self.boardRangeLimit)
                 for path in self._findPrefixPaths(tiles[position], [position])]
        for prefix, path, node in paths:
            self._findWords(prefix, path, node)
