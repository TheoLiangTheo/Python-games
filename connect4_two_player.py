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


def move(p, n, board):
    last = 0
    valid = False
    played = False
    x1 = False
    if p > -1 and p < 7:
        for x in range(6):
            if board[x][p] == None:
                last = x
            else:
                if x == 0:
                    print('invalid move')
                    x1 = True
                    break
                else:
                    if n == 1:
                        board[last][p] = 'x'
                    else:
                        board[last][p] = 'o'
                    valid = True
                    played = True
        if not played and not x1:
            if n == 1:
                board[last][p] = 'x'
            else:
                board[last][p] = 'o'
            valid = True
    else:
        print('invalid move')
    return valid


def four(maze):
    connected = False
    for x in range(6):
        for y in range(4):
            if maze[x][y] == maze[x][y + 1] and maze[x][y] == maze[x][y + 2] and maze[x][y] == maze[x][y + 3]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    for x in range(3):
        for y in range(7):
            if maze[x][y] == maze[x + 1][y] and maze[x][y] == maze[x + 2][y] and maze[x][y] == maze[x + 3][y]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    for x in range(3, 6):
        for y in range(4):
            if maze[x][y] == maze[x - 1][y + 1] and maze[x][y] == maze[x - 2][y + 2] and maze[x][y] == maze[x - 3][
                y + 3]:
                if maze[x][y] == 'o':
                    print('player 2 wins!')
                    connected = True
                elif maze[x][y] == 'x':
                    print('player 1 wins!')
                    connected = True
    for x in range(3):
        for y in range(4):
            if maze[x][y] == maze[x + 1][y + 1] and maze[x][y] == maze[x + 2][y + 2] and maze[x][y] == maze[x + 3][
                y + 3]:
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


while True:
    printboard(board)
    while True:
        p1 = int(input('player 1, which would you like to go? ')) - 1
        m = move(p1, 1, board)
        if m:
            printboard(board)
            break
    if four(board):
        break
    while True:
        p2 = int(input("player 2, which would you like to go? ")) - 1
        m = move(p2, 2, board)
        if m:
            printboard(board)
            break
    if four(board):
        break
    if draw(board):
        break