import random

def print_board(board, reveal=False, solution=None):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            # Show answer only for empty cells if reveal is True
            if reveal and solution and val == " ":
                print(f"[{solution[i][j]}]", end=" ")
            else:
                print(val if val != " " else ".", end=" ")
        print()
    print()

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[startRow + i][startCol + j] == num:
                return False
    return True

def solve(board, find_all=False, count=[0], solution=None):
    for i in range(9):
        for j in range(9):
            if board[i][j] == " ":
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board, find_all, count, solution):
                            if not find_all:
                                return True
                        board[i][j] = " "
                return False
    count[0] += 1
    if solution is not None:
        for i in range(9):
            for j in range(9):
                solution[i][j] = board[i][j]
    return True

def fill_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == " ":
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = " "
                return False
    return True

def generate_puzzle():
    board = [[" " for _ in range(9)] for _ in range(9)]
    fill_board(board)
    solution = [row[:] for row in board]
    puzzle = [row[:] for row in board]
    attempts = 50
    while attempts > 0:
        row, col = random.randint(0,8), random.randint(0,8)
        if puzzle[row][col] == " ":
            continue
        backup = puzzle[row][col]
        puzzle[row][col] = " "
        copy_board = [r[:] for r in puzzle]
        count = [0]
        solve(copy_board, find_all=True, count=count)
        if count[0] != 1:
            puzzle[row][col] = backup
            attempts -= 1
    return puzzle, solution

def is_finished(board):
    for row in board:
        if " " in row:
            return False
    return True

def tutorial():
    print("""
Welcome to Sudoku!

How to play:
- Fill the grid so each row, column, and 3x3 box contains numbers 1-9 exactly once.
- Enter moves as: row col num
  (e.g. 1 3 4 for row 1, col 3, number 4)
- To reveal the solution for empty cells, type 'answer'.
- Empty cells are marked with '.' (dot).
- When you reveal, your guesses remain, and missing answers are shown in [brackets].

Enjoy!
""")

tutorial()
puzzle, solution = generate_puzzle()
print_board(puzzle)

while not is_finished(puzzle):
    entry = input("Enter move as row col num (e.g. 1 3 4), or type 'answer' to reveal: ").strip()
    if entry.lower() == "answer":
        print("\nRevealed solution (your guesses stay, empty cells show answer in [brackets]):")
        print_board(puzzle, reveal=True, solution=solution)
        continue
    try:
        r, c, n = map(int, entry.split())
        r -= 1
        c -= 1
        if not (0 <= r < 9 and 0 <= c < 9):
            print("Row and column must be between 1 and 9.")
            continue
        if puzzle[r][c] != " ":
            print("Cell already filled!")
            continue
        if not (1 <= n <= 9):
            print("Number must be between 1 and 9.")
            continue
        if is_valid(puzzle, r, c, n):
            puzzle[r][c] = n
            print_board(puzzle)
        else:
            print("Invalid move! Try again.")
    except Exception:
        print("Invalid input. Try again.")

print("\nCongratulations, you solved the Sudoku!")