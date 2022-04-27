import csv
import os

# <--- Start of the game, returns the number of columns --->
def start():
    print ('Welcome to Connect 4! ')
    print("\nThe objective of the game is to try to build a row of four pieces (horizontally, vertically or diagonally) \n\t\twhile keeping your opponent from doing the same!")
    print("\nScoring system: Each player gets a point for every winning piece and every neighboring piece of theirs")
    print("\nThe game ends when the board is full and the player with the most points wins the game!")
    print("\nChoose which player goes first and have fun!")
    input("\nPress any key to start the game")
    os.system('cls')

    an1 = input('Would you like to start a new game (N) or continue with a saved board (S)? ')
    while (an1!= 'N' and an1!= 'S'):		                                                    
        an1 = input('Would you like to start a new game (N) or continue with a saved board (S)? ')

    if (an1 == 'N'):    #New game
        while True:							                                                    
            try:
                columns = int(input('Give number of columns (5-10): '))
            except ValueError:
                print('Invalid input!')
            else:
                break

        while (columns<5 or columns>10):
            print('Must be between 5-10!')				                                                
            while True:							                                                    
                try:
                    columns = int(input('Give number of columns (5-10): '))
                except ValueError:
                    print('Invalid input!')
                else:
                    break

        create_new_board(columns)       #Creates new board
        return columns
    
    #Retrieves saved game
    saved_board = read_csv()
    return saved_board


# <--- Creates a new board with the requested number of columns --->
def create_new_board(columns):
    for x in range(columns):        #Creates an empty board
        board.append([])
        for k in range(columns):
            board[x].append(' ')

    for i in range(columns):        #Creates a list with the top indicator for each column (Starts at the number of requested columns)
        top.append(columns)


# <--- Prints the board, with row letters and column numbers --->
def print_board():
    for x in range(columns):        #Prints column numbers
        print ('   ', x+1, end=' ')
    print ("\n", columns*6*"-")
   
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']         
    for x in range(columns):        #Prints row with letters and seperators
        
        print (letters[x], '|', end='')
        for i in range(columns):
            print (' ', board[i][x], ' |', end='')

        if (x != columns-1):
            print('\n')

    print ('\n', columns*6*"-")
    print ('\n\n')


# <--- Pushes piece on the column the player chose --->
def push(p, player):
    top[p] -= 1           

    if (player == 1):                                                            
        board[p][top[p]] = 'O'
        check_four(player)
    else: 
        board[p][top[p]] = 'X'
        check_four(player)
    

# <--- Checks if the player that just placed a piece has a win --->
def check_four(player):
    global wins

    n = columns-1
    if (player == 1):
        piece = 'O'
    else:
        piece = 'X'


    con=True
    while (con == True):        #A condition is used to check if after the rotation of the pieces the player has a new win
        wins = []
        
        #Checks horizontal
        found4 = False
        for i in range(columns):
            for j in range(n-2):
                if (board[j][i]==piece and board[j+1][i]==piece and board[j+2][i]==piece and board[j+3][i]==piece and found4==False):       #Found a win
                    for x in range(j,j+4):      #Saves the coords of the win and the piece of the player in the list wins
                        if ((x,i) not in wins):
                            wins.append((x, i))

                    if (j-1 >= 0):      #Checks if neighboring pieces are also the same
                        extra_four(j-1, i, piece)
                    if (j+4 <= n):
                        extra_four(j+4, i, piece)

                    found4 = True       #Used so it doesn't count a new win with the neighboring pieces
    

        #Checks vertical
        found4 = False
        for j in range(columns):
            for i in range(n-2):
                if (board[j][i]==piece and board[j][i+1]==piece and board[j][i+2]==piece and board[j][i+3]==piece and found4==False):       #Found a win
                    for x in range(i,i+4):      #Saves the coords of the win and the piece of the player in the list wins
                        if  ((j,x) not in wins):
                            wins.append((j, x))    

                    if (i-1 >= 0):      #Checks if neighboring pieces are also the same
                        extra_four(j, i-1, piece)
                    if (i+4 <= n): 
                        extra_four(j, i+4, piece)

                    found4 = True       #Used so it doesn't count a new win with the neighboring pieces
    
 
        #Checks \
        found4 = False
        for i in range(n-2):
            for j in range(n-2):
                if (board[j][i]==piece and board[j+1][i+1]==piece and board[j+2][i+2]==piece and board[j+3][i+3]==piece and found4==False):     #Found a win
                    for x in range(4):      #Saves the coords of the win and the piece of the player in the list wins
                        if ((j+x,i+x) not in wins):
                            wins.append((j+x, i+x))

                    if (j-1>=0 and i-1>=0):     #Checks if neighboring pieces are also the same
                        extra_four(j-1, i-1, piece)
                    if (j+4<=n and i+4<=n): 
                        extra_four(j+4, i+4, piece)

                    found4 = True       #Used so it doesn't count a new win with the neighboring pieces
              
                   
        #Checks /
        found4 = False
        for i in range(n,n-2,-1):
            for j in range(n-2):
                if (board[j][i]==piece and board[j+1][i-1]==piece and board[j+2][i-2]==piece and board[j+3][i-3]==piece and found4==False):     #Found a win
                    for x in range(4):      #Saves the coords of the win and the piece of the player in the list wins
                        if ((j+x,i-x) not in wins):
                            wins.append((j+x, i-x))

                    if (j-1>=0 and i+1<=n):     #Checks if neighboring pieces are also the same
                        extra_four(j-1, i+1, piece)
                    if (j+4<=n and i-4>=0):   
                        extra_four(j+4, i-4, piece)

                    found4 = True       #Used so it doesn't count a new win with the neighboring pieces
        
        con = count_wins(player)
        
    
