eclass QBlock(object):
    """docstring for QBlock"""
    def __init__(self, qdict={'N': 0, 'E': 0, 'S': 0, 'W': 0}, goodexit=False, badexit=False, _wall=False):
        self.QDict = qdict
        self.exitBlock = goodexit or badexit
        self.wall = _wall

        if self.wall:
            self.exitBlock,goodexit,badexit = False

        if goodexit:
        	self.R = 1
        elif badexit:
        	self.R = -1
        else:
        	self.R = 0
