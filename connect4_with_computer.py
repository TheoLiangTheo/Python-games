import random

# Initialize board
board = []
for x in range(6):
    board.append([])
    for y in range(7):
        board[-1].append(None)

def printboard(board):
    for x in range(6):
        for y in range(7):
            if board[x][y] == None:
                print('|   ', end='')
            elif board[x][y] == 'x':
                print('| X ', end='')
            else:
                print('| O ', end='')
        print('|')
        print('_____________________________')
    print('  1   2   3   4   5   6   7  ')

def move(p, board):
    last = 0
    valid = False
    played = False
    x1 = False
    if -1 < p < 7:
        for x in range(6):
            if board[x][p] == None:
                last = x
            else:
                if x == 0:
                    print('invalid move')
                    x1 = True
                    break
                else:
                    board[last][p] = 'x'
                    valid = True
                    played = True
        if not played and not x1:
            board[last][p] = 'x'
            valid = True
    else:
        print('invalid move')
    return valid

def o_move(p, board):
    last = 0
    valid = False
    played = False
    x1 = False
    if -1 < p < 7:
        for x in range(6):
            if board[x][p] == None:
                last = x
            else:
                if x == 0:
                    x1 = True
                    break
                else:
                    board[last][p] = 'o'
                    valid = True
                    played = True
        if not played and not x1:
            board[last][p] = 'o'
            valid = True
    return valid

def four(maze):
    connected = False
    for x in range(6):
        for y in range(4):
            if maze[x][y] == maze[x][y+1] == maze[x][y+2] == maze[x][y+3]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    for x in range(3):
        for y in range(7):
            if maze[x][y] == maze[x+1][y] == maze[x+2][y] == maze[x+3][y]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    for x in range(3,6):
        for y in range(4):
            if maze[x][y] == maze[x-1][y+1] == maze[x-2][y+2] == maze[x-3][y+3]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    for x in range(3):
        for y in range(4):
            if maze[x][y] == maze[x+1][y+1] == maze[x+2][y+2] == maze[x+3][y+3]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    return connected

def draw(board):
    draw = True
    for x in range(6):
        for y in range(7):
            if board[x][y] == None:
                draw = False
                break
    if draw:
        print("It's a draw!")
    return draw

def valid_moves(board):
    return [c for c in range(7) if board[0][c] == None]

def simulate_move(board, col, piece):
    temp = [row[:] for row in board]
    for x in range(5, -1, -1):
        if temp[x][col] is None:
            temp[x][col] = piece
            break
    return temp

def computer(board):
    # Try to win
    for col in valid_moves(board):
        temp = simulate_move(board, col, 'o')
        if four(temp):
            o_move(col, board)
            return
    # Try to block player
    for col in valid_moves(board):
        temp = simulate_move(board, col, 'x')
        if four(temp):
            o_move(col, board)
            return
    # Otherwise, random move
    col = random.choice(valid_moves(board))
    o_move(col, board)

printboard(board)
while True:
    while True:
        try:
            p1 = int(input('player 1, where would you like to go? ')) - 1
            m = move(p1, board)
            if m:
                printboard(board)
                break
        except ValueError:
            print('Please enter a number between 1 and 7.')
    if four(board):
        break
    print("computer, where would you like to go? ")
    computer(board)
    printboard(board)
    if four(board):
        break
    if draw(board):
        break