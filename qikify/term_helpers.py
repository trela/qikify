import curses 

class colors(object):
    def __init__(self):
        self.GREEN    = '\033[0;32m'
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        curses.setupterm()
        if curses.tigetnum("colors") != 256:
            self.disable()
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def outputPassFail(gnd):
    return 'Pass: '+GREEN+str(np.sum(gnd==1))+ENDCOLOR + ' Fail: '+RED+str(np.sum(gnd==0))+ENDCOLOR
