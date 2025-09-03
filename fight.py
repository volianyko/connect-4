import mcts_agent
import minimax_agent
from minimax_agent import count_inrow, possible_moves, drop
import random

def create_empty_board(num_rows, num_cols):
    board = []
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            row.append(0)
        board.append(row)
    return board


def game_over(board, num_rows, num_cols, inrow):
    if count_inrow(board, num_cols, num_rows, inrow, inrow, 1):
        return 1
    if count_inrow(board, num_cols, num_rows, inrow, inrow, 2):
        return 2
    if len(possible_moves(board, num_cols)) == 0:
        return 3
    return 0


def outputBoard(board):
    print("-------------------")
    for row in board:
        for cell in row:
            print(cell, end=' ')
        print()
    print("-------------------")


def fight(firstmove):

    num_rows = 6
    num_cols = 7
    inrow = 4
    board = create_empty_board(num_rows, num_cols)

    player = firstmove
    #player = random.randint(1, 2)
    print(f'player {player} starts the game')

    while not game_over(board, num_rows, num_cols, inrow):

        if player==1:
            next_move = mcts_agent.move(board, num_cols, num_rows, inrow, player=1)
        else:
            next_move = minimax_agent.move(board, num_cols, num_rows, inrow)
        
        print(f'player {player} chose {next_move+1}')
        board = drop(board, next_move, num_rows, player)
        player = 3-player
        
        outputBoard(board)
    #outputBoard(board)
    g = game_over(board, num_rows, num_cols, inrow)
    if g==1:
        print("MCTS won!!!")
    if g==2:
        print("Minimax won!")
    else:
        print("Draw!")

    return g


def fiiight():

    n = 10

    win_1 = 0
    draw = 0
    win_2 = 0
    for i in range(n):
        if i%2==0: g = fight(1)
        else: g = fight(2)

        print('\n\n\n')

        if g==1:
            win_1+=1
        if g==2:
            win_2+=1
        else:   draw+=1
    
    print(f'{n} games were played')
    print(f'MCTS won {win_1} games (with ratio {win_1/n})')
    print(f'minimax won {win_2} games (with ratio {win_2/n})')
    print(f'{draw} games ended in a draw (with ratio {draw/n})')


    

fiiight()
