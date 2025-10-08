import copy

def print_tutorial():
    print("""
Welcome to Console Chess!

RULES:
- Standard chess rules apply: move pieces to capture, check, and checkmate your opponent.
- White always moves first.
- The game detects check, checkmate, and stalemate automatically.

CONTROLS:
- Enter moves in the format: e2 e4
  (This means move the piece from e2 to e4.)
- To castle, move your king two squares: e1 g1 (white kingside), e1 c1 (white queenside), e8 g8 (black kingside), e8 c8 (black queenside).
- When a pawn reaches the last rank, you can choose promotion: Q (Queen), R (Rook), B (Bishop), N (Knight).
- En passant is supported when possible.

PIECE SYMBOLS:
  P / p : Pawn
  R / r : Rook
  N / n : Knight
  B / b : Bishop
  Q / q : Queen
  K / k : King
  Uppercase: White, Lowercase: Black

TO WIN:
- Checkmate your opponent's king.
- Stalemate is a draw.

Press Enter to start the game!
""")
    input()

def create_board():
    return [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"]
    ]

def print_board(board):
    print("  a b c d e f g h")
    for i, row in enumerate(board):
        print(8-i, end=" ")
        for piece in row:
            print(piece, end=" ")
        print(8-i)
    print("  a b c d e f g h")

def parse_move(move):
    try:
        start, end = move.split()
        sx, sy = ord(start[0]) - ord('a'), 8-int(start[1])
        ex, ey = ord(end[0]) - ord('a'), 8-int(end[1])
        return sy, sx, ey, ex
    except:
        return None

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def find_king(board, color):
    k = "K" if color == "white" else "k"
    for y in range(8):
        for x in range(8):
            if board[y][x] == k:
                return (y, x)
    return None

def is_attacked(board, y, x, attacker_color, ep_square=None):
    directions = [
        (1,0), (-1,0), (0,1), (0,-1),
        (1,1), (-1,-1), (1,-1), (-1,1)
    ]
    if attacker_color == "white":
        for dx in [-1,1]:
            ny, nx = y-1, x+dx
            if in_bounds(nx, ny) and board[ny][nx] == "P":
                return True
        if ep_square and (y, x) == ep_square:
            return True
    else:
        for dx in [-1,1]:
            ny, nx = y+1, x+dx
            if in_bounds(nx, ny) and board[ny][nx] == "p":
                return True
        if ep_square and (y, x) == ep_square:
            return True
    for dy, dx in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
        ny, nx = y+dy, x+dx
        if in_bounds(nx, ny):
            piece = board[ny][nx]
            if attacker_color == "white" and piece == "N":
                return True
            if attacker_color == "black" and piece == "n":
                return True
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            if dy == 0 and dx == 0: continue
            ny, nx = y+dy, x+dx
            if in_bounds(nx, ny):
                piece = board[ny][nx]
                if attacker_color == "white" and piece == "K":
                    return True
                if attacker_color == "black" and piece == "k":
                    return True
    for dy, dx in directions:
        for i in range(1,8):
            ny, nx = y + dy*i, x + dx*i
            if not in_bounds(nx, ny): break
            piece = board[ny][nx]
            if piece == ".":
                continue
            if attacker_color == "white":
                if piece == "Q" or (piece == "R" and (dx==0 or dy==0)) or (piece == "B" and dx!=0 and dy!=0):
                    return True
                break
            else:
                if piece == "q" or (piece == "r" and (dx==0 or dy==0)) or (piece == "b" and dx!=0 and dy!=0):
                    return True
                break
    return False

def legal_moves(board, turn, castling_rights, ep_square):
    moves = []
    for sy in range(8):
        for sx in range(8):
            piece = board[sy][sx]
            if piece == ".":
                continue
            if turn == "white" and piece.islower():
                continue
            if turn == "black" and piece.isupper():
                continue
            moves += piece_moves(board, sy, sx, turn, castling_rights, ep_square)
    legal = []
    for sy, sx, ey, ex, promote, ep in moves:
        temp = copy.deepcopy(board)
        temp[ey][ex] = temp[sy][sx]
        temp[sy][sx] = "."
        if ep:
            temp[sy][ex] = "."
        if promote:
            temp[ey][ex] = promote
        king = find_king(temp, turn)
        if king and not is_attacked(temp, king[0], king[1], "black" if turn=="white" else "white", ep_square):
            legal.append((sy,sx,ey,ex,promote,ep))
    return legal

