#! /usr/bin/env python

usage = """bootstrap-sample.py OPTIONS [< goldfile]

  (c) Mark Johnson, 28th September 2013

bootstrap-sample.py creates a bootstrap sample from goldfile
by sampling from its lines
"""

import optparse, random, sys

def read_lines(inf):
    return inf.read().strip().split('\n')

def sample(xs):
    n = len(xs)
    for i in xrange(n):
        print random.choice(xs)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s", "--seed", dest="seed", type="int", default="0",
                      help="random number seed")
    parser.add_option("-n", "--nsamples", dest="nsamples", type="int", default="1",
                      help="number of bootstrap resamples to generate")
    (options, args) = parser.parse_args()

    if options.seed != 0:
        random.seed(options.seed)

    if args == 0:
        lines = read_lines(sys.stdin)
    else:
        lines = read_lines(file(args[0], "rU"))
    print options.nsamples
    for i in xrange(options.nsamples):
        if i > 0:
            print
        sample(lines)
