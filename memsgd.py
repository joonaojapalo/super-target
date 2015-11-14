"""
	Model entropy minimizing sgd learner
"""

import time
import numpy as np

from matchmatrix import *


def sgd_solve(matchmatrix, n_iter=5, alpha=0.999, beta=0.001):
	M = matchmatrix.M
	t = matchmatrix.t
	N = matchmatrix.N
	w = np.ones(matchmatrix.K)
	A = np.ones(matchmatrix.K)
	s = np.zeros(matchmatrix.K)
	nablaE_D = np.zeros(matchmatrix.K)
	eta = 0.01
	alpha = alpha
	beta = beta
	tau0 = 10
	kappa = 0.5 # see Murphy, Machine Learning - probabilistic approach p. 263
	
	tic = time.time()
	for i in xrange(n_iter):
		eta = pow(tau0 + i, -kappa)
		
		# get random row index
		r = np.random.randint(N)
		
		In = M[r].nonzero()[1]
		
		# compute LMS gradient
		y = M[r].dot(w)[0]
		nablaE_D[In] = (y - t[r])
		
		# compute MEM gradient
		c = t[r] / y
#		A[:] = (y - w) / (y**2)
#		B = (w[In] * (c/M[r].data - 1)).sum()
		
		# update model parameters
		w[:] -= + eta * alpha * nablaE_D		# LMS term
#		w[:] -= + eta * beta * t[r] * B * A		# MEM term
#		w[In] -= - eta * beta * B * M[r].data
		
		
		# project negative values to zero
#		w[w<0] = 0.0
		
		# reset gradient vector
		nablaE_D[In] = 0
		if time.time() - tic > 1.0:
			print i, eta, abs(w).sum(), ((M.dot(w)-t)**2).mean()
			tic = time.time()
	
	print 
	return w


m = MatchMatrix()

if __name__ == "__main__":
	m.test20k()
	
	print "Solving..."
	w = sgd_solve(m)
	print w
