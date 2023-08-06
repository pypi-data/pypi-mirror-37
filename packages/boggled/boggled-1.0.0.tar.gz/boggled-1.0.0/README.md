# About Boggled

This is a simple [Boggle](https://en.wikipedia.org/wiki/Boggle) solver/generator package I created as part of a pet project to give a young person in our household a fighting chance against their older siblings.

The project was also intended as a learning opportunity for my son so the code has been documented well enough for a child to understand how it works.

## Note

Neither a dictionary file nor the letters for creating the Boggle dice are provided with the package as I didn't want to tie the package to any particular language. There are suitable resources freely available online.

[WordGameDictionary.com](https://www.wordgamedictionary.com/word-lists/)

The following links detail the letter distributions for various versions of the official game:

- [The Boggle (4x4) redesign and its effect on the difficulty of Boggle](http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html)
- [5x5 Boggle Letter Distribution](https://boardgamegeek.com/thread/300883/letter-distribution)
- [6x6 Boggle Letter Distribution](https://boardgamegeek.com/thread/1071406/looking-letter-distribution)
- [Non-English language versions](https://boardgames.stackexchange.com/questions/29264/boggle-what-is-the-dice-configuration-for-boggle-in-various-languages)

## Simple Solver Example

```python
from boggled import BoggleBoard, BoggleSolver, BoggleWords

words_file = "english.txt"
letters = "AILN SNLC IHIF QU DIK"

gameBoard = BoggleBoard(letters)
gameWords = BoggleWords()
gameWords.loadFromFile(words_file)

solver = BoggleSolver(gameBoard, gameWords)

solver.solve()

print(solver.foundWords)
```

If the dictionary provided the words, the following list would be output:

```python
['ASH', 'DILL', 'DISH', 'FILL', 'FIN', 'FINISH', 'FINS', 'HILL', 'ILL', 'KID', 'KILN', 'KIN', 'LID', 'NAIL', 'NASH', 'NIL', 'QUID', 'SAIL', 'SHIN', 'SILL', 'SIN', 'SNAIL']
```

## TODO

[] Write better tests

- There is 99% test coverage of the code but the quality of the tests could be improved.

[] Add examples of usage.

## Thanks

A big thank you to the creators of Boggle as it has provided endless hours of entertainment in our house.

Boggle<sup>TM</sup> is a registered trademark of [Hasbro, Inc.](https://hasbro.gcs-web.com/)