def piece_moves(board, sy, sx, turn, castling_rights, ep_square):
    piece = board[sy][sx]
    moves = []
    if piece in "Pp":
        direction = -1 if piece == "P" else 1
        ny = sy + direction
        if in_bounds(sx, ny) and board[ny][sx] == ".":
            if (piece == "P" and ny == 0) or (piece == "p" and ny == 7):
                promo = choose_promotion(turn)
                moves.append((sy,sx,ny,sx,promo,False))
            else:
                moves.append((sy,sx,ny,sx,None,False))
            if (piece == "P" and sy == 6) or (piece == "p" and sy == 1):
                ny2 = sy + 2*direction
                if board[ny2][sx] == "." and board[ny][sx] == ".":
                    moves.append((sy,sx,ny2,sx,None,False))
        for dx in [-1,1]:
            nx = sx+dx
            if in_bounds(nx, ny):
                dest = board[ny][nx]
                if dest != "." and ((turn == "white" and dest.islower()) or (turn == "black" and dest.isupper())):
                    if (piece == "P" and ny == 0) or (piece == "p" and ny == 7):
                        promo = choose_promotion(turn)
                        moves.append((sy,sx,ny,nx,promo,False))
                    else:
                        moves.append((sy,sx,ny,nx,None,False))
            if ep_square and (ny, nx) == ep_square:
                moves.append((sy,sx,ny,nx,None,True))
    directions = []
    if piece in "Rr":
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
    if piece in "Bb":
        directions = [(1,1),(-1,-1),(1,-1),(-1,1)]
    if piece in "Qq":
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
    for dy, dx in directions:
        for i in range(1,8):
            ny, nx = sy + dy*i, sx + dx*i
            if not in_bounds(nx, ny): break
            dest = board[ny][nx]
            if dest == ".":
                moves.append((sy,sx,ny,nx,None,False))
            elif (turn == "white" and dest.islower()) or (turn == "black" and dest.isupper()):
                moves.append((sy,sx,ny,nx,None,False))
                break
            else:
                break
    if piece in "Nn":
        for dy, dx in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
            ny, nx = sy+dy, sx+dx
            if in_bounds(nx, ny):
                dest = board[ny][nx]
                if dest == "." or (turn == "white" and dest.islower()) or (turn == "black" and dest.isupper()):
                    moves.append((sy,sx,ny,nx,None,False))
    if piece in "Kk":
        for dy in [-1,0,1]:
            for dx in [-1,0,1]:
                if dy == 0 and dx == 0: continue
                ny, nx = sy+dy, sx+dx
                if in_bounds(nx, ny):
                    dest = board[ny][nx]
                    if dest == "." or (turn == "white" and dest.islower()) or (turn == "black" and dest.isupper()):
                        moves.append((sy,sx,ny,nx,None,False))
        if turn == "white" and sy == 7 and sx == 4 and board[7][4] == "K":
            if castling_rights["white_kingside"]:
                if board[7][5] == "." and board[7][6] == "." and board[7][7] == "R":
                    if not is_attacked(board,7,4,"black") and not is_attacked(board,7,5,"black") and not is_attacked(board,7,6,"black"):
                        moves.append((7,4,7,6,None,False))
            if castling_rights["white_queenside"]:
                if board[7][1] == "." and board[7][2] == "." and board[7][3] == "." and board[7][0] == "R":
                    if not is_attacked(board,7,4,"black") and not is_attacked(board,7,3,"black") and not is_attacked(board,7,2,"black"):
                        moves.append((7,4,7,2,None,False))
        if turn == "black" and sy == 0 and sx == 4 and board[0][4] == "k":
            if castling_rights["black_kingside"]:
                if board[0][5] == "." and board[0][6] == "." and board[0][7] == "r":
                    if not is_attacked(board,0,4,"white") and not is_attacked(board,0,5,"white") and not is_attacked(board,0,6,"white"):
                        moves.append((0,4,0,6,None,False))
            if castling_rights["black_queenside"]:
                if board[0][1] == "." and board[0][2] == "." and board[0][3] == "." and board[0][0] == "r":
                    if not is_attacked(board,0,4,"white") and not is_attacked(board,0,3,"white") and not is_attacked(board,0,2,"white"):
                        moves.append((0,4,0,2,None,False))
    return moves

