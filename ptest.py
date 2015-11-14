import sys
import time
from matchmatrix import *
sys.path.append("../methods/")
from psolve import psolve_sp

m=MatchMatrix()
m.test(sys.argv[1])
st=time.time()
w=psolve_sp(m.M, m.t)
toc=time.time()-st
print "Done in %.2f sec" % toc
outf="coef.csv"
print "Write to %s" % outf

fd = open(outf, "w")
fd.writelines("%i,%.4f\n" % (m.get_edge_id(i), v) for (i,v) in enumerate(w))
