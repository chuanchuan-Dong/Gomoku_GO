import numpy as np
from MCTS import MC_TreeSearch 
from MCTS_node import MC_TreeNode
from gomoku_game_design import *
import random

AI_player = 1
Human_player = -1

def positive_or_negative():
    if random.random() < 0.5:
        return "Human_player", Human_player
    else:
        return "AI_player", AI_player

start_person_str, start_person = positive_or_negative()
state_start = np.zeros((15,15))
print(f"The game start from {start_person_str}")
game_state = gomoku_game(state=state_start, next_person=start_person, win=5)

game_node = MC_TreeNode(state=game_state, parent=None)
print(f"{game_node.state.board}")

while not game_node.is_terminal_node():
    game_node = MC_TreeNode(state=game_state, parent=None)
    if game_node.state.next_person == AI_player:
        mcts = MC_TreeSearch(game_node)
        print("Waiting AI decision...")
        next_move = mcts.best_move(10000)
        game_state = next_move.state
        

    if game_node.state.next_person == Human_player:
        row_cor = int(input("Your row cor"))
        col_cor = int(input("Your col cor"))
        next_step = gomoku_move(x_cor=row_cor, y_cor=col_cor, value=Human_player)
        game_state = game_node.state.move(next_step)
        
    print("Here is new board:")
    print(game_state.board)

            
    

