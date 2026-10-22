import random

# TIC TAC TOE
# players are x, o
# rows then columns (y then x)

def debug():
    list_n = [['', '', ''], ['', '', ''], ['', '', '']]
    return list_n

def user_selection(player, board):
    running = True
    while running:
        print(f"where do you want to place {player}?")
        row = int(input("row (0-2): "))
        column = int(input("column (0-2): "))
        if 0 <= row <= 2 and 0 <= column <= 2:
            if board[row][column] == '':
                board[row][column] = player
                running = False
            else:
                print("Whohoho there, someone's piece is there, try again")
        else:
            print("Invalid row or column, please use 0, 1, or 2.")
        
    return board

def check_draw(board):
    draw = True
    for i in board:
        for j in i:
            if j == "":
                draw = False
                return draw
    return draw

def get_next_to(idxx, idxy, list_n, dir_x, dir_y):
    idxx += dir_x
    idxy += dir_y
    return list_n[idxy][idxx]

def init():
    list_b = []
    for i in range(3):
        list_b.append(["", "", ""])
    return list_b

def check_num_list(list_n, player):
    idx = 0
    idxx = 0
    pl = 3
    for i in list_n:
        if i == player:
            idx += 1
        elif i != "":
            return [0, 3]
        else:
            pl = idxx
        idxx += 1

    return idx, pl

def posi_done(n):
    p = False
    d = False
    if n >= 2:
        p = True
        if n == 3:
            d = True
        
    return [p, d]

def line_check(player, board):
    target_pl = 3
    possible = False
    
    # HORIZONTAL
    idxx = 0
    for i in board:
        n, pl = check_num_list(i, player)
        var = posi_done(n)
        if var[1]:
            return [True, True, 3]
        if var[0]:
            possible = True
            target_pl = [idxx, pl]
        idxx += 1

    # VERTICAL
    for i in range(3):
        vert = [board[0][i], board[1][i], board[2][i]]
        n, pl = check_num_list(vert, player)
        var = posi_done(n)
        if var[1]:
            return [True, True, 3]
        if var[0]:
            possible = True
            target_pl = [pl, i]

    # DIAGONAL
    hor = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    positions = [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]
    for i in range(2):
        n, pl = check_num_list(hor[i], player)
        var = posi_done(n)
        if var[1]:
            return [True, True, 3]
        if var[0]:
            possible = True
            target_pl = positions[i][pl]

    return [possible, False, target_pl]

def print_board(board):
    for row in board:
        print(row)
    print()

def main_2p():
    board = debug()
    peices = ["x", "o"]
    idx = -1
    while True:
        idx += 1
        peice = peices[idx % 2]
        board = user_selection(peice, board)
        print_board(board)
        p_d = line_check(peice, board)
        if p_d[1]:
            print(f"{peice} WINS")
            return
        elif check_draw(board):
            print("DRAW")
            return

def main_ai(hgf):
    board = debug()
    h_peice = "x"
    ai_peice = "o"
    
    # Set starting turn based on hgf (Human Goes First) flag
    turn = "human" if hgf else "ai"

    while True:
        if turn == "human":
            # --- Human Turn ---
            board = user_selection(h_peice, board)
            print_board(board)

            p_d = line_check(h_peice, board)
            if p_d[1]:
                print(f"{h_peice} WINS")
                return
            if check_draw(board):
                print("DRAW")
                return
            
            turn = "ai"

        else:
            # --- AI Turn ---
            p_d_human = line_check(h_peice, board)
            human_block_place = p_d_human[2]
            
            ai_check = line_check(ai_peice, board)
            ai_win_place = ai_check[2]

            # 1. Take winning move if available
            if ai_check[0] and ai_win_place != 3:
                board[ai_win_place[0]][ai_win_place[1]] = ai_peice
            # 2. Otherwise block human winning move
            elif p_d_human[0] and human_block_place != 3:
                board[human_block_place[0]][human_block_place[1]] = ai_peice
            # 3. Otherwise pick a random empty space
            else:
                running_ai = True
                while running_ai:
                    a = random.randint(0, 2)
                    b = random.randint(0, 2)
                    if board[a][b] == '':
                        board[a][b] = ai_peice
                        running_ai = False

            print("AI placed its piece:")
            print_board(board)

            # Check if AI won or drew
            p_d_ai = line_check(ai_peice, board)
            if p_d_ai[1]:
                print(f"{ai_peice} WINS")
                return
            if check_draw(board):
                print("DRAW")
                return
            
            turn = "human"

main_ai(False)