# By Tanut Apiwong, ID 6238396
# Sudoku Solver
# 27 SEP 2020
import math
import time

DIMENSION = 9
SUB_DIMENSION = math.isqrt(DIMENSION)

PUZZLE = [
    0, 9, 6, 0, 4, 0, 0, 0, 0,
    0, 0, 2, 6, 0, 5, 9, 4, 7,
    4, 0, 5, 0, 9, 0, 0, 0, 6,
    6, 8, 0, 0, 0, 0, 3, 7, 4,
    5, 4, 7, 0, 0, 0, 0, 8, 2,
    3, 2, 1, 0, 7, 0, 6, 5, 0,
    0, 0, 8, 7, 0, 0, 4, 0, 3,
    9, 6, 3, 4, 8, 0, 7, 0, 5,
    1, 0, 0, 0, 5, 6, 0, 0, 8,
]


def print_board(state):
    print('  |', '  '.join(str(i) for i in range(1, DIMENSION + 1)))
    print('-' * (DIMENSION * 3 + 2))
    for r in range(DIMENSION):
        offset = r * DIMENSION
        row = state[offset: offset + DIMENSION]
        print(r + 1, '|', '  '.join(str(e) for e in row))


def find_empty_indexes(state):
    return [i for i, value in enumerate(state) if value == 0]


def has_duplicates(values):
    values = [v for v in values if v > 0]
    return len(values) != len(set(values))


def board_is_valid(state):
    """Check that no row, column, or sub-box contains a duplicate value."""
    for r in range(DIMENSION):
        offset = r * DIMENSION
        if has_duplicates(state[offset: offset + DIMENSION]):
            return False
    for c in range(DIMENSION):
        if has_duplicates(state[c:: DIMENSION]):
            return False
    for box_r in range(SUB_DIMENSION):
        for box_c in range(SUB_DIMENSION):
            box = []
            for r in range(SUB_DIMENSION):
                offset = (box_r * SUB_DIMENSION + r) * DIMENSION + box_c * SUB_DIMENSION
                box.extend(state[offset: offset + SUB_DIMENSION])
            if has_duplicates(box):
                return False
    return True


def is_valid_placement(state, index, value):
    """Check that placing value at index conflicts with no cell in the
    same row, column, or sub-box."""
    row, col = divmod(index, DIMENSION)
    row_offset = row * DIMENSION
    for c in range(row_offset, row_offset + DIMENSION):
        if state[c] == value:
            return False
    for r in range(col, DIMENSION * DIMENSION, DIMENSION):
        if state[r] == value:
            return False
    box_row = row - row % SUB_DIMENSION
    box_col = col - col % SUB_DIMENSION
    for r in range(box_row, box_row + SUB_DIMENSION):
        offset = r * DIMENSION + box_col
        for i in range(offset, offset + SUB_DIMENSION):
            if state[i] == value:
                return False
    return True


def _solve(state, empty_indexes, idx):
    if idx == len(empty_indexes):
        return True
    index = empty_indexes[idx]
    for value in range(1, DIMENSION + 1):
        if is_valid_placement(state, index, value):
            state[index] = value
            if _solve(state, empty_indexes, idx + 1):
                return True
            state[index] = 0
    return False


def solve_sudoku(state):
    """Return a solved copy of state, or None if the board is unsolvable."""
    if not board_is_valid(state):
        return None
    working = state[:]
    if _solve(working, find_empty_indexes(working), 0):
        return working
    return None


if __name__ == '__main__':
    print()
    print('Sudoku Game Board:')
    print_board(PUZZLE)

    print()
    print('Number of boxes to be filled:', len(find_empty_indexes(PUZZLE)))

    start_time = time.perf_counter()
    solved_state = solve_sudoku(PUZZLE)
    end_time = time.perf_counter()

    print()
    if solved_state is None:
        print('No solution exists for this board.')
    else:
        print('Solution:')
        print_board(solved_state)
    print('Time usage:', int((end_time - start_time) * 1000), 'ms')
