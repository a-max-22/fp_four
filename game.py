from dataclasses import dataclass
from typing import List
import random
import copy

SYMBOL_EMPTY = ' '
elements_symbols = ('A','B','C','D','E','F')

@dataclass(frozen=True)
class Element:
    symbol:str = SYMBOL_EMPTY

    def __str__(self):
        return self.symbol

EmptyElement = Element()

def is_element_empty(elem:Element) -> Element:
    return elem.symbol == SYMBOL_EMPTY

def make_empty_element() -> Element:
    return Element()

def make_random_element() -> Element:
    return Element(random.choice(elements_symbols))

def compare_elements(elem1:Element, elem2:Element) -> bool:
    return ((elem1 != EmptyElement) and (elem1 == elem2))

def clone_element(elem:Element) -> Element:
    return copy.copy(elem)


@dataclass(frozen=True)
class Board:
    size:int
    cells:List[List[Element]]


def make_empty_board(size:int) -> Board:
    assert size > 0, "make_empty_board: board size has to be > 0, actual is %s" \
                      % size

    cells = [[make_empty_element() for _ in  range(size)] \
             for _ in range(size)]
    return Board(size, cells)


def board_fill_with_random_cells(board:Board) -> Board:
    size:int = board.size
    new_cells = [[make_random_element() for _ in range(size)] \
                  for _ in range(size)]
    return Board(size, new_cells)


def clone_board(board:Board) -> Board:
    return copy.deepcopy(board)



@dataclass(frozen=True)
class BoardState:
    score:int
    board:Board

