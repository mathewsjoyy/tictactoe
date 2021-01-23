import random   # Import random module to use for computer random move

# The following function print the current board to the command window.
def print_board(board):
    print("\n")
    print(" |", board[0], "|", board[1], "|", board[2], " |     1 | 2 | 3")
    print(" |", "--+---+---", "|")
    print(" |", board[3], "|", board[4], "|", board[5], " |     4 | 5 | 6")
    print(" |", "--+---+---", "|")
    print(" |", board[6], "|", board[7], "|", board[8], " |     7 | 8 | 9")

# This function takes the existing board, position input from player,
# marker type (either x or o) and returns the updated board based on the arguments.
def update_board(board, position, marker):
    board[position-1] = marker
    print_board(board)
    return board

# Add any other functions below for your program

# Function to allow the user to select the game mode they wish to play either,
# Player vs Player (PvP) or Player vs Computer (PvC).
def game_selection():
    while True:
        game_mode = input("""\nSelect what game mode you want to play.
- Player Vs Player Type 'PvP'
- Player vs Computer Type 'PvC'
Type your desired game mode here: """)
        if game_mode in ('PvP', 'pvp', 'PVP'):
            return p_v_p()    # Calls function for Player vs Player
        elif game_mode in ('PvC', 'pvc', 'PVP'):
            return p_v_c()    # Calls function for Player vs Computer
        else:
            print("\n-- INVALID GAME MODE Type 'PvP' or 'PvC' --")

# This function is called whenever the initial game ends,and give the user the
# option to play another game or to exit out the console.
def play_again():
    while True:
        play_another = input("\nThank you for playing! \
Would you like to play again (Type 'yes') or press any key to exit!: ").lower()
        if not play_another == "yes":
            exit(0)
        return None

# Define a class for Player
class Player:
    # Player class has values for there counter (X/O),and if they have won (True/False)
    def __init__(self, counter):
        self.has_won = False
        self.counter = counter

    # Method to allow player objects to move and select a unoccupied position on the board,
    # from 1-9,along with error checking/validation of there input e.g.input is a integer.
    def move(self):
        while True:
            try:
                player_input = int(input(f"\nWhere do you want to place your {self.counter}?(1-9): "))
            except ValueError:
                print("\nInvalid Input not an number,Try Again.")
                continue
            if player_input in range(1, 10) and board[player_input - 1] == " ":
                update_board(board, player_input, self.counter)
                return self.game_state(self.counter)
            else:
                print("\nPlease enter a position between 1-9 ,which is also empty.")

    # Method which allows the board to be reset back to empty, and to reset the has_won
    # value back to 'False'. So the user can choose to play a fresh match.
    def reset(self):
        global board
        board = [" " for move in range(9)]
        self.has_won = False

    # This method allows any player to move an existing counter to any location on the board
    def move_exisiting_piece(self):
        if self.counter not in board:    # Check if the player has a counter on the board
            return None

        while True:    # Ask user if they want to move an exisiting piece or not
            answer = input("\nDo you want to move an existing piece (yes/no): ").lower()
            if answer == "yes":
                break
            if answer == "no":
                return None

        while True:    # Loop which asks user to choose the counter they want to move
            try:
                location = int(input("\nWhat's the location of the your counter"
                                     " you want to move (1-9): "))
            except ValueError:
                print("\nYou did not enter a valid location on the board!")
            if location in range(1, 10) and board[location - 1] == self.counter:
                board[location - 1] = " "
                while True:    # Loop to ask user where to move the exisiting counter
                    try:
                        move_location = int(input("\nWhere on the board is the new location"
                                                  " you want to place the piece? (1-9): "))
                    except ValueError:
                        print("\nNot a valid location,Try Again.")
                    if move_location in range(1, 10) and board[move_location - 1] == " ":
                        update_board(board, move_location, self.counter)
                        return self.game_state(self.counter)
                    else:
                        print("\nThis location is not avaliable to place your piece.")
            else:
                print(f"\nYou do not have a {self.counter} in this location! Try Again.")

    # This method is used to check the game state after every indivdual move to check if
    # the game is a draw, a win or to continue playing.
    def game_state(self, counter):
        horizontal_win = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        vertical_win = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        diagnol_win = [[1, 5, 9], [3, 5, 7]]

        for x, y, z in horizontal_win:  # Uses a for loop to check for horizontal win
            if board[x-1] == board[y-1] == board[z-1] != " ":
                print("\nPlayer with counter " + board[x-1] + " has won!")
                self.has_won = True
                return 1

        for x, y, z in vertical_win:    # Uses a for loop to check for vertical win
            if board[x-1] == board[y-1] == board[z-1] != " ":
                print("\nPlayer with counter " + board[x-1] + " has won!")
                self.has_won = True
                return 1

        for x, y, z in diagnol_win:     # Uses a for loop to check for diagnol win
            if board[x-1] == board[y-1] == board[z-1] != " ":
                print("\nPlayer with counter " + board[x-1] + " has won!")
                self.has_won = True
                return 1

        # Use a for loop to check if board is full and there is no winner (draw)
        if len([c for c in board if c in ('X', 'O')]) == 9:
            print("\nTHIS GAME IS A DRAW! NOBODY WINS!")
            self.has_won = True
            return 1
        return 0    # Return 0 if no win/draw is found 

