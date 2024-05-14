"""
# logic flow
1.set empty board
2.loop until win
    a.get users input
        i.check if valid
        ii.skip pc input if not
    b.random pc input
        i.check if valid
        ii.repeat until valid
    c.check board state - has someone won?
    d.if win, check who won
    e.draw conidition - if no more spaces and no win
3.print winner

# co-ordinates
input = X, Y
list = [Y][X]

# board layout
(0,0) | (1,0) | (2,0)
(0,1) | (1,1) | (2,1)
(0,2) | (1,2) | (2,2)

# win conditions
(0,0), (1,0), (2,0)
(0,1), (1,1), (2,1)
(0,2), (1,2), (2,2)
(0,0), (0,1), (0,2)
(1,0), (1,1), (1,2)
(2,0), (2,1), (2,2)
(0,0), (1,1), (2,2)
(2,0), (1,1), (0,2)
"""

import random
from tabulate import tabulate

random.seed()

def main():
    
    # set empty board
    board = [
        ["-","-","-"],
        ["-","-","-"],
        ["-","-","-"]
    ]

    # request difficulty from user - if not hard, then easy
    difficulty = input("Difficulty (hard or easy): ")

    while True:
        # check for valid input
        try:
            co_ords_user = user_move(board)
        except ValueError:
            continue
        
        # check if spot available
        if check_available(board,co_ords_user):
            board[co_ords_user[1]][co_ords_user[0]] = "X"
        else:
            print("Spot already used")
            continue

        # check for winner
        winner = check_win(board)

        if winner:
            print(tabulate(board,tablefmt="jira"))
            if winner == "X":
                print("player wins!")
            else:
                print("PC wins")
            break

        # check for draw
        if check_draw(board):
            print(tabulate(board,tablefmt="jira"))
            print("Draw")
            break

        ### PC move
        while True:
        
            if difficulty.lower().strip() != "hard":
                # PC - easy level
                co_ords_pc = pc_move_easy(board)

                if check_available(board,co_ords_pc):
                    board[co_ords_pc[1]][co_ords_pc[0]] = "O"
                    break
                else:
                    continue

            # PC - hard level
            else:
                co_ords_pc = pc_move_hard(board)

                if check_available(board,co_ords_pc):
                    print(co_ords_pc)
                    board[co_ords_pc[1]][co_ords_pc[0]] = "O"
                    break
                else:
                    continue
        
        # print board
        print(tabulate(board,tablefmt="jira"))

        # check for winner
        winner = check_win(board)

        if winner:
            if winner == "X":
                print("player wins!")
            else:
                print("PC wins")
            break

def check_available(board,co_ords):
    # return if specified co-ordinates is available spot
    return board[co_ords[1]][co_ords[0]] == "-"

def user_move(board):
    # get move
    move = input("Move: ")

    # check if input is valid e.g (1,2) and raise errors if not
    try:
        co_ords = list(map(int,move.split(",")))
    except:
        raise ValueError
    else:
        if len(co_ords) != 2:
            raise ValueError

        for i in co_ords:
            if i > 2 or i < 0:
                raise ValueError
            
    return co_ords

def pc_move_easy(board):
    # return 2 random numbers between 0 and 2
    return [random.randint(0,2),random.randint(0,2)]

def check_win(board):
    # check each possible winning combination and return the player with that combo
    if board[0][0] != "-" and board[0][0] == board[0][1] == board[0][2]:
        return board[0][0]
    elif board[1][0] != "-" and board[1][0] == board[1][1] == board[1][2]:  
        return board[1][0]
    elif board[2][0] != "-" and board[2][0] == board[2][1] == board[2][2]:  
        return board[2][0]
    elif board[0][0] != "-" and board[0][0] == board[1][0] == board[2][0]:  
        return board[0][0]
    elif board[0][1] != "-" and board[0][1] == board[1][1] == board[2][1]:  
        return board[0][1]
    elif board[0][2] != "-" and board[0][2] == board[1][2] == board[2][2]: 
        return board[0][2] 
    elif board[0][0] != "-" and board[0][0] == board[1][1] == board[2][2]: 
        return board[0][0] 
    elif board[0][2] != "-" and board[0][2] == board[1][1] == board[2][0]:  
        return board[0][2]

def check_draw(board):
    # loop through each row and return False if there's still unclaimed spots
    for i in board:
        if i.count("-") != 0:
            return False
        
    # return True if no unclaimed spots 
    return True

def check_first_move(board):
    for i in board:
        if i.count("O") != 0:
            return False
        
    # return True if no unclaimed spots 
    return True

