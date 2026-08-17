import unittest

from sudoku_solver import (
    DIMENSION,
    PUZZLE,
    board_is_valid,
    find_empty_indexes,
    is_valid_placement,
    solve_sudoku,
)


class SolveSudokuTest(unittest.TestCase):
    def test_solves_the_bundled_puzzle(self):
        solved = solve_sudoku(PUZZLE)
        self.assertIsNotNone(solved)
        self.assertNotIn(0, solved)
        self.assertTrue(board_is_valid(solved))
        # The given clues must be preserved in the solution.
        for i, value in enumerate(PUZZLE):
            if value != 0:
                self.assertEqual(value, solved[i])

    def test_does_not_mutate_the_input_board(self):
        original = PUZZLE[:]
        solve_sudoku(PUZZLE)
        self.assertEqual(original, PUZZLE)

    def test_unsolvable_board_returns_none(self):
        # Row 1 forces its last cell to be 9, but column 9 already
        # contains a 9 further down: valid board, yet unsolvable.
        board = [0] * (DIMENSION * DIMENSION)
        board[0:DIMENSION] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        board[4 * DIMENSION + 8] = 9
        self.assertTrue(board_is_valid(board))
        self.assertIsNone(solve_sudoku(board))

    def test_board_with_conflicting_clues_returns_none(self):
        board = [0] * (DIMENSION * DIMENSION)
        board[0] = 5
        board[1] = 5
        self.assertFalse(board_is_valid(board))
        self.assertIsNone(solve_sudoku(board))


class ValidationTest(unittest.TestCase):
    def test_empty_board_is_valid(self):
        self.assertTrue(board_is_valid([0] * (DIMENSION * DIMENSION)))

    def test_duplicate_in_column_is_invalid(self):
        board = [0] * (DIMENSION * DIMENSION)
        board[3] = 7
        board[3 + 5 * DIMENSION] = 7
        self.assertFalse(board_is_valid(board))

    def test_duplicate_in_sub_box_is_invalid(self):
        board = [0] * (DIMENSION * DIMENSION)
        board[0] = 4
        board[DIMENSION + 1] = 4
        self.assertFalse(board_is_valid(board))

    def test_is_valid_placement_checks_row_column_and_box(self):
        board = [0] * (DIMENSION * DIMENSION)
        board[0] = 1
        self.assertFalse(is_valid_placement(board, 8, 1))   # same row
        self.assertFalse(is_valid_placement(board, 72, 1))  # same column
        self.assertFalse(is_valid_placement(board, 10, 1))  # same sub-box
        self.assertTrue(is_valid_placement(board, 40, 1))
        self.assertTrue(is_valid_placement(board, 8, 2))

    def test_find_empty_indexes(self):
        board = [0] * (DIMENSION * DIMENSION)
        board[7] = 3
        empties = find_empty_indexes(board)
        self.assertEqual(DIMENSION * DIMENSION - 1, len(empties))
        self.assertNotIn(7, empties)


if __name__ == '__main__':
    unittest.main()
