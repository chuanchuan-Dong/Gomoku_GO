from MCTS_node import MC_TreeNode
class MC_TreeSearch():
    def __init__(self, node: MC_TreeNode) -> None:
        self.root = node

    def best_move(self, simulation_number = 1000):
        for _ in range(0, simulation_number):
           v = self.policy_in_searchtree() # v is the next move
           reward = v.rollout()
        #    print(v.state.board)
        #    print(reward)
           v.backpropagate(reward)
        return self.root.best_children()



    def policy_in_searchtree(self) -> MC_TreeNode:
        """
        select a node to run rollout
        return a node
        """
        currenn_node = self.root
        while not currenn_node.is_terminal_node():
            if not currenn_node.is_fully_expand(): 
                return currenn_node.expand()
            else:
                currenn_node = currenn_node.best_children()
                # print(currenn_node.state.board)
                # print(f"find best children,{currenn_node.is_terminal_node()}")

        return currenn_node
        