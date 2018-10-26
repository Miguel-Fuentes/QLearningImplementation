import QBlock as qb


class QEnv(object):
    """docstring for QEnv"""
    worldMap = list()

    def __init__(self, donut, forbidden, wall, _width, _height, discountrate, learningrate, livingreward, _epsilon):
        self.width = _width
        self.height = _height
        self.discountRate = discountrate
        self.learningRate = learningrate
        self.epsilon = _epsilon
        self.START_LOC = (0, 0)
        self.agentLoc = self.START_LOC

        self.worldMap = [[0 for j in range(_width)] for i in range(_height)]

        for i in range(self.height):
            for j in range(self.width):
                loc = (i * self.width + j) + 1
                if loc == donut:
                    self.worldMap[i][j] = (qb.QBlock(loc, livingreward, goodexit=True))
                elif loc == forbidden:
                    self.worldMap[i][j] = (qb.QBlock(loc, livingreward, badexit=True))
                elif loc == wall:
                    self.worldMap[i][j] = (qb.QBlock(loc, livingreward, _wall=True))
                else:
                    self.worldMap[i][j] = (qb.QBlock(loc, livingreward))

    def printMap(self):
        upsideDownDict = {0: 2, 1: 1, 2: 0}
        for i in range(self.height):
            for j in range(self.width):
                if upsideDownDict[i] == self.agentLoc[0] and j == self.agentLoc[1]:
                    print('A', end='')
                else:
                    print(self.worldMap[-(i + 1)][j], end='')
            print()

    def moveTest(self):
        moving = True
        while moving:
            self.printMap()
            movement = input("Enter Movement: ")
            if movement in ['n', 'e', 's', 'w']:
                self.agentLoc = self.move(movement)
            else:
                moving = False

    def move(self, action):
        loc = (0, 0)
        if action == 's':
            if self.agentLoc[0] == 0:
                return self.agentLoc
            else:
                loc = (self.agentLoc[0] - 1, self.agentLoc[1])
        elif action == 'e':
            if self.agentLoc[1] == self.width - 1:
                return self.agentLoc
            else:
                loc = (self.agentLoc[0], self.agentLoc[1] + 1)
        elif action == 'n':
            if self.agentLoc[0] == self.height - 1:
                return self.agentLoc
            else:
                loc = (self.agentLoc[0] + 1, self.agentLoc[1])
        elif action == 'w':
            if self.agentLoc[1] == 0:
                return self.agentLoc
            else:
                loc = (self.agentLoc[0], self.agentLoc[1] - 1)
        else:
            print('Invalid direction given to move function')

        if self.worldMap[loc[0]][loc[1]].isWall():
            return self.agentLoc
        else:
            return loc

    def getQs(self):
        Qs = list()
        for i in range(self.height):
            for j in range(self.width):
                Qs.append(((i * self.width + j + 1), self.worldMap[i][j].QDict))
        return Qs

    def learn(self):
        '''
        What has to happen

        Loop (maxiteration)
            1) pick action (epsilon change of picking a random action)

            2) figure out where that action takes you

            3) go there and update Q of the node where you came from

            4) if you hit an exit:
                a) Start Back over
                b) Check if Q has converged
                '''

        iterations = 0
        converged = False
        Qs = self.getQs()

        while iterations < 10000 and not converged:
            iterations += 1

            action = self.worldMap[self.agentLoc[0]][self.agentLoc[1]].chooseAction(self.epsilon)
            if action == 'exit':
                self.worldMap[self.agentLoc[0]][self.agentLoc[1]].QUpdateExit(self.learningRate)
                self.agentLoc = self.START_LOC
                '''                 
                if Qs == self.getQs():
                    converged = True
                    print('CONVERGED!!!')
                else:
                    Qs = self.getQs()'''

            else:
                nextNodeLoc = self.move(action)
                self.worldMap[self.agentLoc[0]][self.agentLoc[1]].QUpdate(action,
                                                                          self.worldMap[nextNodeLoc[0]][nextNodeLoc[1]],
                                                                          self.learningRate,
                                                                          self.discountRate)
                self.agentLoc = nextNodeLoc
