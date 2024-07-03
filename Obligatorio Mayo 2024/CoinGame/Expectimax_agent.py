
from agent import Agent
from board import Board


class ExpectimaxAgent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def next_action(self, obs):
        best_action, _ = self.expectimax(obs, self.player, 4, float('-inf'), float('inf'))
        return best_action
    
    def heuristic_utility(self, board: Board):
        amountInRow = []
        for i in range(board.board_size[0]):
            amountInRow.append(board.grid[i].sum())
        
        nim_sum = 0
        for amount in amountInRow:
            nim_sum ^= amount
        return -1 if nim_sum == 0 else 1
        
    def expectimax(self, obs, player, depth, alpha, beta):
        ends, winner = obs.is_end(player)
        if ends:
            if winner == self.player:
                return None, 1
            elif winner == 2:
                return None, -1
            else:
                return None, 0

        if depth == 0:
            return None, self.heuristic_utility(obs)

        action_boards = []
        possible_actions = obs.get_possible_actions()
        for action in possible_actions:
            newBoard = obs.clone()
            newBoard.play(action)
            action_boards.append((action, newBoard))


        best_action = None

        if player != self.player:
            min_eval = float('inf')
            cantActions = action_boards.__len__()
            for action, next_board in action_boards:
                _, eval = self.expectimax(next_board, (player % 2) + 1, depth - 1, alpha, beta)
                if eval/cantActions < min_eval:   ##Uniform distribution
                    min_eval = eval/cantActions
                    best_action = action
                alpha = max(alpha, min_eval)
                if alpha >= beta:
                    break
            return best_action, min_eval
        else:
            
            max_eval = float('-inf')
            for action, next_board in action_boards:
                _, eval = self.expectimax(next_board, (player % 2) + 1, depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
                beta = min(beta, max_eval)
                if alpha >= beta:
                    break
            return best_action, max_eval