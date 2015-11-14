#!/usr/bin/python

import optparse
import time
from matchmatrix import *

options, args = optparse.OptionParser().parse_args()
out = open(args[1], "w")

m = MatchMatrix()
m.fromfile(args[0])
print "%s -- Solving %s" % (time.ctime(), args[0])
m.solve(n_iter=10)
print "%s -- MARE %.4f" % (time.ctime(), m.mare())
print "%s -- Writing to %s" % (time.ctime(), args[1])
out.writelines("%i,%f\n" % (m.get_edge_id(k), w) for k, w in enumerate(m.w))