def pc_move_hard(board):
    """
    optimal play

    first turn
    1. if center, go corner
    2. if anything else, go center

    next turn(s)
    1. if can win, win
    2. if user can win, block
    3. otherwise corners if value
    4. otherwise random
    """
    if check_first_move(board):
        if board[1][1] == "X":
            return [random.choice([0,2]),random.choice([0,2])]
        else:
            return [1,1]
    else:
        # top row near complete        
        if board[0][0] != "-" and board[0][0] == board[0][1] and board[0][2] == "-":
            return [2,0]

        elif board[0][0] != "-" and board[0][0] == board[0][2] and board[0][1] == "-":
            return [1,0]

        elif board[1][0] != "-" and board[0][1] == board[0][2] and board[0][0] == "-":
            return [0,0]
        
        # mid row near complete
        if board[1][0] != "-" and board[1][0] == board[1][1] and board[1][2] == "-":
            return [2,1]

        elif board[1][0] != "-" and board[1][0] == board[1][2] and board[1][1] == "-":
            return [1,1]

        elif board[1][1] != "-" and board[1][1] == board[1][2] and board[1][0] == "-":
            return [0,1]

        # bottom row near complete
        if board[2][0] != "-" and board[2][0] == board[2][1] and board[2][2] == "-":
            return [2,2]

        elif board[2][0] != "-" and board[2][0] == board[2][2] and board[2][1] == "-":
            return [1,2]

        elif board[2][2] != "-" and board[2][1] == board[2][2] and board[2][0] == "-":
            return [0,2]        
                    
        # first col near complete
        if board[0][0] != "-" and board[0][0] == board[1][0] and board[2][0] == "-":
            return [0,2]

        elif board[0][0] != "-" and board[0][0] == board[2][0] and board[1][0] == "-":
            return [0,1]

        elif board[1][0] != "-" and board[1][0] == board[2][0] and board[0][0] == "-":
            return [0,0]

        # mid col near complete
        if board[0][1] != "-" and board[0][1] == board[1][1] and board[2][1] == "-":
            return [1,2]

        elif board[0][1] != "-" and board[0][1] == board[2][1] and board[1][1] == "-":
            return [1,1]

        elif board[1][1] != "-" and board[1][1] == board[2][1] and board[0][1] == "-":
            return [1,0]
                    
        # last col near complete
        if board[0][2] != "-" and board[0][2] == board[1][2] and board[2][2] == "-":
            return [2,2]

        elif board[0][2] != "-" and board[0][2] == board[2][2] and board[1][2] == "-":
            return [2,1]

        elif board[1][2] != "-" and board[1][2] == board[2][2] and board[0][2] == "-":
            return [2,0]

        # diag -> near complete
        if board[0][0] != "-" and board[0][0] == board[1][1] and board[2][2] == "-":
            return [2,2]

        elif board[0][0] != "-" and board[0][0] == board[2][2] and board[1][1] == "-":
            return [1,1]

        elif board[1][1] != "-" and board[1][1] == board[2][2] and board[0][0] == "-":
            return [0,0]
        
        # diag <- near complete
        if board[0][2] != "-" and board[0][2] == board[1][1] and board[2][0] == "-":
            return [0,2]

        elif board[0][2] != "-" and board[0][2] == board[2][0] and board[1][1] == "-":
            return [1,1]

        elif board[1][1] != "-" and board[1][1] == board[2][0] and board[0][2] == "-":
            return [2,0]
        
        # corners
        corner_top_left_check = (
            board[0][0] == "-"
            and
            (
                (board[0][1] in ["-","O"] and board[0][2] in ["-","O"])
                or
                (board[1][0] in ["-","O"] and board[2][0] in ["-","O"])
                or
                (board[1][1] in ["-","O"] and board[2][2] in ["-","O"])
            )
        )

        corner_top_right_check = (
            board[0][2] == "-"
            and
            (
                (board[1][2] in ["-","O"] and board[2][2] in ["-","O"])
                or
                (board[0][1] in ["-","O"] and board[0][0] in ["-","O"])
                or
                (board[1][1] in ["-","O"] and board[2][0] in ["-","O"])
            )
        )

        corner_bottom_left_check = (
            board[2][0] == "-"
            and
            (
                (board[1][0] in ["-","O"] and board[0][0] in ["-","O"])
                or
                (board[2][1] in ["-","O"] and board[2][2] in ["-","O"])
                or
                (board[1][1] in ["-","O"] and board[0][2] in ["-","O"])
            )
        )

        corner_bottom_right_check = (
            board[2][2] == "-"
            and
            (
                (board[2][1] in ["-","O"] and board[2][0] in ["-","O"])
                or
                (board[1][2] in ["-","O"] and board[0][2] in ["-","O"])
                or
                (board[1][1] in ["-","O"] and board[0][0] in ["-","O"])
            )
        )

        if corner_top_left_check:
            return [0,0]
        elif corner_top_right_check:
            return [2,0]
        elif corner_bottom_left_check:
            return [0,2]
        elif corner_bottom_right_check:
            return [2,2]

        # otherwise return random
        return pc_move_easy(board)
    

if __name__ == "__main__":
    main()
