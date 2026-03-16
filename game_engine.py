from game import Element, make_empty_element, is_element_empty, make_random_element,\
                 Board,  make_empty_board, clone_board, clone_element,\
                 board_fill_with_random_cells,\
                 BoardState
from matches import Match, find_matches,  get_indices_for_matches
from typing import List
from itertools import filterfalse, product
from pipe import Pipe

BOARD_DEFAULT_SIZE = 8 



def draw(board:Board) -> Board:
    sep = ' ' 
    size:int = board.size
    
    print(sep * 3, *range(0, size), sep = sep)
    print()
    for i in range(0, size):
        print(i,sep, *board.cells[i], sep = sep)  
    print()
    print('-' * (size * 2 + 3))

    return board


def make_and_draw_board(size:int) -> Board:
    board = make_empty_board(size)
    board = board_fill_with_random_cells(board)
    draw(board)
    return board


def apply_gravity(board:Board) -> Board:
    new_board = make_empty_board(board.size)
    rows_num = board.size
    cols_num = board.size

    for col in range(cols_num):
        column = (board.cells[i][col] for i in reversed(range(rows_num)))
        nonempty_elems = filterfalse(is_element_empty, column)
        for (row_ind, elem) in zip(reversed(range(rows_num)), nonempty_elems):
            new_board.cells[row_ind][col] = clone_element(elem)

    return new_board 


def erase_matched_elements(board:Board, matches:List[Match]) -> Board:
    new_board = clone_board(board)
    matches_indices = get_indices_for_matches(matches)
    for row, col in matches_indices:
        new_board.cells[row][col] = make_empty_element()
    
    return new_board


def remove_matches(board:Board, matches:List[Match]) -> Board:
    draw(board)
    new_board = erase_matched_elements(board, matches)    
    ready_board = apply_gravity(new_board)
    draw(ready_board)
    return ready_board


def fill_empty_spaces(board:Board) -> Board:
    rows_num = board.size
    cols_num = board.size
    for (row, col) in product(range(cols_num), range(rows_num)):
        if not is_element_empty(board.cells[row][col]):
            continue
        board.cells[row][col] = make_random_element()
    draw(board)
    return board


def remove_matches_and_fill_board(board:Board, matches:List[Match]) -> Board:
    return  board | Pipe(remove_matches, matches) | \
                    Pipe(draw) | \
                    Pipe(fill_empty_spaces) | \
                    Pipe(draw)      


def process_cascade(board:Board) -> Board:
    matches:List[Match] = find_matches(board)
    if matches == []:
        return board
    
    result_board = remove_matches_and_fill_board(board, matches)
    return process_cascade(result_board)


def initialize_game(board_size:int) -> BoardState:
    assert board_size > 0, "initialize_game: board size has to be > 0, actual is %s" \
                      % board_size

    board = make_empty_board(board_size) | \
            Pipe(board_fill_with_random_cells) | \
            Pipe(process_cascade) 
    
    return BoardState(0, board)




if __name__ == "__main__":
    board = make_and_draw_board(BOARD_DEFAULT_SIZE)
    matches = find_matches(board)
    print(matches)
    after_removal = erase_matched_elements(board, matches)
    draw(after_removal)
    after_gravity = apply_gravity(after_removal)
    draw(after_gravity)
    after_filling = fill_empty_spaces(after_gravity)
    draw(after_filling)

