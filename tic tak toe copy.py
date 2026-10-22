import random
import pygame
import math
import time
import colorsys
from pygame._sdl2.video import Window
pygame.init()
monitor_info = pygame.display.Info()
SCREEN_WIDTH = monitor_info.current_w
SCREEN_HEIGHT = monitor_info.current_h
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True
BG_COLOUR = (0, 0, 0)




#TICK TAC TOE
#players are x,o
#rows then colums
#y then x




######## FIX EDGE CASES, eg when colom 0 has all x
def draw_board(board):
    screen.fill(BG_COLOUR)
    board_lines = [[(300,0),(300,900)],[(600,0),(600,900)],[(0,300),(900,300)],[(0,600),(900,600)]]
    for i in board_lines:
        pygame.draw.line(screen, (255,255,255), i[0],i[1],10)
    r = -1
    for i in board:
        r += 1
        c = -1
        for j in i:
            c+= 1
            if j == "x":
                draw_x(c*300 + 150,r*300 + 150, 250)
            if j == "o":
                draw_o(c*300 + 150,r*300 + 150, 250)
                
def won_line(in_val):
    in_val = in_val[0]
    if in_val <= 2:
        line_over_pos = [(0,in_val*300+150),(900,in_val*300+150)]
    elif in_val <= 5:
        line_over_pos = [((in_val-3)*300+150,0),((in_val-3)*300+150,900)]
    elif in_val == 6:
        line_over_pos = [(0,0),(900,900)]
    else:
        line_over_pos = [(0,900),(900,0)]
    pygame.draw.line(screen, (255,255,255), line_over_pos[0],line_over_pos[1],10)
    pygame.display.flip()
    time.sleep(5)


def draw_x(x,y,size):
    board_lines = [[(x + size/2,y + size/2),(x - size/2,y - size/2)],[(x - size/2,y + size/2),(x + size/2,y - size/2)]]
    #[(x + size/2,y - size/2),(x + 50,y - size/2)]
    for j in board_lines:
        pygame.draw.line(screen, (255,0,0), j[0],j[1],20)
    
def draw_o(x,y,size):
    pygame.draw.circle(screen, (0,0,255),(x,y),size/2,20)



# TIC TAC TOE
# players are x, o
# rows then columns (y then x)
def user_selection(player, board):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mposx = event.pos[0]
                    mposy = event.pos[1]
                    mposx = math.floor(mposx/300)
                    mposy = math.floor(mposy/300)
                    if board[mposy][mposx] == "":
                        run = False
                        board[mposy][mposx] = player
                
        
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
    direction = []
    target_pl = 3
    possible = False
    
    # HORIZONTAL
    idxx = 0
    for i in board:
        n, pl = check_num_list(i, player)
        var = posi_done(n)
        if var[1]:
            direction.append(idxx)
        if var[0] and pl != 3:
            possible = True
            target_pl = [idxx, pl]
        idxx += 1

    # VERTICAL
    for i in range(3):
        vert = [board[0][i], board[1][i], board[2][i]]
        n, pl = check_num_list(vert, player)
        var = posi_done(n)
        if var[1]:
            direction.append(i+3)
        if var[0] and pl != 3:
            possible = True
            target_pl = [pl, i]

    # DIAGONAL
    hor = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    positions = [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]
    for i in range(2):
        n, pl = check_num_list(hor[i], player)
        var = posi_done(n)
        if var[1]:
            direction.append(i+6)
        if var[0] and pl != 3:
            possible = True
            target_pl = positions[i][pl]

    return [possible,direction!=[],target_pl,direction]

def print_board(board):
    for row in board:
        print(row)
    print()

def main_2p():
    board = init()
    draw_board(board)
    pygame.display.flip()
    peices = ["x", "o"]
    idx = -1
    while True:
        idx += 1
        peice = peices[idx % 2]
        board = user_selection(peice, board)
        print_board(board)
        draw_board(board)
        pygame.display.flip()
        p_d = line_check(peice, board)
        if p_d[1]:
            print(f"{peice} WINS")
            won_line(p_d[3])
            return
        elif check_draw(board):
            time.sleep(0.5)
            screen.fill(BG_COLOUR)
            font = pygame.font.Font(None, 350)
            text_surface = font.render("DRAW", True, ((255,255,255)))
            screen.blit(text_surface, (80, 370))
            pygame.display.flip()
            print("DRAW")
            time.sleep(5)
            return

def main_ai(hgf):
    screen = pygame.display.set_mode((900, 900), pygame.SHOWN)
    sdl_window = Window.from_display_module()
    sdl_window.focus()
    
    
    board = init()
    h_peice = "x"
    ai_peice = "o"
    draw_board(board)
    pygame.display.flip()
    
    # Set starting turn based on hgf (Human Goes First) flag
    turn = "human" if hgf else "ai"
    running = True
    while running:
        draw_board(board)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if turn == "human":
            # --- Human Turn ---
            board = user_selection(h_peice, board)
            print_board(board)
            draw_board(board)
            pygame.display.flip()

            p_d = line_check(h_peice, board)
            if p_d[1]:
                print(f"{h_peice} WINS")
                won_line(p_d[3])
                return
            if check_draw(board):
                time.sleep(0.5)
                screen.fill(BG_COLOUR)
                font = pygame.font.Font(None, 350)
                text_surface = font.render("DRAW", True, ((255,255,255)))
                screen.blit(text_surface, (80, 370))
                pygame.display.flip()
                print("DRAW")
                time.sleep(5)
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
            draw_board(board)
            pygame.display.flip()

            # Check if AI won or drew
            p_d_ai = line_check(ai_peice, board)
            if p_d_ai[1]:
                print(f"{ai_peice} WINS")
                won_line(p_d_ai[3])
                return
            if check_draw(board):
                time.sleep(0.5)
                screen.fill(BG_COLOUR)
                font = pygame.font.Font(None, 350)
                text_surface = font.render("DRAW", True, ((255,255,255)))
                screen.blit(text_surface, (80, 370))
                pygame.display.flip()
                print("DRAW")
                time.sleep(5)
                return
                return
            
            turn = "human"
font = pygame.font.Font(None, 100)
text_surface = font.render("1", True, ((255,255,255)))
screen.blit(text_surface, (100, 420))
text_surface = font.render("2", True, ((255,255,255)))
screen.blit(text_surface, (700, 420))
pygame.display.flip()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                run = False
                if event.pos[0] <= 450:
                    nump = 1
                else:
                    nump = 2
                        
screen.fill(BG_COLOUR)                       
if nump == 1:
    font = pygame.font.Font(None, 100)
    text_surface = font.render("Go first?", True, ((255,255,255)))
    screen.blit(text_surface, (450, 100))
    text_surface = font.render("y", True, ((255,255,255)))
    screen.blit(text_surface, (100, 420))
    text_surface = font.render("n", True, ((255,255,255)))
    screen.blit(text_surface, (700, 420))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    run = False
                    if event.pos[0] <= 450:
                        nump = "Y"
                    else:
                        nump = "N"
    screen.fill(BG_COLOUR)  
    main_ai(nump.upper()=="Y")
else:
    main_2p()