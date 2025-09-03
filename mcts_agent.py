from random import random
import minimax_agent
import copy
import random
import math
import numpy as np

class Game():
    def __init__(self, num_rows, num_cols, inrow, player):
        self.rows = num_rows
        self.cols = num_cols
        self.inrow = inrow
        self.player = player

class State():
    def __init__(self, board, game, parent, player, heights = []):
        self.board = board
        self.rules = game
        self.parent = parent
        if parent==-1:
            self.parent = self
        self.children = []
        self.player = player
        self.total_score = 0
        self.visited = 0
        self.move = -1
        self.heights = heights
        if len(heights)==0:
            self.calculateHeights()

    def calculateHeights(self):
        for j in range(self.rules.cols):
            row = 0
            while row+1<self.rules.rows and self.board[row+1][j]==0:
                row+=1
            self.heights.append(row)

    def possibleMoves(self):
        moves = []
        for j in range(self.rules.cols):
            if self.board[0][j] == 0:
                moves.append(j)
        return moves
    
    def terminateState(self):
        #print("Terminate state")
        if minimax_agent.count_inrow(self.board, self.rules.cols, self.rules.rows, self.rules.inrow, self.rules.inrow, 2):
            return True, 1
        if minimax_agent.count_inrow(self.board, self.rules.cols, self.rules.rows, self.rules.inrow, self.rules.inrow, 1):
            return True, 0
        if len(self.possibleMoves())==0:
            return True, 0.2
        #print("false")
        #print(self.board)
        return False, None
    
    def simulateMove(self, col, player):
        if self.board[0][col]!=0:
            #print(f'Column {col} is full, unable to make the move')
            return
        self.move = col
        row = self.heights[col]
        self.board[row][col] = player
        self.heights[col] -=1
    
    def undoMove(self, col):
        self.heights[col] += 1
        self.board[self.heights[col]][col] = 0
    
    def findTerminateState(self):
        new_board = copy.deepcopy(self)
        player = copy.deepcopy(self.player)
        while 1:
            terminate, value = new_board.terminateState()
            if terminate:
                #print(self.board)
                #print(new_board.board)
                #print(value)
                return value
            
            #moves = new_board.possibleMoves()
            #random_move = random.randint(0, len(moves)-1)
            #new_board.simulateMove(moves[random_move], player)
            cols = new_board.possibleMoves()
            values = []
            for col in cols:
                new_board.simulateMove(col, player)
                val = minimax_agent.calc_value_2(new_board.board, self.rules.cols, self.rules.rows, self.rules.inrow, player)
                values.append(val)
                new_board.undoMove(col)
            min_value = min(values)
            if min_value<=0:
                values = [v-min_value + 1 for v in values]
            sum = 0
            for v in values:    sum+=v
            probabilities = [v/sum for v in values]
            x = np.random.choice(len(values), p=probabilities)
            #print(f'chose column {cols[x]} for player {player}')
            new_board.simulateMove(cols[x], player)
            #move = minimax_agent.one_move_lookahead(new_board.board, self.rules.cols, self.rules.rows, self.rules.inrow, player=player)
            #new_board.simulateMove(move, player)
            player = 3 - player
    
    def createChild(self, move):
        childState = State(copy.deepcopy(self.board), self.rules, self, 3-self.player, copy.deepcopy(self.heights))
        childState.simulateMove(move, self.player)

        self.children.append(childState)
    
    def isLeaf(self):
        return len(self.children) == 0


    def expand(self):
        moves = self.possibleMoves()
        if len(moves) == 0:
            return False
        for move in moves:
            self.createChild(move)
        return True

    def getValue(self, iteration, c = 1):
        if self.visited==0:
            return float('inf')
        return self.total_score*1.0/self.visited + c*math.sqrt((math.log(iteration))/self.visited)

    def getAverageScore(self):
        if self.visited==0:
            return float('inf')
        return self.total_score*1.0/self.visited

    



class MCTree():
    def __init__(self, root_board, game):
        self.root = State(root_board, game, -1, game.player)

    def selectChild(self, state, it):
        #print("selecting a child")
        if state.isLeaf():
            return None
        max_value = 0
        best_node = []
        for child in state.children:
            value = child.getValue(it)
            #print(f"child {child.move} has value {value}, {math.isinf(value)}")
            if value>max_value:
                max_value = value
                best_node = [child]
            elif value==max_value:
                best_node.append(child)

        x = random.randint(0, len(best_node)-1)
        return best_node[x]


    def selectLeaf(self, it):
        state = self.root
        while not state.isLeaf():
            state = self.selectChild(state, it)
        return state

    def expandLeaf(self, leaf):
        if leaf.expand():
            return self.selectChild(leaf, 0)
        return leaf


    def update(self, node, value):
        #print(f"dfs {node}")
        node.total_score += value
        node.visited += 1
        if node.parent == node:
            return
        self.update(node.parent, value)
        

    def iteration(self, it):
        #selection
        leaf = self.selectLeaf(it)
        #print(f'selected leaf {leaf.move}')
        #expansion
        child = self.expandLeaf(leaf)
        #print(f'child at random {child.move}')
        #rollout
        rollout_value = child.findTerminateState()
        #backpropagation
        self.update(child, rollout_value)

    
    def runSimulation(self, iterations = 100):
        for iteration in range(iterations):
            #print(f'iteration {iteration}')
            self.iteration(iteration)
            #print()
        
    
    def getBestMove(self):
        if self.root.isLeaf():
            return None
        max_value = 0
        best_node = []
        for child in self.root.children:
            value = child.getAverageScore()
            print(f"child {child.move}, value {value}")
            if value>max_value:
                max_value = value
                best_node = [child.move]
            elif value==max_value:
                best_node.append(child.move)
        x = random.randint(0, len(best_node)-1)
        return best_node[x]



def move(board, num_cols, num_rows, inrow, player=2):
    game = Game(num_rows, num_cols, inrow, player)
    mct = MCTree(board, game)
    mct.runSimulation()
    return mct.getBestMove()
        


