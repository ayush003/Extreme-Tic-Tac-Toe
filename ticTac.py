import sys
import random
import signal
from time import time
import copy
from operator import itemgetter


class Team72():

    def __init__(self):
        self.available_moves = []
        self.inc_costs = [0, 1, 100, 10000]
        self.INF = 10000000
        self.initial_level = 2
        self.endtime = 22
        self.starttime = 0
        self.max_player = 1
        self.map_symbol = ['o', 'x']
        self.num_blks_won = [0, 0]
        self.maxlen = 0
        self.mindepth = 9
        self.last_blk_won = 0
        self.dict = {}
        self.just_start = 1

    
    def update(self, board, old_move, new_move, ply):

        board.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply

        x = new_move[1]/3
        y = new_move[2]/3
        k = new_move[0]
        fl = 0

        # checking if a small_board has been won or drawn or not after the current move
        bs = board.big_boards_status[k]
        for i in range(3):
            # checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ply):
                board.small_boards_status[k][x][y] = ply
                return 'SUCCESSFUL', True
            # checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ply):
                board.small_boards_status[k][x][y] = ply
                return 'SUCCESSFUL', True
        # checking for diagonal patterns
        # diagonal 1
        if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ply):
            board.small_boards_status[k][x][y] = ply
            return 'SUCCESSFUL', True
        # diagonal 2
        if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ply):
            board.small_boards_status[k][x][y] = ply
            return 'SUCCESSFUL', True
        # checking if a small_board has any more cells left or has it been drawn
        for i in range(3):
            for j in range(3):
                if bs[3*x+i][3*y+j] == '-':
                    return 'SUCCESSFUL', False
        board.small_boards_status[k][x][y] = 'd'
        return 'SUCCESSFUL', False

        # checking if a small_board has been won or drawn or not after the current move

    def move(self, board, old_move, flag):
        
        start = time()
        self.starttime = start
        self.timeup = 0
        if flag == "x":
            self.max_player = 1
        elif flag == 'o':
            self.max_player = 0
        self.num_blks_won = [0, 0]
        player = self.max_player
        level = self.initial_level
        if self.last_blk_won:
            self.num_blks_won[self.max_player] = 1
        all_moves = board.find_valid_move_cells(old_move)
        length1 = len(all_moves)
        self.available_moves = board.find_valid_move_cells(old_move)
        length = length1
        random_no = random.randrange(length)
        prevans = self.available_moves[random_no]
        if self.just_start == 1:
            self.just_start = 0
            if self.max_player == 1:
                return prevans
        while(not self.timeup):
            ans, val = self.move_minimax(board, old_move, player, level)

            self.maxlen = max(self.maxlen, len(self.dict))
            if (self.timeup):
                break
            prevans = ans
            level += 1
        status, blk_won = self.update(
            board, old_move, prevans, self.map_symbol[player])

        if blk_won == True:
            self.last_blk_won ^= 1
        else:
            self.last_blk_won = 0
        board.big_boards_status[prevans[0]][prevans[1]][prevans[2]] = "-"
        board.small_boards_status[prevans[0]][prevans[1]/3][prevans[2]/3] = "-"
        self.mindepth = min(self.mindepth, level)
        return prevans

    

    def move_minimax(self, board, old_move, player, level):

        self.available_moves = board.find_valid_move_cells(old_move)
        best_move = self.available_moves[random.randrange((len(self.available_moves)))]
        maxval = -self.INF
        temp = self.num_blks_won[player]

        for move in self.available_moves:
            self.num_blks_won[player] = temp

            status, blk_won = self.update(
                board, old_move, move, self.map_symbol[player])
            if blk_won:
                self.num_blks_won[player] ^= 1
            else:
                self.num_blks_won[player] = 0

            if blk_won and self.num_blks_won[player] == 1:
                score = self.minimax(
                    level-1, player, move, -self.INF, self.INF, board, player)
                self.num_blks_won[player] = 0
            else:

                score = self.minimax(
                    level-1, player ^ 1, move, -self.INF, self.INF, board, player)

            board.big_boards_status[move[0]][move[1]][move[2]] = "-"
            board.small_boards_status[move[0]][move[1]/3][move[2]/3] = "-"

            if score > maxval:
                best_move = move
                maxval = score
        self.num_blks_won[player] = temp
        return best_move, score

    def minimax(self, level, player, old_move, alpha, beta, board, prev_player):
      
        if self.timeup == 1:
            return self.heuristic(board, prev_player, old_move)
        time_so_far = time() - self.starttime
        time_limit = self.endtime
        if time_so_far >= time_limit:
            self.timeup = 1
            return self.heuristic(board, prev_player, old_move)
        if board.find_terminal_state()!=('CONTINUE', '-'):
            return self.heuristic(board, prev_player, old_move)
        if level == 0:
            return self.heuristic(board, prev_player, old_move)
        score = self.INF
        possible_moves = board.find_valid_move_cells(old_move)
        if (player != self.max_player):
            score = score
        elif (player == self.max_player):
            score = -score

        temp = self.num_blks_won[player]

        for move in possible_moves:
            self.num_blks_won[player] = temp

            status, blk_won = self.update(
                board, old_move, move, self.map_symbol[player])
            if blk_won:
                self.num_blks_won[player] ^= 1
            else:
                self.num_blks_won[player] = 0

            if player == self.max_player:
                if blk_won and self.num_blks_won[player] == 1:
                    score = max(score, self.minimax(
                        level-1, player, move, alpha, beta, board, player))
                    self.num_blks_won[player] = 0
                else:
                    score = max(score, self.minimax(
                        level-1, player ^ 1, move, alpha, beta, board, player))
                
                if score >= alpha:
                    alpha = score

            else:
                if blk_won and self.num_blks_won[player] == 1:
                    score = min(score, self.minimax(
                        level-1, player, move, alpha, beta, board, player))
                    self.num_blks_won[player] = 0
                else:
                    score = min(score, self.minimax(
                        level-1, player ^ 1, move, alpha, beta, board, player))
                if score <= beta:
                    beta = score
            # undo move
            board.big_boards_status[move[0]][move[1]][move[2]] = "-"
            board.small_boards_status[move[0]][move[1]/3][move[2]/3] = "-"

            if self.timeup ==1:
                break

            if (alpha >= beta):
                break
        self.num_blks_won[player] = temp
        return score

    def heuristic(self, board, player, old_move):

        cur_state = board.find_terminal_state()
        if cur_state[1] == "WON":
            if player != self.max_player:
                return -self.INF
            elif player == self.max_player:
                return self.INF
        cost = [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]

        for i in range(3):
            for j in range(3):
                value1 = self.INF/100
                value2 = -self.INF/100
                if (board.small_boards_status[0][i][j] == self.map_symbol[self.max_player]):
                    cost[0][i][j] = value1
                elif(board.small_boards_status[0][i][j] == self.map_symbol[self.max_player ^ 1]):
                    cost[0][i][j] = value2  
                else:
                    cost[0][i][j] = self.computecost(board, self.max_player,0, i, j)
        for i in range(3):
            for j in range(3):
                if (board.small_boards_status[1][i][j] == self.map_symbol[self.max_player]):
                    cost[1][i][j] = self.INF/100
                elif(board.small_boards_status[1][i][j] == self.map_symbol[self.max_player ^ 1]):
                    cost[1][i][j] = -self.INF/100
                else:
                    cost[1][i][j] = self.computecost(board, self.max_player,1, i, j)
        
                       

        return (self.compute_for_bigboard(board, self.max_player, cost)+self.compute_for_bigboard2(board, self.max_player, cost))

    def compute_for_bigboard(self, board, player, cost):

        row = []
        
        row_tot = [0]*3
        for i in range(3):
            row.append([])
          

        total = 0

        for i in range(3):
            for j in range(3):
                row[i].append(board.small_boards_status[0][i][j])
                row_tot[i] += cost[0][i][j]
        for i in range(3):
            cntmx = row[i].count(self.map_symbol[player])
            cntmn = row[i].count(self.map_symbol[player ^ 1])
            cntemp = row[i].count('-')

            if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
                total += row_tot[i]
        col = []
        for i in  range(3):
            col.append([])
        col_tot = [0]*3

        for i in range(3):
            for j in range(3):
                col[j].append(board.small_boards_status[0][i][j])
                col_tot[j] += cost[0][i][j]

        

        for i in range(3):
            cntmx = col[i].count(self.map_symbol[player])
            cntmn = col[i].count(self.map_symbol[player ^ 1])
            cntemp = col[i].count('-')
            if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
                total += col_tot[i]

        diagonal1 = []
        diagonal2 = []
        d1_t = 0
        d2_t = 0
        for i in range(3):
            diagonal1.append(board.small_boards_status[0][i][i])
            diagonal2.append(board.small_boards_status[0][i][2-i])
        d1_t = cost[0][0][0] + cost[0][0][1] + cost[0][0][2]
        d2_t = cost[0][0][2] + cost[0][1][1] + cost[0][2][0]

        cntmn = diagonal1.count(self.map_symbol[player ^ 1])
        cntmx = diagonal1.count(self.map_symbol[player])
        if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
            total += d1_t
        cntmn = diagonal2.count(self.map_symbol[player ^ 1])
        cntmx = diagonal2.count(self.map_symbol[player])
        if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
            total += d2_t

        if (total == 0):
            for i in range(3):
                for j in range(3):
                    total += cost[0][i][j]
        return total

    def compute_for_bigboard2(self, board, player, cost):

        row = []
        row_tot = [0]*3
        for i in range(3):
            row.append([])

        total = 0

        for i in range(3):
            for j in range(3):
                row[i].append(board.small_boards_status[1][i][j])
                row_tot[i] += cost[1][i][j]
        col = []
        for i in range(3):
            col.append([])
        col_tot = [0]*3
        for i in range(3):
            for j in range(3):
                col[j].append(board.small_boards_status[1][i][j])
                col_tot[j] += cost[1][i][j]

        

        for i in range(3):
            cntmx = col[i].count(self.map_symbol[player])
            cntmn = col[i].count(self.map_symbol[player ^ 1])
            cntemp = col[i].count('-')
            if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
                total += col_tot[i]
        diagonal1 = []
        diagonal2 = []
        d1_t = 0
        d2_t = 0
        for i in range(3):
            diagonal1.append(board.small_boards_status[1][i][i])
            diagonal2.append(board.small_boards_status[1][i][2-i])
        d1_t = cost[1][0][0] + cost[1][0][1] + cost[1][0][2]
        d2_t = cost[1][0][2] + cost[1][1][1] + cost[1][2][0]

        cntmn = diagonal1.count(self.map_symbol[player ^ 1])
        cntmx = diagonal1.count(self.map_symbol[player])
        if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
            total += d1_t
        cntmn = diagonal2.count(self.map_symbol[player ^ 1])
        cntmx = diagonal2.count(self.map_symbol[player])
        if (cntmx+cntemp == 3 or cntmn+cntemp == 3):
            total += d2_t

        if (total == 0):
            for i in range(3):
                for j in range(3):
                    total += cost[1][i][j]
        return total

    def computecost(self, board, player, board_no, row_no, col_no):

        row = []
        for i in range(3):
            row.append([])
        
        total = 0
        for i in range(3*row_no, 3*row_no+3):
            for j in range(3*col_no, 3*col_no+3):
                row[i % 3].append(board.big_boards_status[board_no][i][j])

        for i in range(3):
            cntmx = row[i].count(self.map_symbol[player])
            cntmn = row[i].count(self.map_symbol[player ^ 1])
            if (cntmx > 0):
                if cntmn == 0:
                    total += self.inc_costs[cntmx]
            elif(cntmn > 0):
                if cntmx == 0:
                    total -= self.inc_costs[cntmn]

        col = []
        for i in range(3):
            col.append([])

        for i in range(3*row_no, 3*row_no+3):
            for j in range(3*col_no, 3*col_no+3):
                col[j % 3].append(board.big_boards_status[board_no][i][j]) 


        for i in range(3):
            cntmx = col[i].count(self.map_symbol[player])
            cntmn = col[i].count(self.map_symbol[player ^ 1])
            if (cntmx > 0 ):
                if cntmn == 0:
                    total += self.inc_costs[cntmx]
            elif (cntmn > 0):
                if cntmx == 0:
                    total -= self.inc_costs[cntmn]
        diagonal1 = []
        diagonal2 = []
        diagonal1.append(board.big_boards_status[board_no][3*row_no][3*col_no])
        diagonal1.append(
            board.big_boards_status[board_no][((3*row_no)+1)][((3*col_no)+1)])
        diagonal1.append(
            board.big_boards_status[board_no][((3*row_no)+2)][((3*col_no)+2)])
        cntmx = diagonal1.count(self.map_symbol[player])
        cntmn = diagonal1.count(self.map_symbol[(player ^ 1)])
        if (cntmx > 0 ):
            if cntmn == 0:
                total += self.inc_costs[cntmx]
        elif (cntmn > 0):
            if cntmx == 0:
                total -= (self.inc_costs[cntmn])
            

        diagonal2.append(
            board.big_boards_status[board_no][((3*row_no)+0)][((3*col_no)+2)])
        diagonal2.append(
            board.big_boards_status[board_no][((3*row_no)+1)][((3*col_no)+1)])
        diagonal2.append(
            board.big_boards_status[board_no][((3*row_no)+2)][((3*col_no)+0)])

        
        cntmn = 0
        cntmx = 0
        cntmx = diagonal2.count(self.map_symbol[player])
        cntmn = diagonal2.count(self.map_symbol[(player ^ 1)])
        if (cntmx > 0 ):
            if cntmn == 0:
                total += self.inc_costs[cntmx]
        elif (cntmn > 0):
            if cntmx == 0:
                total -= (self.inc_costs[cntmn])

        return total
