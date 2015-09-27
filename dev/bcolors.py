#A simple module which allows printing in colors

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def printGreen(str) :
    print(GREEN + str + ENDC)
def printBlue(str) :
    print(BLUE + str + ENDC)
def printWarning(str) :
    print(WARNING + str + ENDC)
def printFail(str) :
    print(FAIL + str + ENDC)
def printHeader(str) :
    print(HEADER + str + ENDC)
def printBold(str) :
    print(BOLD + str + ENDC)
def printUnderline(str) :
    print(UNDERLINE + str + ENDC)
