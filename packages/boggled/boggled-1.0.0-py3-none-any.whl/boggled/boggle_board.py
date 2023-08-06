# boggle_board.py
"""
Library to build a representation of the Boggle board and provide the solver
with a simple map to navigate between neighboring tiles on the board.
"""
from math import floor, sqrt
from re import sub


class BoggleBoard():
    """
    Represents a view of the letter tiles for the puzzle to be solved.
    """

    def __init__(self, tiles=None):
        """
        Initialise the empty board and fill it with letter tiles if provided.
        """
        self._columns = None
        self._neighbors = None
        self._rangeLimit = None
        self._rows = None
        self._tiles = None
        if tiles:
            self.createBoard(tiles)

    @property
    def columns(self):
        """
        The number of columns in the grid that makes up the board.

        The property is populated when the `createBoard` method is called.

        >>> ex = BoggleBoard('ABCD EFGH IJKL MNOP')
        >>> ex.columns
        4
        """
        return self._columns

    @property
    def neighbors(self):
        """
        A dict structure in which the keys are the enumerated positions on the
        board and the values are the list of neighbors for that position.

        The property is populated when the `createBoard` method is called.

        >>> ex = BoggleBoard('A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P')
        >>> isinstance(ex.tiles, dict)
        True
        >>> len(ex.neighbors)
        16
        >>> ex.neighbors.keys()
        dict_keys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        >>> isinstance(ex.neighbors[1], list)
        True
        >>> ex.neighbors[1]
        [6, 2, 5]
        >>> ex.neighbors[2]
        [1, 3, 5, 6, 7]
        >>> ex.neighbors[3]
        [2, 4, 6, 7, 8]
        >>> ex.neighbors[4]
        [3, 7, 8]
        >>> ex.neighbors[5]
        [1, 2, 6, 9, 10]
        >>> ex.neighbors[6]
        [1, 2, 3, 5, 7, 9, 10, 11]
        >>> ex.neighbors[7]
        [2, 3, 4, 6, 8, 10, 11, 12]
        >>> ex.neighbors[8]
        [3, 4, 7, 11, 12]
        >>> ex.neighbors[9]
        [5, 6, 10, 13, 14]
        >>> ex.neighbors[10]
        [5, 6, 7, 9, 11, 13, 14, 15]
        >>> ex.neighbors[11]
        [6, 7, 8, 10, 12, 14, 15, 16]
        >>> ex.neighbors[12]
        [7, 8, 11, 15, 16]
        >>> ex.neighbors[13]
        [9, 10, 14]
        >>> ex.neighbors[14]
        [9, 10, 11, 13, 15]
        >>> ex.neighbors[15]
        [10, 11, 12, 14, 16]
        >>> ex.neighbors[16]
        [11, 12, 15]
        """
        return self._neighbors

    @property
    def rangeLimit(self):
        """
        The upper limit for the range of the tiles on the board.

        The property is populated when the `createBoard` method is called.

        >>> ex = BoggleBoard('A B C D E F G H I J K L M N O P')
        >>> ex.rangeLimit
        17
        """
        return self._rangeLimit

    @property
    def rows(self):
        """
        The number of rows in the grid that makes up the board.

        The property is populated when the `createBoard` method is called.

        >>> ex = BoggleBoard('ABCDEFGHIJKLMNOP')
        >>> ex.rows
        4
        """
        return self._rows

    @property
    def tiles(self):
        """
        A dict structure in which the keys are the enumerated positions on the
        board and the values content of the letter tile.

        The property is populated when the `createBoard` method is called.

        >>> ex = BoggleBoard('ABCDEFGHIJKLMNOP')
        >>> isinstance(ex.tiles, dict)
        True
        >>> len(ex.tiles)
        16
        >>> ex.tiles.keys()
        dict_keys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        >>> ex.tiles[1]
        'A'
        >>> ex.tiles[8]
        'H'
        >>> ex.tiles[16]
        'P'
        """
        return self._tiles

    @tiles.setter
    def tiles(self, new_tiles: str):
        """
        Repopulates the board with new tiles.
        """
        self.createBoard(new_tiles)

    def createBoard(self, tiles):
        """
        Creates the board and determines its properties by parsing the string
        of tile values.

        Args:
            tiles: String of characters to be placed on the board.

        Any fragment will be split into individual characters if it is more
        than two characters in length.

        The string can be in a number of formats and mixed formats are handled:
        >>> ex_1 = BoggleBoard()
        >>> ex_1.createBoard('ABCDEFGH')
        >>> len(ex_1.tiles)
        8
        >>> ex_1.tiles
        {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}
        >>> ex_2 = BoggleBoard()
        >>> ex_2.createBoard('A B C D E F')
        >>> len(ex_2.tiles)
        6
        >>> ex_2.tiles
        {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F'}
        >>> ex_3 = BoggleBoard()
        >>> ex_3.createBoard('Z, X, Y, W, V, U')
        >>> len(ex_3.tiles)
        6
        >>> ex_3.tiles
        {1: 'Z', 2: 'X', 3: 'Y', 4: 'W', 5: 'V', 6: 'U'}
        >>> ex_4 = BoggleBoard()
        >>> ex_4.createBoard('A, B CH TH E,F')
        >>> len(ex_4.tiles)
        6
        >>> ex_4.tiles
        {1: 'A', 2: 'B', 3: 'CH', 4: 'TH', 5: 'E', 6: 'F'}
        """
        if tiles.isalpha():
            _list = [ch for ch in tiles]
        else:
            _list = []
            for el in (sub(r'\W+', ' ', tiles)).split():
                _list.extend([ch for ch in el] if (len(el) > 2) else [el])
        self._tiles = {pos: tile.upper()
                       for pos, tile in enumerate(_list, 1)}
        num_tiles = len(self._tiles)
        cols = floor(sqrt(num_tiles))
        while num_tiles % cols is not 0:
            cols -= 1
        # TODO: What to do if we are left with a single column?
        # i.e. num_tiles is a prime number
        self._rows = num_tiles // cols
        self._columns = cols
        self._rangeLimit = num_tiles + 1
        self._neighbors = {p: [n for n in self.positionNeighbors(p)]
                           for p in range(1, self._rangeLimit)}

    def positionNeighbors(self, position: int):
        """
        Returns a list of valid neighbors for the provided board position.
        Raises an IndexError if the position is not in the enumerated board.

        Args:
            position: int in the range of 1 to the total number of tiles.

        This method is called within the `createBoard` method to populate the
        neighbors property.

        Knowing the number of columns in a grid and the total number of
        positions it contains allows the neighbors for a given position to be
        determined easily.

        Using the following grid as an example:
        +---+---+---+---+
        |1  |2  |3  |4  |
        | A | B | C | D |
        +---+---+---+---+
        |5  |6  |7  |8  |
        | E | F | G | H |
        +---+---+---+---+
        |9  |10 |11 |12 |
        | I | J | K | L |
        +---+---+---+---+
        |13 |14 |15 |16 |
        | M | N | O | P |
        +---+---+---+---+

        Number of columns = 4
        Number of positions = 16

        Each position in the grid potentially has 8 neighbors as illustrated
        in the grid below.

        +---+---+---+
        |0  |1  |2  |
        |   |   |   |
        +---+---+---+
        |3  |4  |5  |
        |   | X |   |
        +---+---+---+
        |6  |7  |8  |
        |   |   |   |
        +---+---+---+

        The list of possible neighbors for 'X' is [0, 1, 2, 3, 5, 6, 7, 8].

        The position value for each possible neighbor in the list can be
        determined by applying the appropriate calculation from the following:

        0 : (current position) - (number of columns + 1)
        1 : (current position) - (number of columns)
        2 : (current position) - (number of columns - 1)
        3 : (current position) - 1
        5 : (current position) + 1
        6 : (current position) + (number of columns - 1)
        7 : (current position) + (number of columns)
        8 : (current position) + (number of columns + 1)

        The positions on the edge of the board will have fewer valid neighbors.

        The enumerated board positions simplifies the checks that need to be
        performed to find a position's neighbors.

        Board properties for eliminating neighbors for each edge case:

        Top    : (current position) - (number of columns) < 1
        Right  : (current position) % (number of columns) = 0
        Left   : (current position) % (number of columns) = 1
        Bottom : (current position) + (number of columns) > (positions count)

        Applying these rules will determine a list of neighbors that are not
        valid for the given position. The list may contain duplicate items,
        these are removed by creating a set from the list.

        The set of valid neighbors is the set of all neighbors less the set
        of invalid neighbors.

        >>> ex = BoggleBoard('A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P')
        >>> ex.positionNeighbors(2)
        [1, 3, 5, 6, 7]
        >>> ex.positionNeighbors(4)
        [3, 7, 8]
        >>> ex.positionNeighbors(5)
        [1, 2, 6, 9, 10]
        >>> ex.positionNeighbors(7)
        [2, 3, 4, 6, 8, 10, 11, 12]
        >>> ex.positionNeighbors(12)
        [7, 8, 11, 15, 16]
        >>> ex.positionNeighbors(14)
        [9, 10, 11, 13, 15]
        """
        if 1 <= position < self._rangeLimit:
            cols = self._columns
            possible_neighbors = [-(cols + 1), -(cols), -(cols - 1),
                                  -1, 0, +1,
                                  (cols - 1), cols, (cols + 1)]
            invalid_neighbors = [4]
            if position - cols < 1:
                invalid_neighbors.extend([0, 1, 2])
            if (position % cols) == 0:
                invalid_neighbors.extend([2, 5, 8])
            if (position % cols) == 1:
                invalid_neighbors.extend([0, 3, 6])
            if position + cols >= self._rangeLimit:
                invalid_neighbors.extend([6, 7, 8])
            valid_neighbors = set(range(9)).difference(set(invalid_neighbors))
            return [(position + possible_neighbors[n])
                    for n in valid_neighbors]
        raise IndexError
