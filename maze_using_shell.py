hard_maze = [
    [1,0,1,1,0,1,0,0,0,0,0,0,1,0,3],
    [1,0,0,0,0,1,0,1,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,1,0,1,1,1,1,0,0],
    [1,2,1,0,1,0,1,1,0,0,0,0,0,1,0],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,1,0],
    [1,0,1,0,1,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,1,0,1,1,1,1,1],
    [0,1,1,1,1,0,1,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1]
]
#hard maze option
medium_maze = [
    [1,0,1,1,0,1,0,1,0,0,0,0,1,1,3],
    [1,0,0,0,0,1,0,1,0,1,1,0,0,0,0],
    [1,0,1,0,1,0,0,1,0,1,1,1,1,1,0],
    [1,2,1,0,0,0,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1]
]
#medium maze option
easy_maze = [
    [1,0,0,0,1],
    [1,0,1,0,0],
    [0,0,1,1,0],
    [0,1,0,1,3],
    [0,2,0,0,1],
    [1,1,1,1,1]
]
#easy maze option
def printmaze(maze,player_row,player_col):#print out the whole maze
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            if x == player_row and y == player_col:
                print('P', end = ' ')#print player location
            elif maze[x][y] == 1:
                print('#', end = ' ')#print walls
            elif maze[x][y] == 2:
                print('S', end = ' ')#print start
            elif maze[x][y] == 3:
                print('E', end = ' ')#print end
            else:
                print('.', end = ' ')#print paths
        print()
def move(direction,row,col,maze,end_row,end_col):#move options
    if direction == 'w':
        if row == 0 or maze[row-1][col] == 1:
            print('invalid move')
        else:
            row -= 1
            return(row,col)
    elif direction == 's':
        if row == len(maze)-1 or maze[row+1][col] == 1:
            print('invalid move')
        else:
            row += 1
            return(row,col)
    elif direction == 'd':
        if  col == len(maze[0])-1 or maze[row][col+1] == 1:
            print('invalid move')
        else:
            col += 1
            
            return(row,col)
    elif direction == 'a':
        if col == 0 or maze[row][col-1] == 1:
            print('invalid move')
        else:
            col -= 1
            
            return(row,col)
    elif direction == 'give up':
        shortest_path = find_shortest_path(maze,row,col,end_row,end_col) #get the path taken to end
        shortest_print(shortest_path) #print out the maze and path taken
    else:
        print('Invalid move. Options are up/left/down/right (w/a/s/d) or give up:')
    
    return(row,col)
def tutorial():
    print('first, enter your dimensions. In this example, we will use 5 and 5')
    print('rows: 5')
    print('columns: 5')
    print('then, start typing the first row of the maze. "1" is a wall, "0" is a path, "2" is your start and "3" is your end')
    print('enter row1: 10310')
    print('then start typing the next')
    print('enter row2: 00101')
    print('enter row3: 01001')
    print('enter row4: 20011')
    print('enter row5: 10111')
    print("that's all! enjoy your maze!")
def find_shortest_path(maze,r,c,er,ec):
    end = (er,ec)
    to_do_list = [(r,c)]
    visited = {(r,c):True} #prevent re-iterations
    vectors = [(-1,0),(1,0),(0,-1),(0,1)]
    paths = {(r,c):[(r,c)]} #keep track of paths
    while True:
        if len(to_do_list) == 0:
            break
        current = to_do_list.pop(0)
        current_row, current_column = current
        if current == end:
            break
        for dx,dy in vectors:
            new_row = dx + current_row
            new_col = dy + current_column
            #find valid neighbors
            if new_row >= 0 and new_col >= 0 and new_row < len(maze) and new_col < len(maze[0]) and maze[new_row][new_col] != 1:
                if (new_row,new_col) not in visited:
                    to_do_list.append((new_row,new_col))
                    visited[(new_row,new_col)] = True
                    paths[(new_row,new_col)] = paths[current] + [(new_row,new_col)]
    #get the shortest path
    return paths[end]
def shortest_print(path):
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            if (x,y) in path:
                print('P', end = ' ') #print path to end
            elif maze[x][y] == 1:
                print('#', end = ' ') #print walls
            elif maze[x][y] == 2:
                print('S', end = ' ') #print start
            elif maze[x][y] == 3:
                print('E', end = ' ') #print end
            else:
                print('.', end = ' ') #print path
        print()
    
while True:
    while True:
        mode = input('do you want to play easy, medium, hard or make a custom maze?(e/m/h/c):')
        if mode.lower() == 'm':
            maze = medium_maze
            pos_row = 3
            pos_col = 1
            end_row = 0
            end_col = 14
            break
        elif mode.lower() == 'e':
            maze = easy_maze
            pos_row = 4
            pos_col = 1
            end_row = 3
            end_col = 4
            break
        elif mode.lower() == 'h':
            maze = hard_maze
            pos_row = 3
            pos_col = 1
            end_row = 0
            end_col = 14
            break
        elif mode.lower() == 'c':
            tut = input('do you want to look at a tutorial?(y/n) ')
            if tut.lower() == 'y':
                tutorial()
            maze = []
            rows = int(input('rows: '))
            cols = int(input('cols: '))
            for x in range(rows):
                a = list(input('enter row'+str(x+1)+':'))
                for y in range(cols):
                    a[y] = int(a[y])
                    if a[y] == 2:
                        pos_row = x
                        pos_col = y
                    elif a[y] == 3:
                        end_row = x
                        end_col = y
                maze.append(a)
            break                
        print('not an option')
    printmaze(maze,pos_row,pos_col)
    while [pos_row,pos_col] != [end_row,end_col]:
        d = input('which direction(w/a/s/d) or give up: ')
        pos_row, pos_col = move(d, pos_row, pos_col, maze, end_row, end_col)
        if d == 'give up':
            break
        printmaze(maze, pos_row, pos_col)
    if d != 'give up':
        print('you won!')
    else:
        print('better luck next time')
    play_again = input('play again? (y/n)')
    if play_again == 'n':
        break
print('thanks for playing')