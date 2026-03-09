from typing import List 
from enum import Enum
from dataclasses import dataclass
from typing import Iterator, Any, Callable, Generator

from game import Board, EmptyElement, compare_elements


MATCH_LENGTH = 3

class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

@dataclass(frozen=True)
class Match:
    direction:Direction
    row:int
    col:int
    len:int


def add_match_if_valid(matches:List[Match], row:int, col:int, length:int,\
                       direction:Direction) -> List[Match]:
    if length >= MATCH_LENGTH:
        matches.append(Match(direction, row, col, length))
    return matches


def find_continuous_subsequences(items: Iterator[tuple[int,Any]],\
                                 desired_sequence_len:int,
                                 compare_func:Callable,\
                                 default_value:Any) -> List[tuple[int,int]]:

    subsequences: List[tuple[int,int]] = []
    sequence_item = default_value
    sequence_start_ind = 0
    
    for index, item in items:
        if compare_func(item, sequence_item):
            continue
        length = index - sequence_start_ind
        if length >= desired_sequence_len:
            subsequences.append((sequence_start_ind, length))
        sequence_start_ind, sequence_item = index, item    

    length = index - sequence_start_ind + 1
    if length >= desired_sequence_len:
        subsequences.append((sequence_start_ind, length))

    return subsequences


def find_matches(board:Board) -> List[Match]:
    matches:List[Match] = []
    rows_num = board.size
    cols_num = board.size

    # find horizontal matches
    for row in range(rows_num):
        subseqs = find_continuous_subsequences(enumerate(board.cells[row]), \
                                               MATCH_LENGTH,\
                                               compare_elements, EmptyElement)
        
        matches += [Match(Direction.HORIZONTAL, row, col, length) \
                    for col, length in subseqs]

    # find vertical matches
    for col in range(cols_num):
        column = (board.cells[i][col] for i in range(rows_num))
        subseqs = find_continuous_subsequences(enumerate(column),\
                                               MATCH_LENGTH,\
                                               compare_elements, EmptyElement)

        matches += [Match(Direction.VERTICAL, row, col, length) \
                    for row, length in subseqs]

    return matches


def get_indices_for_match(match:Match) -> \
                          Generator[tuple[int,int], None, None]:
    
    if match.direction == Direction.VERTICAL:
        return ( (match.row + i, match.col) for i in range(match.len) )
    elif match.direction == Direction.HORIZONTAL:
        return ( (match.row, match.col + i) for i in range(match.len) )
    
    assert False, "match_to_board_indices: unknown direction %x" % match.direction


def get_indices_for_matches(matches:Iterator[Match]) -> \
                            Generator[tuple[int,int], None, None]:
    
    for match_indices in map(get_indices_for_match, matches):
        yield from match_indices


def test_subsequences():
    row = ['F', 'C', 'B', 'E', 'C', 'C', 'C', 'C']
    cmp = lambda a,b: a==b
    subseqs = find_continuous_subsequences(enumerate(row), 2, 
                                           cmp, '0')
    assert subseqs[0] == (4,4)

if __name__ == "__main__":
    test_subsequences()