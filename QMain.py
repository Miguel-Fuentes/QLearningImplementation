import QEnv as env

WIDTH = 4
HEIGHT = 3
LIVING_REWARD = -0.1
DISCOUNT_RATE = 0.5
LEARNING_RATE = 0.1
EPSILON = 0.1

dirArrows = {'n': '\u2191', 'e': '\u2192', 's': '\u2193', 'w': '\u2190', '':'', 'exit': 'exit'}

running = True
while running:
    goodInput = True

    try:
        donutLoc = int(input("Enter the location of the Donut square: "))
        badLoc = int(input("Enter the location of the Forbidden square: "))
        wallLoc = int(input("Enter the location of the Wall square: "))
        if len(set([donutLoc, badLoc, wallLoc])) != 3:
            print("One of the locations was repeated")
            raise Exception()
        outputType = input("Enter the output type (either p or q): ")
        if outputType == 'q':
            qOfInterestLoc = int(input("Enter the location of the square you want q values of: "))
            if any(loc not in range(2, WIDTH * HEIGHT + 1) for loc in [donutLoc, badLoc, wallLoc, qOfInterestLoc]):
                print("One of the locations was not in range")
                raise Exception()
        elif outputType != 'p':
            print("Did not recognize output type")
            raise Exception()
        elif any(loc not in range(2, WIDTH * HEIGHT + 1) for loc in [donutLoc, badLoc, wallLoc]):
            print("One of the locations was not in the range")
            raise Exception()
    except:
        print("Invalid input try again")
        goodInput = False

    if goodInput:
        currentEnv = env.QEnv(donutLoc, badLoc, wallLoc, WIDTH, HEIGHT, DISCOUNT_RATE, LEARNING_RATE, LIVING_REWARD,
                              EPSILON)
        currentEnv.learn()
        if outputType == 'p':
            for q in currentEnv.getQs():
                actionQ = float('-inf')
                policyChoice = ''
                for action, val in q[1].items():
                    if val > actionQ:
                        actionQ = val
                        policyChoice = action
                print(f'{q[0]}: {dirArrows[policyChoice]}')
        elif outputType == 'q':
            qOfInterest = currentEnv.getQs()[qOfInterestLoc - 1]
            print(f'Q values of location {qOfInterestLoc}')
            for act, val in qOfInterest[1].items():
                print(f'{dirArrows[act]}: {val}')
        anotherTrial = input("Tpye 'y' to do another trial with different locations and output type: ")
        if anotherTrial != 'y':
            running = False
