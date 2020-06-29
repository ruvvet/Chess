# Python Practice
# Creating a Chess Game w/ Python
# Using Lists, Dict, + other basic Python concepts


# Creating the Chess board.
# The chess board is made up of nested lists for 8x8 cells
# 8 lists for each row, these represent the 1-8 values on the board.
# 8 elements in each row (the columns), represent the A-H values on the board.
# Lists:
# ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# [
#  '0',
#  '1',
#  '2',
#  '3',
#  '4',
# ]
board = [
    ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
    ['♟︎', '♟︎', '♟︎', '♟︎', '♟︎', '♟︎', '♟︎', '♟︎'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
    ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
]

# Cheat board
# board = [
#     ['♜', '', '♝', '♛', '♚', '♝', '♞', '♜'],
#     ['♟︎', '♟︎', '♟︎', '', '♖', '♙', '', '♟︎'],
#     ['', '', '', '', '', '', '', ''],
#     ['', '', '', '', '', '♟︎', '', ''],
#     ['', '', '', '', '♙', '', '', ''],
#     ['', '', '', '', '', '', '', ''],
#     ['♙', '♙', '♙', '', '♙', '♙', '♙', '♙'],
#     ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
# ]

# Defining the chess board pieces.
# Dictionary where each piece is the key.
# And the values associated with each key are the 'Type' and 'Color'.
pieces = {
    '♜': ['rook', 'b'],
    '♞': ['knight', 'b'],
    '♝': ['bishop', 'b'],
    '♛': ['king', 'b'],
    '♚': ['queen', 'b'],
    '♟︎': ['pawn', 'b'],
    '♖': ['rook', 'w'],
    '♘': ['knight', 'w'],
    '♗': ['bishop', 'w'],
    '♕': ['king', 'w'],
    '♔': ['queen', 'w'],
    '♙': ['pawn', 'w']
}

# Text return strings go here.
SELECT_PIECE_STRING = 'Select a piece to move (A2): '
ERROR_INVALID_PIECE = 'Please select a valid piece'
ERROR_INVALID_LOC = 'Invalid location'
INPUT_LOC = 'Input a location: '
PROMO_STRING = 'Promote pawn to (Queen): '
ERROR_INVALID_PROMO = 'Invalid Promo. '

# Printing column + row headers + prettifying
column_headers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
column_spacing = ' '
row_headers = [8, 7, 6, 5, 4, 3, 2, 1]
row_spacing = '  '


# Main function.
def main():
    # Define player. White always starts in chess.
    # Swap players below after the move has validated.
    current_player = 'w'

    # Print intro
    print('--------LIFE IS A GAME OF CHESS--------')
    print()

    # Captured pieces.
    # Captured pieces are appended to these lists.
    captured_b = []
    captured_w = []

    # Initialize winner as false
    winner = False

    # While no winner exists, life goes on.
    # This occurs each round there is no winner.
    while not winner:
        # Call print board function.
        # Print the board state.
        # Print which player's turn it is.
        # Print the captured pieces.
        print()
        print_board(board)
        print()
        print('>>> ', current_player.upper(), 'Player Turn', '\n'
                'Captured Pieces: ', '\n'
                'W:', ' , '.join(captured_w), '\n'
                'B:', ' , '.join(captured_b))

        # Call the player input function.
        # Pass arguments: the current player + the captured pieces.
        # Current_player used to reference which moves are valid
        # Captured pieces used append to the list
        player_move(current_player, captured_b, captured_w)

        # Swap current player between white and black 
        # each time we complete a valid round.
        current_player = 'w' if current_player == 'b' else 'b'

        # Check for winner each round
        # If king is in either list, king is captured
        # Game ends
        if '♚' in captured_b or '♔' in captured_w:
            winner = True
            print()
            print('!!! and MATE \n'
                'Player', current_player, 'is the winner!')
            print ('GG')
        else:
            winner = False

    return current_player, winner


# Print board function that prints the board state after each turn
# Passes the nested board list + prettifies before printing.
def print_board(board):
    # Output the board to the console (showing it as a grid)
    # Print all column headers + for each element add spacing to center
    print(column_spacing + row_spacing + '    '.join(column_headers) + '\n')

    # Enumerate: returns the index + the element at that index as (index, elem)
    # For each index + row in the enumerated board
    # Print the element in the list at the index of the row >> row_header[0]=8
    # Then, for every element/column in each row list
    # Print the column if true (has a chess piece), or print ' ' if empty
    # Separate all cells with '  |  ' for readability
    for index, row in enumerate(board):
        print(
            str(row_headers[index]) +
            row_spacing +
            '  | '.join([column if column else ' ' for column in row])
        )


# Function to validate the player's input + move is valid
# Passes the input_string from the player_move function below
# Also validate that input valid: (A2)
    # Input = length 2
    # First char is Alpha + A-H
    # Second char is num + 1-8
def player_input(input_string):
    # lowercase player input
    location = input(input_string).lower()

    # While none of the needed conditions are true:
    # Return error message + re-prompt for input until all are True
    while (len(location) != 2
            or not location[0].isalpha()
            or not location[1].isdigit()
            or location[0] not in column_headers
            or int(location[1]) not in row_headers):
        print(ERROR_INVALID_LOC)
        return player_input(input_string)

    # Return 2 values
    # Use first char of input and lookup in col list to get col
    # Use second char of input and subtract from 8 to get row
    return column_headers.index(location[0]), 8 - int(location[1])


# Function to validate valid moves depending on:
    # Selected piece type
    # Current player color
# Pass the selected piece, the selected col + row, and target col + row
def move_validation(selected_piece, piece_column, piece_row, target_column, target_row):
    # Define the absolute value of change in col + row
    # Distance that can be traveled backwards/forwards
    # For different pieces
    delta_col = abs(target_column - piece_column)
    delta_row = abs(target_row - piece_row)

    # Determine the piece type from the selected piece
    # And looking it up in the pieces dictionary.
    # If the conditions meet the requirements
    # It is a valid move, return 'True'

    # Kings move one space in either hor/vert direction
    if pieces[selected_piece][0] == 'king':
        return delta_col <= 1 and delta_row <= 1

    # Queens can move any number of cells vert, horizontal, and diagonal
    # Diagonal >> slope of 1 >> delta_row/delta_col >> delta_row == delta_col
    # Distance already limited by range of board,
    # so no specific range limit parameters need to be set.
    if pieces[selected_piece][0] == 'queen':
        return ((delta_row == delta_col)
                or (delta_col != 0 and delta_row == 0)
                or (delta_col == 0 and delta_row != 0))

    # Bishops can move diagonally any number of cells
    if pieces[selected_piece][0] == 'bishop':
        return delta_row == delta_col

    # Knights can move 2 + 1 in an 'L' Shape.
    # If they move 2 cells vert, 1 must be horizontal
    if pieces[selected_piece][0] == 'knight':
        return ((delta_col == 2 and delta_row == 1)
                or (delta_col == 1 and delta_row == 2))

    # Rooks can move vert/hor any number of cells
    if pieces[selected_piece][0] == 'rook':
        return ((delta_col != 0 and delta_row == 0)
                or (delta_col == 0 and delta_row != 0))

    # Pawns move 1 space forward only.
    # Except:
        # First move for pawn, can move 1-2 cells forward
        # Can move diagonal forward only to capture
    if pieces[selected_piece][0] == 'pawn':
        # First move for Pawns:
        # If in row index 1 (Black pawns) or row index 6 (White Pawns)
        # It is the first move + can move 1-2 moves vertically forward
        if ((piece_row == 1 and pieces[selected_piece][1] == 'b')
                or (piece_row == 6 and pieces[selected_piece][1] == 'w')):
            # Since there are pieces behind the pawns
            # Going backwards is invalid either way
            # Simplify by using absolute value (cheating)
            return delta_row <= 2 and delta_col == 0
        # Pawn Capturing:
        # if diagonal board space contains an opposite player piece (not '')
        # Can move diagonally forward one space
        elif (board[target_row][target_column] != ''):
            return ((delta_row == delta_col)
                    and (delta_col <= 1 or delta_row <= 1))
        # Normal moves:
        # Can only move vertically one space through rows up/down
        # Based on color of pawn
        elif board[target_row][target_column] == '':
            return ((pieces[selected_piece][1] == 'b'
                    and target_row - piece_row == 1
                    and delta_col == 0)
                    or
                    (pieces[selected_piece][1] == 'w'
                    and target_row - piece_row == -1
                    and delta_col == 0))


# Function to define Promoting a Pawn
# Pawns are promoted if they reach the other side of the board
# They can be turned into any piece of the player's choosing
def promotion(selected_piece):
    # Prompt input for piece it should be promoted to
    promo = input(PROMO_STRING).lower()

    # If input is not in the list of valid pieces (lookup from pieces dict key)
    # Or if input = king
    # Re-prompt entry
    if promo not in list(set([piece[0] for piece in pieces.values()])):
        promo = input(ERROR_INVALID_PROMO + PROMO_STRING).lower()
    elif promo == 'king':
        promo = input(ERROR_INVALID_PROMO + PROMO_STRING).lower()

    # Else it is a valid promotion.
    # Look up the Key (piece) from pieces dictionary
    # Based on input + current player color
    # key = piece
    # value[0] = type (King, Queen, etc.)
    # value[1] >> color
    # Return type, replace on board.
    else:
        for key, value in pieces.items():
            if promo == value[0] and pieces[selected_piece][1] == value[1]:
                return key


# Function to move pieces, validate moves, and update board.
# Takes the current_player, and captured pieces lists
def player_move(current_player, captured_b, captured_w):
    # Selecting a piece to move >>>
    # Call player_input function.
    # Player input function returns 2 items
    # Assign as a tuple (pieec_col, piece_row)
    piece_column, piece_row = player_input(SELECT_PIECE_STRING)

    # Lookup piece on board using the tuple
    # Selected piece var = A1. A = col, 1 = row.
    # Locate cell  = find the row 1, then find column A
    selected_piece = board[piece_row][piece_column]

    # Check if selected piece is valid:
    # Invalid if:
    # If selected piece is '' empty (false)
    # Or if player color does not match assigned color in pieces dictionary
    # Give error + re-prompt until valid choice
    while selected_piece == '' or current_player != pieces[selected_piece][1]:
        print(ERROR_INVALID_PIECE)
        piece_column, piece_row = player_input(SELECT_PIECE_STRING)
        selected_piece = board[piece_row][piece_column]

    # Look up selected piece using the Pieces dicionary
    # And print piece type
    print('You have selected: '
            + pieces[selected_piece][0].upper() + ' ' + selected_piece)

    # Get input for where piece should be moved >>>
    # Call player_input function, assign input as col, row
    # Locate target cell = find the target row, then find cell in target col
    target_column, target_row = player_input(INPUT_LOC)
    target_cell = board[target_row][target_column]

    # Validate target location is empty
    # Or piece in cell is not the players own piece for capture
    # Validate different moves for various types of pieces
    # Re-prompt until valid
    while (target_cell != '' and current_player == pieces[target_cell][1]) or not move_validation(selected_piece, piece_column, piece_row, target_column, target_row):
        print(ERROR_INVALID_LOC)
        target_column, target_row = player_input(INPUT_LOC)
        target_cell = board[target_row][target_column]

    # Valid piece & valid move:
    # Replace old spot on board with empty ''
    board[piece_row][piece_column] = ''

    # Print captured pieces and append to list
    if board[target_row][target_column] != '':
        if pieces[selected_piece][1] == 'b':
            captured_w.append(board[target_row][target_column])
        if pieces[selected_piece][1] == 'w':
            captured_b.append(board[target_row][target_column])

    # Replace old captured piece with new piece
    board[target_row][target_column] = selected_piece

    # Promotion:
    # Pawns are promoted when they reach the other side of the board
    # If selected piece is a pawn
    # and if target space is the other side of the board
    # and its a valid move
    # Call promotion function
    if pieces[selected_piece][0] == 'pawn':
        if ((target_row == 0 and pieces[selected_piece][1] == 'w')
                or (target_row == 7 and pieces[selected_piece][1] == 'b')):
            promoted_piece = promotion(selected_piece)
        # While Promoted piece is false, continue calling
            while not promoted_piece:
                promoted_piece = promotion(selected_piece)
            # If True, replace pawn on board with promoted piece
            board[target_row][target_column] = promoted_piece


# START
main()
