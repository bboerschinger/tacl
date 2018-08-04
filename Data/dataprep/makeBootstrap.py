# make bootstrap if stdin

import sys,random,time

if __name__=="__main__":
    n = int(sys.argv[1])
    lines = []
    for l in sys.stdin:
        lines.append(l.strip())
    random.seed(time.time())
    N = len(lines)-1
    for i in xrange(n):
        print lines[random.randint(0,N)]