def choose_promotion(turn):
    while True:
        promo = input(f"{turn.capitalize()} pawn promotion! Choose (Q,R,B,N): ").upper()
        if promo in "QRBN":
            return promo if turn == "white" else promo.lower()

def make_move(board, sy, sx, ey, ex, promote, ep, castling_rights, turn):
    piece = board[sy][sx]
    board[ey][ex] = piece
    board[sy][sx] = "."
    ep_square = None
    if promote:
        board[ey][ex] = promote
    if piece in "Kk" and abs(ex - sx) == 2:
        if turn == "white":
            if ex == 6:
                board[7][5] = board[7][7]
                board[7][7] = "."
            elif ex == 2:
                board[7][3] = board[7][0]
                board[7][0] = "."
            castling_rights["white_kingside"] = False
            castling_rights["white_queenside"] = False
        else:
            if ex == 6:
                board[0][5] = board[0][7]
                board[0][7] = "."
            elif ex == 2:
                board[0][3] = board[0][0]
                board[0][0] = "."
            castling_rights["black_kingside"] = False
            castling_rights["black_queenside"] = False
    if ep:
        if turn == "white":
            board[ey+1][ex] = "."
        else:
            board[ey-1][ex] = "."
    if piece == "P" and sy == 6 and ey == 4 and sx == ex:
        ep_square = (5, sx)
    elif piece == "p" and sy == 1 and ey == 3 and sx == ex:
        ep_square = (2, sx)
    else:
        ep_square = None
    if piece == "R" and sy == 7 and sx == 7:
        castling_rights["white_kingside"] = False
    if piece == "R" and sy == 7 and sx == 0:
        castling_rights["white_queenside"] = False
    if piece == "r" and sy == 0 and sx == 7:
        castling_rights["black_kingside"] = False
    if piece == "r" and sy == 0 and sx == 0:
        castling_rights["black_queenside"] = False
    if piece == "K":
        castling_rights["white_kingside"] = False
        castling_rights["white_queenside"] = False
    if piece == "k":
        castling_rights["black_kingside"] = False
        castling_rights["black_queenside"] = False
    return ep_square

def is_check(board, turn, ep_square):
    king = find_king(board, turn)
    if not king:
        return False
    return is_attacked(board, king[0], king[1], "black" if turn=="white" else "white", ep_square)

# --- TUTORIAL ---
print_tutorial()

# --- GAME LOOP ---
board = create_board()
turn = "white"
castling_rights = {
    "white_kingside": True,
    "white_queenside": True,
    "black_kingside": True,
    "black_queenside": True
}
ep_square = None

while True:
    print_board(board)
    legal = legal_moves(board, turn, castling_rights, ep_square)
    if not legal:
        if is_check(board, turn, ep_square):
            print(f"Checkmate! {'Black' if turn=='white' else 'White'} wins!")
        else:
            print("Stalemate!")
        break
    if is_check(board, turn, ep_square):
        print(f"{turn.capitalize()} is in check!")
    print(f"{turn.capitalize()}'s move (e.g. 'e2 e4'):")
    move = input()
    parsed = parse_move(move)
    if not parsed:
        print("Invalid format! Use e.g.: e2 e4")
        continue
    sy, sx, ey, ex = parsed
    chosen = None
    for m in legal:
        if m[0] == sy and m[1] == sx and m[2] == ey and m[3] == ex:
            chosen = m
            break
    if not chosen:
        print("Illegal move!")
        continue
    promote = chosen[4]
    ep = chosen[5]
    ep_square = make_move(board, sy, sx, ey, ex, promote, ep, castling_rights, turn)
    turn = "black" if turn == "white" else "white"