# <--- Checks if a player has any wins. Changes the score accordingly (each piece = 1 point) --->
def count_wins(player):
    global wins
    global points1
    global points2

    if (len(wins)>0):       #If there are any wins
            
            print_board()
            for cords in wins:
                board[cords[0]][cords[1]] = '*'

            if (player == 1):       #Changes scores
                points1 += len(wins)
            else:
                points2 += len(wins)

            #Checks how many wins were found and prints winning message
            if (len(wins)>=4 and len(wins)<8):      #1 win was found
                print('Player', player, 'got a win!')
            elif (len(wins) >= 8):       #Multiple wins were found
                print('Player', player, 'got multiple wins!')
            print_board()

            pop_items()     #Removes the * and moves the rest of the board

            return True
    #There were no additional wins after the pop so the loop ends
    return False



# <--- Checks if neighboring pieces are the same --->              
def extra_four(x,y,piece):
    global wins
    
    if (board[x][y] == piece):
        wins.append((x, y)) 


# <--- Removes the winning pieces and moves the rest of the board --->    
def pop_items():
    for j in range(columns):
        for i in range(columns-1, -1, -1):
            if (board[j][i] == '*'):
                while (board[j][i] == '*'):
                    board[j].pop(i)
                    board[j].insert(0, ' ')
                    top[j] += 1


# <--- Creates the CSV file when the player requests to save progress --->    
def create_csv():
    data = []
    for i in range(columns):        #Turns the board to zeros, ones and twos that saves to the file
        data.append([])
        for j in range(columns):
            if (board[j][i] == ' '):
                data[i].append(0)
            elif (board[j][i] == 'O'):
                data[i].append(1)
            else:
                data[i].append(2)
    score = [points1, points2]

    filename = input('Give file name: ')
    with open(filename, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)
        csvwriter.writerow(score)

    print('Progress saved!')



# <--- Creates the board from a given CSV file --->  
def read_csv():
    global points1
    global points2

    ans = input('Give file name: ')
    data = []
    score = []

    while True:
        try:
            file = open(ans)
        except FileNotFoundError:
            print('File not found!')
            ans = input('Give file name: ')
        else:
            break
                     
    csvreader = csv.reader(file)
    for row in csvreader:       #Saves CSV lines to list data
        data.append(row)
    file.close()

    score = data.pop(-1)        #Saves the last line of the CSV file to a different list
    rows = len(data)        #Calculates the columns of the saved board

    points1 = int(score[0])
    points2 = int(score[1])

    for i in range(rows):       #Creates the saved board (turns the zeros, ones and twos to ' ','O','X')
        board.append([])
        for j in range(rows):
            if (int(data[j][i]) == 0):
                board[i].append(' ')
            elif (int(data[j][i]) == 1):
                board[i].append('O')
            else:
                board[i].append('X')
    
    for j in range(rows):       #Calculates the top of each column
        top.append(0)
        while (board[j][top[j]]==' ' and top[j]<rows-1):
            top[j] += 1
        if (board[j][top[j]] == ' '):
            top[j] += 1
    return rows


 
if __name__ == "__main__":
    board = []
    top = []
    points1 = 0
    points2 = 0

    columns = start()
    print_board()

    an3 = ' '
    while (an3!='s' and sum(top)>0):
        player = 1

        while True:
            try:
                p1 = (int(input('Player 1: Choose a column to place your piece (\'O\'): ')) -1) 
            except ValueError:
                print('Invalid input!')
            else:
                break
        
        while (p1<0 or p1>columns-1 or top[p1]<=0):
            print('Must be between 1 and', columns, 'and not full!')				                                        
            while True:
                try:
                    p1 = (int(input('Player 1: Choose a column to place your piece (\'O\'): ')) -1) 
                except ValueError:
                    print('Invalid input!')
                else:
                    break
        
        push(p1, player)
        print_board()
       
        if (sum(top)>0):        #Checks if the board is full
            player = 2
            
            while True:
                try:
                    p2 = (int(input('Player 2: Choose a column to place your piece (\'X\'): ')) -1) 
                except ValueError:
                    print('Invalid input!')
                else:
                    break 
            
            while (p2<0 or p2>columns-1 or top[p2]<=0):
                print('Must be between 1 and', columns, 'and not full!')				                                    
                while True:
                    try:
                        p2 = (int(input('Player 2: Choose a column to place your piece (\'X\'): ')) -1) 
                    except ValueError:
                        print('Invalid input!')
                    else:
                        break 

            push(p2, player)
            print_board()
            print('\n')
        else:
            break       #The board is full, the game ends

    
        if (sum(top) > 0):      #Checks if the board is full
            print('Player 1:', points1)
            print('Player 2:', points2)
            print('\n')
            an3 = input('Press any key to continue\nTo pause the game and save progress press "s":')
        else:       #The board is full, the game ends
            break 
    
    if (an3 == 's'):
        create_csv()
    else:
        print('The game is over!')
        print('Player 1:', points1)
        print('Player 2:', points2)
