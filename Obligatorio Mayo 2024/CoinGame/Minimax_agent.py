from board import Board
from agent import Agent
import random

class Minimax_agent(Agent):
    def __init__(self, player=1):
        super().__init__(player)

    def next_action(self, board):
        action, _ = self.minimax(board, self.player, 2, float('-inf'), float('inf'))
        return action

    def heuristic_utility(self, board):
        return self.nim_sum(board) + self.coinGroups(board)

    def nim_sum(self, board):
        nim_sum = 0
        for row in board.grid:
            row_sum = 0
            for cell in row:
                if cell == 0:
                    if row_sum != 0:
                        nim_sum ^= row_sum
                        row_sum = 0
                else:
                    row_sum += 1
        for row in board.grid:
            if row_sum == sum(row):
                nim_sum ^= row_sum
        return -nim_sum



    def coinGroups(self, board):
        count = 0
        for row in board.grid:
            row_count = 0
            for cell in row:
                if cell != 0:
                    row_count += 1
                else:
                    if row_count != 0:
                        count += 1
                        row_count = 0
            if row_count == sum(row):
                count = 1
        return -count

    def minimax(self, board, player, depth, alpha, beta):
        is_end, winner = board.is_end(player)
        if is_end:
            if winner == self.player:
                return None, 1
            elif winner == 2:
                return None, -1
            else:
                return None, 0
        if depth == 0:
            return None, self.heuristic_utility(board)
        
        possible_actions = board.get_possible_actions()
        actions_and_boards = []
        for action in possible_actions:
            new_board = board.clone()
            new_board.play(action)
            actions_and_boards.append((action, new_board))

        best_action = None
        if player != self.player:
            min_eval = float('inf')
            for action, new_board in actions_and_boards:
                _, eval = self.minimax(new_board, (player % 2) + 1, depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    act, _ = random.choice(actions_and_boards)
                    best_action = act
                alpha = max(alpha, min_eval)
                if alpha >= beta:
                    break
            return best_action, min_eval
        if player == self.player:
            max_eval = float('-inf')
            for action, new_board in actions_and_boards:
                _, eval = self.minimax(new_board, (player % 2) + 1, depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
                beta = min(beta, max_eval)
                if alpha >= beta:
                    break
            return best_action, max_eval
