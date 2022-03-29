NUM_ROWS = 6
NUM_COLS = 7
WINNING_ROW_SIZE = 4

# Class representing the game board
class Board():
    def __init__(self, rows: int = NUM_ROWS, cols: int = NUM_COLS, winning_row_size: int = WINNING_ROW_SIZE) -> None:
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.winning_row_size = winning_row_size
        # List used to quickly retrieve the next open row in each column, initialized to bottom of board
        self.open_rows = [rows-1]*cols
        # Variable used to represent the current turn
        self.turn = 1
    
    # Function to display the board
    def display_board(self) -> None:
        # Display the column numbers
        print("\n")
        for col in range(self.cols):
            print(f" ({col})", end="")
        print("\n")    

        # Display board slots
        for row in range(self.rows):
            print('|', end="")
            for col in range(self.cols):
                print(f" {self.board[row][col]} |", end="")
            print("\n")
    
    # Helper function that returns the player whose turn it is 
    def get_player(self) -> int:
        return 1 if self.turn % 2 == 1 else 2

    # Helper function that determines whether an adjacent slot is within the bounds of the board
    def valid_slot(self, row: int, col: int) -> bool:
        return (0 <= row < self.rows and 0 <= col < self.cols)

    # Function that drops a piece into the selected column of the board in the next empty row
    def drop_piece(self, col: int) -> bool:
        # Get the next empty row of the given column
        row = self.open_rows[col]
        # Drop a piece in the given column if there are still empty slots
        if row >= 0:
            self.board[row][col] = self.get_player()
            # Set the next open row for the given column to the row above
            self.open_rows[col] -= 1
            # Switch turns
            self.turn += 1
            # Check if the player won after they dropped a piece
            return self.check_win(row, col)
        # If the column is full, let the player know
        else:
            print("Column full! Please select another column")
            return False

    # Function that checks to see if there is a winner
    def check_win(self, row: int, col: int) -> bool:
        # Identify the player that dropped the last piece
        player = self.board[row][col]
        # Test all 8 outward directions from the last dropped piece
        # Each subset contains the following two values:
        # - Direction to move
        # - Amount of matching pieces found in that direction
        directions = [
            # Vertical row
            [(1,0), 0],
            [(-1,0), 0],
            # Horizontal row
            [(0,1), 0],
            [(0,-1), 0],
            # Positive slope diagonal
            [(1,1), 0],
            [(-1,-1), 0],
            # Negative slope diagonal
            [(1,-1), 0],
            [(-1,1), 0]
        ]

        # Search each direction
        for direction in directions:
            x, y = direction[0]
            # The maximum distance from the origin we will search for each direction is the winning row size - 1 (e.g. 4 - 1 = 3)
            for dist_from_origin in range(self.winning_row_size-1):
                
                # Get the next adjacent slot in the current direction
                next_row = row + (x * (dist_from_origin+1))
                next_col = col + (y * (dist_from_origin+1))
                
                # Stop searching the current direction if any of the following are true for the next adjacent coordinate: 
                # - Is outside the bounds of the board
                # - Is an empty slot
                # - Contains a non-matching piece
                if not self.valid_slot(next_row, next_col) or self.board[next_row][next_col] != player:
                    break
                
                # Increment the number of matching pieces for the current direction if a matching piece is found
                direction[1] += 1
        
        # Search through the direction pairs (i.e. vertical row, horizontal row, and diagonals) to determine whether the player has won
        for i in range(0, len(directions)-1, 2):
            
            # A player has won if the matching pieces in the direction pair is greater than or equal to the winning row size - 1
            if directions[i][1] + directions[i+1][1] >= self.winning_row_size-1:
                # Show the status of the board and notify the players of the winner
                self.display_board()
                print(f"Player {player} wins!")
                return True

        return False

        

# Game loop
def play_game() -> None:
    # Create a game board
    game_board = Board()
    game_over = False
    
    # Loop until a player has won or there is a draw
    while not game_over:
        # Display the status of the board with every turn
        game_board.display_board()
        
        # Prompt the user for input
        try:
            col = int(input(f"Player {game_board.get_player()} - select a column (0-{game_board.cols - 1}): "))
        
        # If user input isn't an integer, re-prompt input
        except:
            print(f"Invalid input! Select a number between 0 and {game_board.cols - 1}")
            continue

        # If the user selected a column outside the bounds of the board, re-prompt input
        if col >= game_board.cols or col < 0:
            print(f"Invalid column! Select a number between 0 and {game_board.cols - 1}")
        
        # Drop a piece for the current player in the selected column if they selected a column within the bounds of the board
        else:
            # End the game if a winner is found after the piece is dropped
            game_over = game_board.drop_piece(col)
        
        # End the game if there are no more empty slots and a winner hasn't been found
        if not any(' ' in slot for slot in game_board.board):
            # Show the status of the board and notify the players that the game ended in a draw
            game_board.display_board()
            print("Draw! Neither player wins")
            return

if __name__ == '__main__':
    play_game()