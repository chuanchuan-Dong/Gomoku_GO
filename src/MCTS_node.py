from gomoku_game_design import gomoku_move, gomoku_game
from collections import defaultdict
import numpy as np

class MC_TreeNode():
    def __init__(self, state: gomoku_game, parent=None) -> None:
        self.state = state
        self.parent: MC_TreeNode = parent
        self.children = []
        
        self.number_of_visit = 0
        self.untried_action = None
        self.result = defaultdict(int)

        
    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def is_fully_expand(self):
        
        return len(self.find_untried_action_of_node()) == 0
    

    def find_untried_action_of_node(self) -> gomoku_move:
        if self.untried_action is None:
            self.untried_action = self.state.get_legal_action()
        return self.untried_action
    
    def q(self):
        win = self.result[self.parent.state.next_person]
        loss = self.result[-self.parent.state.next_person]
        return win - loss


    def n(self):
        return self.number_of_visit


    def expand(self):
        action = self.find_untried_action_of_node().pop()
        next_state = self.state.move(action)
        child_node = MC_TreeNode(next_state, parent=self)
        self.children.append(child_node)
        # print("expand")
        return child_node
    
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def rollout(self, AI_player = 1):  # Only consider 3 depth from AI view
        current_state = self.state

        for _ in range(3):
            # print(f"---------------Start roll out{i} ----------------")
            # print(current_state.board)
            # print(current_state.is_game_over())
            if current_state.is_game_over():
                # print("The node is attach game over")
                # print(current_state.board)
                AI_player_reward = current_state.get_reward(person=AI_player)
                human_player_reward = current_state.get_reward(person= -AI_player)
                # return current_state.get_reward(person=AI_player)
                return AI_player_reward - 0.8*human_player_reward

            else:
                # print("The node Not is attach game over, After move")
                possible_action = current_state.get_legal_action()
                action = self.rollout_policy(possible_action)
                current_state = current_state.move(action)
                # print(current_state.board)
            AI_player_reward = current_state.get_reward(person=AI_player)
            human_player_reward = current_state.get_reward(person= -AI_player)
        
        # return current_state.get_reward(person=AI_player)
        return AI_player_reward - 0.8*human_player_reward
    
    def backpropagate(self, result, next_person=1):
        self.number_of_visit += 1
        self.result[next_person] += result
        if self.parent:
            self.parent.backpropagate(result)


    def best_children(self,c_para = 1.5):
        weight = []
        for each_children in self.children:
            each_weight = each_children.q() / each_children.n() + c_para * np.sqrt(np.log(self.n()) / each_children.n())
            weight.append(each_weight)
        return self.children[np.argmax(weight)]