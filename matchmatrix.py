import scipy.sparse as sp
import numpy as np

try:
	from sklearn.linear_model import SGDRegressor
except ImportError:
	from scikits.learn.linear_model import SGDRegressor

try:
	import filetools
	HAS_FILETOOLS = True
except ImportError:
	HAS_FILETOOLS = False


class MatchMatrix:
	def fromfile(self, path):
		""" read data from .match file
		"""
		data = filetools.read_data(path)
		print "File read: %i lines" % len(data)
		self.build_matrix(data)
	def test(self, fn="test.match"):
		M = []
		for r in open(fn):
			a=r.strip().split(",")
			M.append((313,int(a[1]),int(a[2]),(float(a[3]),float(a[4])),(float(a[5]),float(a[6])),float(a[7]),float(a[8]),[int(x,36) for x in a[9:]]))
		print "File read"
		self.build_matrix(M)
	def test20k(self):
		self.test("test20k.csv")
	def build_matrix(self, rawdata):
		""" build scipy.sparse matrix AND travel time vector from .match file data

			matchfilename   : str; path to .match file
		"""
		N = len(rawdata)
		s = set()
		for d in rawdata:
			s.update(d[7])
		K = len(s)
		self.I = dict((j, i) for (i, j) in enumerate(s))
		self.I_rev = dict((i, j) for (i, j) in enumerate(s))
		D = sp.dok_matrix((N, K))
		self.t = np.zeros(N)
		print "Empty %i x %i matrix created" % (N, K)
		
		for n,d in enumerate(rawdata):
			if len(d[7]) == 1:
				D[n,self.I[d[7][0]]] = 1# d[6] - d[5]
			else:
				D[n, self.I[d[7][0]]] = 1 # d[5]
				D[n, self.I[d[7][-1]]] = 1 # d[6]
				for eid in d[7][1:-1]:
					D[n, self.I[eid]] = 1.0
			self.t[n] = float(d[2] - d[1])
		print "DOK matrix built."
		
		self.M = sp.csr_matrix(D)
		print "DOK to CSR conversion done."
		self.N = N
		self.K = K
	
	def get_edge_id(self, k):
		return self.I_rev[k]
	
	def solve(self, n_iter=5):
		self.clf = SGDRegressor(fit_intercept=False, n_iter=1, warm_start=True)
		self.clf.fit(self.M, self.t)
		for i in xrange(n_iter):
			self.clf.fit(self.M, self.t, coef_init=self.clf.coef_)
			self.clf.coef_[self.clf.coef_<0] = 0
		self.w = self.clf.coef_
	
	def mare(self):
		r = self.M.dot(self.clf.coef_)
		return np.mean(abs((r / self.t) - 1))


