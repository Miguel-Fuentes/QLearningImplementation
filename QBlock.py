import random


class QBlock(object):
    """docstring for QBlock"""

    def __init__(self, nodeNumber, livingreward, goodexit=False, badexit=False, _wall=False):
        self.exitBlock = goodexit or badexit
        self.wall = _wall
        self.livingReward = livingreward
        self.id = nodeNumber

        if self.wall:
            self.exitBlock, goodexit, badexit = False, False, False

        if goodexit:
            self.QDict = {'exit': 0}
            self.RDict = {'exit': 100}
        elif badexit:
            self.QDict = {'exit': 0}
            self.RDict = {'exit': -100}
        elif _wall:
            self.QDict = {}
            self.RDict = {}
        else:
            self.QDict = {'n': 0, 'e': 0, 's': 0, 'w': 0}
            self.RDict = {'n': 0, 'e': 0, 's': 0, 'w': 0}

    def __repr__(self):
        if self.RDict == {'exit': -100}:
            return 'X'
        elif self.RDict == {'exit': 100}:
            return 'O'
        elif self.RDict == {}:
            return 'W'
        else:
            return 'N'

    def getID(self):
        return self.id

    def maxQ(self):
        maxQ = float('-inf')
        for _, val in self.QDict.items():
            if val > maxQ:
                maxQ = val
        return maxQ

    def R(self, action):
        try:
            return (self.RDict[action] + self.livingReward)
        except:
            print('Invalid action given to R function')

    def isWall(self):
        return self.wall

    def chooseAction(self, epsilon):
        chosenAction = 'error'
        if random.random() < epsilon:
            actions = list(self.QDict)
            chosenAction = random.choice(actions)
        else:
            actionQ = float('-inf')
            for action, val in self.QDict.items():
                if val > actionQ:
                    actionQ = val
                    chosenAction = action
        return chosenAction

    def QUpdate(self, action, nextNode, learningRate, discountRate):
        if action in self.QDict.keys():
            self.QDict[action] = round((1 - learningRate) * self.QDict[action] + learningRate * (
                    self.R(action) + discountRate * nextNode.maxQ()), 2)
        else:
            print("Invalid action passed to QUpdate")

    def QUpdateExit(self, learningRate):
        self.QDict['exit'] = round((1 - learningRate) * self.QDict['exit'] + learningRate * self.RDict['exit'], 2)
