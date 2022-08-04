import random
import math
import re

from sqlalchemy import null

# Create an board object to represent the minesweeper game
class Board:
    def __init__(self, dimmSize, numBombs):
        # Keep track of these parameters (board size and number of bombs)
        self.dimSize = dimmSize
        self.numBombs = numBombs

        # Creation of the board
        # makeNewBoard() is an helper function which will create the board and plant the bombs into the board
        self.board = self.makeNewBoard()
        # assignValueToBoard() is an helper function which will assign the number to determine how many bombs are around the area
        self.assignValueToBoard()

        # Initalize a set to keep track of which locations we've uncovered
        # Something like (row, col) tuples into this set
        # So if we dig at 0,0 then self.dug = {(0,0)}
        self.dug = set()
    
    def makeNewBoard(self):
        # Construct a new board based on the dimension size and number of bombs that the player has set or with the default value

        # Generate a new board
        board = [[None for _ in range(self.dimSize)] for _ in range(self.dimSize)]
        # In a nutshell create an array that look like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [..., ..., ..., ...],
        #  [None, None, ..., None],
        # A board filled with board with none

        # Plant the bomb onto the board
        bombPlanted = 0
        while bombPlanted < self.numBombs:
            loc = random.randint(0, self.dimSize**2 -1)
            # We want the number of times dimSize goes into loc to tell us the row index
            row = loc // self.dimSize
            # We want the remainder to tell us what index in that row to look for the column index
            col = loc % self.dimSize 

            # We will use * to represent the bomb while None as a "normal space"
            if board[row][col] == '*':
                # This means we've actually planted a bomb there already so keep going
                continue

            # Bomb planted onto the board              
            board[row][col] = '*'
            bombPlanted += 1
        return board

    def assignValueToBoard(self):
        # With the bombs planted onto the board, we can assign a number 0-8 for all the empty spaces to represent how many neighboring bombs there are.
        for r in range(self.dimSize):
            for c in range(self.dimSize):
                if self.board[r][c] == '*':
                    # If the square is already an bomb, we dont want to calculate anything
                    continue
                self.board[r][c] = self.getNumNeighboringBombs(r, c)

    def getNumNeighboringBombs(self, row, col):
        # Iterate through each of the neighboring positions and sum number of bombs
        # Top left: (row-1, col-1)
        # Top mid: (row-1, col)
        # Top right: (row-1, col+1)
        # Left: (row, col-1)
        # Right: (row, col+1)
        # Bottom left: (row+1, col-1)
        # Bottom  mid: (row+1, col)
        # Bottom  right: (row+1, col+1)

        # Making sure we dont go out of bound
        numNeighboringBombs = 0

        # For each row, we are checking above and below
        # For the lower bound (max(0, row-1), we are setting it with the highest value so if we were at 0,0 it would not set the index to -1 since it would be out of bound
        # For the upper bound min(self.dimSize-1, row+1)+1), that is the biggest index we can go
        for r in range(max(0, row-1), min(self.dimSize-1, row+1)+1):
            # For each column we are checking the left and the right side
            for c in range(max(0,col-1), min(self.dimSize-1, col+1)+1):
                if r == row and c == col:
                    # Original location, dont check
                    continue
                if self.board[r][c] == '*':
                    numNeighboringBombs += 1
        return numNeighboringBombs

    
    def dig(self, row, col):
        # Dig at the location given
        # Return true if its an successful dig, false if a bomb were dug

        # Scenarios for the dig function:
        # S1: Hit a bomb -> game over and return false
        # S2: Dig at location with neighboring bombs -> finish dig and return true
        # S3: Dig at location with no neighboring bombs -> recursively dig neighbors

        # Keep track of where we dug
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # Where self.board[row][col] == 0 -> S3
        for r in range(max(0, row-1), min(self.dimSize-1, row+1)+1):
            for c in range(max(0,col-1), min(self.dimSize-1, col+1)+1):
                # If this place has already been dug, then continue
                if(r, c) in self.dug:
                    continue
                self.dig(r, c)
        # If our initial dig didnt't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # This is a magic function where if you call print on this object
        # it'll print out what this function returns!
        # Return a string that shows the board to the player

        # Create a new array that represents what the user would see
        visibleBoard = [[None for _ in range(self.dimSize)] for _ in range(self.dimSize)]
        for row in range(self.dimSize):
            for col in range(self.dimSize):
                if (row, col) in self.dug:
                    visibleBoard[row][col] = str(self.board[row][col])
                else:
                    visibleBoard[row][col] = ' '

        # put this together in a string
        string_rep = ''

        # Get max column widths for printing
        widths = []
        for idx in range(self.dimSize):
            columns = map(lambda x: x[idx], visibleBoard)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # Print the csv strings
        indices = [i for i in range(self.dimSize)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visibleBoard)):
            row = visibleBoard[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dimSize)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


# Function to play the game, default board size is 10 by 10 with 10 bombs
def play(dimSize = 10, numBombs = 10):
    # Step 1: Create the board and plant the bombs
    board = Board(dimSize, numBombs)

    # Step 2: Show the user the board and ask for where they want to dig


    # Step 3a: If location is a bomb, show game over message
    # Step 3b: If location is not a bomb, dig recursively until each square is at least next to a bomb
    # Step 4: Repeat step 2 and 3a/b until there are no more places to dig which results in an victory
    safe = True
    while len(board.dug) < board.dimSize ** 2 - numBombs:
        print(board)
        # Regex basically split the string with , and matches it with either 0,0 or 0, 0 or 0, .... 0 
        userInput = re.split(',(\\s)*', input('Where would you like to dig? Input as row, col: '))
        row, col = int(userInput[0]), int(userInput[-1])
        if row < 0 or row >= board.dimSize or col < 0 or col >= dimSize:
            print("Invalid location. Try again.")
            continue

        # If its an valid spot, we dig
        safe = board.dig(row, col)
        if not safe:
            # Dug a bomb so game over
            print("Sorry Game over: ")
            # Reveal the whole board
            board.dug = [(r,c) for r in range(board.dimSize) for c in range(board.dimSize)]
            print(board)
            break

    if safe:
        print("Congratulations! You have won!")

if __name__ == '__main__':
    # Data sanitization (Limit user inputting numbers only)
    while True:
        try:
            # Create a board size that the user has specified. Maximum a 10 by 10 
            boardsize = input("Enter a boardsize: ")
            # Create mines. The quantity of mines are <= boardsize^2
            bombQuantity = input("Enter the number of bombs: ")

            # User has not specified the board size or the bomb quantity therefore default values were used
            if(len(boardsize) == 0 and len(bombQuantity) == 0):
                play()
            # User has only specified the quantity of mines
            elif(len(boardsize) == 0 and len(bombQuantity) != 0):
                # If specified quantity of mines exceed the board size default values are used
                if(int(bombQuantity) > int(boardsize)):
                    play(10, 10)
                play(10, int(bombQuantity))
            # User has only specified the board size
            elif(len(boardsize) != 0 and len(bombQuantity) == 0):
                # If specified board size is greater than 10 by 10 then default values are used
                if(int(boardsize) > 10):
                    play(10, 10)
                play(int(boardsize), 10)
            # User has only both the board size and quanity of mines
            else:
                # If specified quantity of mines exceed the board size, half the board is filled with mines (custom board if user has entered in two valid input)
                if(int(bombQuantity) > int(boardsize)):
                    play(int(boardsize), math.floor(int(pow(int(boardsize), 2)/2)))
                play(int(boardsize), int(bombQuantity))
            break
        except:
            print("Please enter a valid integer for either the board size or quantity of mines!")

