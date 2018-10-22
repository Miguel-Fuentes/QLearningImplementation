import QEnv as env

running = True
while (running):
	goodInput = True

	try:
		donutLoc = int(input("Enter the location of the Donut square: "))
		badLoc = int(input("Enter the location of the Forbidden square: "))
		wallLoc = int(input("Enter the location of the Wall square: "))
		if len(set([donutLoc,badLoc,wallLoc])) != 3:
			print("One of the locations was repeated")
			raise Exception()
		outputType = input("Enter the output type (either p or q): ")
		if outputType == 'q':
			qOfInterestLoc = int(input("Enter the location of the square you want q values of: "))
			if any(loc not in range(2,13) for loc in [donutLoc,badLoc,wallLoc,qOfInterestLoc]):
				print("One of the locations was not in the range [2,12]")
				raise Exception()
		elif outputType != 'p':
			print("Did not recognize output type")
			raise Exception()
		elif any(loc not in range(2,13) for loc in [donutLoc,badLoc,wallLoc]):
			print("One of the locations was not in the range [2,12]")
			raise Exception()
	except:
		print("Invalid input try again")
		goodInput = False

	if goodInput:
		print("Imagine we do some calculations here")
		anotherTrial = input("Tpye 'y' to do another trial with different locations and output type: ")
		if anotherTrial != 'y':
			running = False