# Class for the computer, which inherited values and methods from the Player class
class Computer(Player):
    def __init__(self, counter):
        Player.__init__(self, counter)

    # Method to allow computer to select the optimal position to place a counter
    def cpu_move(self):
        # Create a 2D array of all possible combinations to play
        winning_combos = [[0, 1, 2], [0, 2, 1], [2, 1, 0], [3, 4, 5],
                          [3, 5, 4], [4, 5, 3], [6, 7, 8], [6, 8, 7],
                          [7, 8, 6], [0, 3, 6], [0, 6, 3], [3, 6, 0],
                          [1, 4, 7], [1, 7, 4], [4, 7, 1], [2, 5, 8],
                          [2, 8, 5], [5, 8, 2], [0, 4, 8], [0, 8, 4],
                          [8, 4, 0], [2, 4, 6], [2, 6, 4], [6, 4, 2]]

        # For each value in each sub array of win_combos we check for a winning position
        # for the computer.If there is none then we check if the human player has a winning turn
        # next, if so we place a 'O' in that position
        for x, y, z in winning_combos:
            if board[4] == " ":
                print("The Computer has placed a 'O' in position 5")
                update_board(board, 5, self.counter)
                return self.game_state(self.counter)
            elif board[x] == "O" and board[y] == "O" and board[z] == " ":
                print("The computer has placed a 'O' in position " + str(z+1))
                update_board(board, z+1, self.counter)
                return self.game_state(self.counter)
            elif board[x] == "X" and board[y] == "X" and board[z] == " ":
                print("The computer has placed a 'O' in position " + str(z+1))
                update_board(board, z+1, self.counter)
                return self.game_state(self.counter)

        # If non of the operations above work then get the computer to select a random
        # position on the board to place a 'O'.
        while True:
            move = random.randint(1, 9)
            if board[move-1] == " ":
                print("The computer has placed a 'O' in position " + str(move))
                update_board(board, move, self.counter)
                return self.game_state(self.counter)

# This function is called to play the player vs player game mode and uses a while
# loop to keep switching players, and checking for a win / draw.
def p_v_p():
    print("\nWelcome to Player vs Player Game Mode ", end="")
    print("PLAYER 1 you're COUNTER 'X', PLAYER 2 you're COUNTER 'O'!")

    while True:
        print("\n -PLAYER ONE'S TURN (X)-")
        if player1.move_exisiting_piece() is None:
            player1.move()
        if player1.has_won:    # If player 1 has won, reset the board and has_won values
            player1.reset()
            player2.reset()
            return None

        print("\n -PLAYER TWO'S TURN (O)-")
        if player2.move_exisiting_piece() is None:
            player2.move()
        if player2.has_won:    # If player 2 has won, reset the board and has_won values
            player1.reset()
            player2.reset()
            return None

# This function is called to play the player vs computer game mode and uses a while,
# loop to keep switching players, and checking for a win / draw.
def p_v_c():
    print("\nWELCOME TO PLAYER VS COMPUTER! \nHUMAN PLAYER you're PLAYER 1", end="")
    print(" and COUNTER 'X', The COMPUTER is PLAYER 2 and COUNTER 'O'")

    while True:
        print("\n -PLAYER ONE'S TURN (X)-")
        if player1.move_exisiting_piece() is None:
            player1.move()
        if player1.has_won:    # If player 1 has won, reset the board and has_won values
            player1.reset()
            computer.reset()
            return None

        print("\nThe computer is selecting where to place the next 'O'...")
        computer.cpu_move()
        if computer.has_won:   # If the computer has won, reset the board and has_won values
            player1.reset()
            computer.reset()
            return None

# Program main starts from here

# Global variable for the board
board = [" " for move in range(9)]

# Define the objects for Player vs Player game mode
player1 = Player("X")
player2 = Player("O")

# Define objects for Player vs Computer gamemode
computer = Computer("O")

# If this is the main file execute the Tic Tac Toe Game
if __name__ == "__main__":
    while True:    # Run a loop to let user select game mode / play again
        game_selection()
        play_again()
