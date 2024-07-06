from board import Board
from agent import Agent
import random

class Minimax_agent(Agent):
    def __init__(self, player=1):
        super().__init__(player)


    def next_action(self, obs):
        best_action, _ = self.minimax(obs, self.player, 4, float('-inf'), float('inf'))
        return best_action

    def heuristic_utility(self, board: Board):
        return self.evaluate_board(board)

    def evaluate_board(self, board: Board):
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
            if row_sum == sum(row):
                nim_sum ^= row_sum
        return -nim_sum

    def max_in_row(self, board: Board):
        max_count = 0
        for row in board.grid:
            row_count = 0
            for cell in row:
                if cell == 0:
                    if row_count != 0:
                        max_count = max(row_count, max_count)
                        row_count = 0
                else:
                    row_count += 1
            if row_count == sum(row):
                max_count = max(row_count, max_count)
        return -max_count

    def single_stones(self, board: Board):
        single_count = 0
        for row in board.grid:
            row_count = 0
            for cell in row:
                if cell == 0:
                    if row_count != 0:
                        single_count += 1
                        row_count = 0
                else:
                    row_count += 1
            if row_count == sum(row):
                single_count = 1
        return -single_count

    def number_of_rows(self, board: Board):
        row_count = 0
        for row in board.grid:
            if len(row) > 0:
                row_count += 1
        return -row_count

    def empty_cells_sum(self, board: Board):
        return -board.grid.sum()

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
        action_boards = [(action, board.clone().play(action)) for action in possible_actions]

        best_action = None

        if player != self.player:
            min_eval = float('inf')
            for action, next_board in action_boards:
                _, eval = self.minimax(next_board, (player % 2) + 1, depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_action = action
                alpha = max(alpha, min_eval)
                if alpha >= beta:
                    break
            return best_action, min_eval
        else:
            max_eval = float('-inf')
            for action, next_board in action_boards:
                _, eval = self.minimax(next_board, (player % 2) + 1, depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
                beta = min(beta, max_eval)
                if alpha >= beta:
                    break
            return best_action, max_eval
