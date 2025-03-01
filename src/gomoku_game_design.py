import numpy as np
from itertools import groupby


def count(board, player=1,n=15):
    """
    board should be a list
    
    """
    open_count = np.zeros(5)
    closed_count = np.zeros(5)
    board_shape = n
    for i in range(board_shape):
        row_each = board[i]
        groupboard = groupby(row_each)
        each_key = []
        each_num = []
        the_last_group = 0
        for i, (key, group) in enumerate(groupboard): # 
            each_key.append(key)
            each_num.append(len(list(group))-1)
            the_last_group = i
        #end for
        for i in range(the_last_group + 1 ):
            if each_key[i] == player:
                if len(each_key) == 1:
                    open_count[each_num[i]] += 1
                    continue
                if i == 0:
                    if each_key[i+1] == -player: #closed
                        closed_count[each_num[i]] += 1
                        continue
                    else :
                        open_count[each_num[i]] += 1
                        continue
                if i == the_last_group:
                    if each_key[i-1] == -player: #closed
                        closed_count[each_num[i]] += 1 
                        continue
                    else:
                        open_count[each_num[i]] += 1
                        continue
                else:
                    if each_key[i+1] == -player and each_key[i-1] == -player: #closed
                        closed_count[each_num[i]] += 1
                        # print("case31")
                    else:
                        open_count[each_num[i]] += 1
                        # print(i)
                        # print("case32")
        #end for 
    #end for
    return open_count, closed_count

def turn_diag_list(matrix):
    dig_list = []
    for i in range(-matrix.shape[0]+1, matrix.shape[1], 1):
        dig_list.append(list(matrix.diagonal(i)))
    return dig_list

class gomoku_move():
    def __init__(self, x_cor, y_cor, value) -> None:
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.value = value

class gomoku_game():
    x = 1 #AI
    o = -1
    def __init__(self, state, next_person, win=5) -> None:
        """


        Input: 
            state: the game  state (15 * 15)
        """
        self.board = state
        self.board_size = state.shape[0]
        self.win = win # how many in the board lead to win
        self.next_person = next_person


    def check_win(self):
        """
        1 means x wins 
        -1 means o wins
        0 means draw
        None means no result yet.
        """
        for i in range(self.board_size - self.win + 1):
            row_sum = np.sum(self.board[:,i:i+self.win], axis = 1)
            colum_sum = np.sum(self.board[i:i+self.win,:], axis= 0)
            if row_sum.max() == self.win or colum_sum.max() == self.win:
                return self.x
            
            if row_sum.min() == -self.win or colum_sum.min() == -self.win:
                return self.o
        for i in range(self.board_size - self.win + 1):
            for j in range(self.board_size - self.win + 1):
                sub_board = self.board[i:i+self.win, j:j+self.win]
                dig_sum = np.trace(sub_board)
                dig_sum_inv = np.trace(sub_board[::-1])
                if dig_sum == self.win or dig_sum_inv == self.win:
                    return self.x
                if dig_sum == -self.win or dig_sum_inv == -self.win:
                    return self.o
        # draw 
        if np.all(self.board != 0):
            return 0
        
        return None
    
    def get_reward(self, person=1):
        gomoku_board_list_row = (self.board.tolist())
        gomoku_board_list_col = self.board.T.tolist()
        gomoku_board_list_diag = turn_diag_list(self.board)
        gomoku_board_list_diag_inv = turn_diag_list(self.board[::-1])
        o_row, c_row = count(gomoku_board_list_row, person,len(gomoku_board_list_row))
        o_col, c_col = count(gomoku_board_list_col, person, len(gomoku_board_list_col))
        o_diag, c_diag = count(gomoku_board_list_diag, person, len(gomoku_board_list_diag))
        o_diag_inv, c_diag_inv = count(gomoku_board_list_diag_inv, person, len(gomoku_board_list_diag_inv))    
        open_count = np.array(o_row+o_col+o_diag_inv+o_diag)
        close_count = np.array(c_row+c_col+c_diag+c_diag_inv)
        Point_Open = np.array([1,10,100,1000, 1e10])
        Point_Close = np.array([0.11,1,10,100, 1e10])
        return np.sum(np.multiply(open_count, Point_Open)) + np.sum(np.multiply(close_count, Point_Close))


    def is_game_over(self):
        """
        check wheter game is over 
        retrun 1: game over
               0: keep going 
        """
        return self.check_win() is not None
    
    def check_move_legal(self, move: gomoku_move):
        if move.value != self.next_person:
            return False
        
        x_in_range = (0 <= move.x_cor < self.board_size)
        y_in_range = (0 <= move.y_cor < self.board_size)
        if not x_in_range or not y_in_range:
            return False

        return self.board[move.x_cor, move.y_cor] == 0
    
    def move(self, move: gomoku_move):
        if not self.check_move_legal(move):
            raise ValueError("It is ilegal move")
        new_board = self.board.copy()
        new_board[move.x_cor, move.y_cor] = move.value
        next_person = - self.next_person

        return type(self)(new_board, next_person) #######
    
    def get_legal_action(self):
        index = np.where(self.board == 0)
        return [gomoku_move(coord[0], coord[1], self.next_person)
                for coord in list(zip(index[0], index[1]))]