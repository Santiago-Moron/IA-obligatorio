from agent import Agent
from board import Board


class Minimax_agent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def next_action(self, obs):
        evalAction = self.minimax(obs, 10, 1)
        print("Minimax result: ", evalAction)
        return evalAction[1]
    
    def heuristic_utility(self, board: Board):
        amountInRow = []
        for i in range(board.board_size[0]):
            amountInRow.append(board.grid[i].sum())

        binaryXor = 0
        for i in range(len(amountInRow)):
            binaryAmount = bin(amountInRow[i])[2:]
            binaryXor = binaryXor ^ int(binaryAmount)
            print(binaryXor)
        if (binaryXor % 2 == 1):
            return -1
        return 1
        
    def minimax(self, obs, depth=10, numberPlayer=1):
        if depth == 0:
            return [None, self.heuristic_utility(obs)]
        if (numberPlayer == 1):
            maxEval = -100000
            bestAction = obs.get_possible_actions()[0]
            for action in obs.get_possible_actions():
                [eval, action] = self.minimax(obs.apply_action(action), depth - 1, numberPlayer*-1)
                if eval >= maxEval:
                    maxEval = eval
                    bestAction = action
            return [maxEval, bestAction]
        if (numberPlayer == -1):
            minEval = 100000
            bestAction = obs.get_possible_actions()[0]
            minEval = 100000
            for action in obs.get_possible_actions():
                [eval, action] = self.minimax(obs.apply_action(action), depth - 1, numberPlayer*-1)
                if eval <= minEval:
                    minEval = eval
                    bestAction = action
            return [minEval, bestAction]