from abc import ABC, abstractmethod
from board import Board

class Agent(ABC):
    
    @abstractmethod
    def __init__(self, player):
        self.player = player
        self.board = (player % 2) + 1

    @abstractmethod
    def next_action(self, obs):
        (action,bestAction) = self.minimax(obs, 10, 1)
        return action
    
    @abstractmethod
    def heuristic_utility(self, board: Board):
        amountInRow = []
        for i in range(board.board_size[0]):
            amountInRow.append(board.grid[i].sum())

        binary = []
        binaryXor = 0
        for i in range(len(amountInRow)):
            binary.append(bin(amountInRow[i]))
            binaryXor = binaryXor ^ binary(amountInRow[i])
        

    def minimax(self, obs, depth=10, numberPlayer=1):
        if depth == 0 or obs.is_game_over():
            return self.heuristic_utility(obs)
        if (numberPlayer == 1):
            maxEval = -100000
            bestAction = None
            for action in obs.get_possible_actions():
                eval = self.minimax(obs.apply_action(action), depth - 1, numberPlayer*-1)
                if eval >= maxEval:
                    maxEval = eval
                    bestAction = action
            return (maxEval, bestAction)
        if (numberPlayer == -1):
            minEval = 100000
            bestAction = None
            minEval = 100000
            for action in obs.get_possible_actions():
                eval = self.minimax(obs.apply_action(action), depth - 1, numberPlayer*-1)
                if eval <= minEval:
                    minEval = eval
                    bestAction = action
            return (minEval, bestAction)