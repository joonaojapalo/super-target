import optparse
import time
from numpy import *
from collections import defaultdict



M	= defaultdict(dict)
Mr	= defaultdict(dict)

# funcs.
q = lambda k:[i for (i,v) in enumerate(M[:,k]) if v != 0]
z = lambda k,i,v:matrix([v if j==i else 0 for j in xrange(k)])
gi = lambda i,w:-2*(alpha*float(M[:,i].T * (t - M*w)) + beta*sum(M[q(i),i]-w[i]))
gpi = lambda i,w:matrix([2*alpha*float(M[:,i].T*(M[:,j])) + (2*beta*len(q(i)) if i == j else 0) for j in xrange(w.shape[0])]).T


M = matrix([[1, 1, 1],
        [0, 1, 1],
        [0, 0, 1],
        [0, 1, 1],
        [0, 1, 1],
        [0, 0, 1]])
t = matrix([[ 8.5 ],
        [ 6.25],
        [ 0.75],
        [ 5.5 ],
        [ 6.5 ],
        [ 1.5 ]])

alpha	= 0.8
beta	= 0.2
gamma	= 0.002
w = matrix(ones(3)).T

for j in xrange(500):
	w = w - gamma * 2 * sum(gi(k, w) * gpi(k, w) for k in xrange(len(w)))
	print "%i: %s" % (j, w.T)

