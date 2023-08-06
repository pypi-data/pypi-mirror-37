from setuptools import setup, find_packages

long_description = """
A suite of classes that model the elements of the Hasbro game. Boards of 
different sizes can be randomly generated from a collection of  dice.
Given a list of words, a puzzle can be solved by finding all of the words on
the Boggle board.

BoggleDice - The game dice - you can roll them.
BoggleBoard - The board, place the dice on the board and shake it!
BoggleWords - A dictionary for finding words.
BoggleSolver - Finds words from the dictionary that are on the board.

The official game letters and a dictionary file are NOT included.
"""

setup(
    name="boggled",
    description="Simple Boggle game solver and generator.",
    version="1.0.0",
    author="Dan Nagle",
    author_email="d.a.nagle@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danag/boggled",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
