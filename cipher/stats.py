# -*- coding: utf-8 -*-

from copy import deepcopy
from alphabet import default_alphabet

class Stats:
	
	def __init__(self, alphabet = default_alphabet):
		
		self.alphabet = alphabet
		self.alen = len(alphabet.a_string)
		self.reset()

	def reset(self):
		self.singlef = [0.0 for i in xrange(0, self.alen)]
		self.doublef = [[0.0 for i in xrange(0, self.alen)] for i in xrange(0, self.alen)]
		
	def load_singlef_from_file(self, filename):
		f = open(filename, "r")
		i = 0
		
		for line in f:
			line = unicode(line.strip(), "utf-8")

			if len(line) == 0: continue
			
			self.singlef[i] = float(line)
			
			i += 1
		
		self.compute_means()
			
	def load_doublef_from_file(self, filename):
	
		tmp = [[0.0 for i in xrange(0, self.alen)] for i in xrange(0, self.alen)]
		
		f = open(filename, "r")
		i = 0
		
		for line in f:
			line = unicode(line.strip(), "utf-8")

			if len(line) == 0: continue
			
			row = line.split()
			
			row = map(lambda x: float(x.strip()), row)

			tmp[i] = row
			
			i += 1
			
		for x in range(0, self.alen):
			for y in range(0, self.alen):
				self.doublef[x][y] = tmp[y][x]
		
		self.compute_means()
		
	def process_text(self, text):
		
		self.reset()
		
		tlen = len(text)
		
		single_count = 0.0
		double_count = 0.0
		
		for pos, char in enumerate(text):
		
			ci = self.alphabet.lookup(char)
			
			if ci == -1: continue
			
			self.singlef[ci] += 1.0
			single_count += 1.0
			
			if pos == tlen - 1: continue
			
			ci_n = self.alphabet.lookup(text[pos + 1])
			
			if(ci_n == -1): continue
			
			self.doublef[ci][ci_n] += 1.0
			double_count += 1.0
			
		self.singlef = map(lambda x: x / (single_count / 100.0), self.singlef)
		self.doublef = map(lambda x: map(lambda y: y / (double_count / 1000.0), x), self.doublef)
		self.compute_means()
		
		
		
	def clone(self):
	
		return deepcopy(self)
		
		
	def compute_means(self):
		ms = 0.0
		md = 0.0
		
		for i in xrange(0, self.alen):
			ms += self.singlef[i]
			
		for x in xrange(0, self.alen):
			for y in xrange(0, self.alen):
				md += self.doublef[x][y]
		
		ms /= float(self.alen)
		md /= float(self.alen**2.0)
		
		self.singlef_mean = ms
		self.doublef_mean = md
		
		devs = 0.0
		devd = 0.0
		
		for i in xrange(0, self.alen):
			devs += (self.singlef[i] - self.singlef_mean)**2.0
			
		for x in xrange(0, self.alen):
			for y in xrange(0, self.alen):
				devd += (self.doublef[x][y] - self.doublef_mean)**2.0

		devs = (devs / float(self.alen))**0.5
		devd = (devd / float(self.alen**2.0))**0.5
		
		self.singlef_stddev = devs
		self.doublef_stddev = devd

	def compute_difference(self, other):
	
		# this doesn't work so well -> broken
		'''factora = 0.0
		factorb = 0.0
		
		for i in xrange(0, self.alen):
			factora += abs(self.singlef[i] - other.singlef[i])**2.0
			
		for x in xrange(0, self.alen):
			for y in xrange(0, self.alen):
				factorb += abs((self.doublef[x][y] - other.doublef[x][y]) / 10.0)**2.0
		'''		
		#return factorb
		
		# compute pearson's sample linear correlation
		corrd = 0.0
		
		for x in xrange(0, self.alen):
			for y in xrange(0, self.alen):
				corrd += (self.doublef[x][y] - self.doublef_mean) * (other.doublef[x][y] - other.doublef_mean)
				
		corrd /= self.doublef_stddev * other.doublef_stddev * float(self.alen)**2.0
		
		
		corrs = 0.0
		
		for i in xrange(0, self.alen):
			corrs += (self.singlef[i] - self.singlef_mean) * (other.singlef[i] - other.singlef_mean)
				
		corrs /= self.singlef_stddev * other.singlef_stddev * float(self.alen)

		
		
		return (corrs + corrd) * 50
		
	def __str__(self):
	
		res = u""
		
		res += u"Single freq:\n|"
		
		for i, v in enumerate(self.singlef):
			res += u" %s %2.3f |" % (self.alphabet.a_string[i], v)
		
		res += u"\nDouble freq:\n"
		
		for x, row in enumerate(self.doublef):
			res += u"|"
			for y, item in enumerate(row):
				res += u" %s%s %2.3f |" % (self.alphabet.a_string[x], self.alphabet.a_string[y], item)
			
			res += u"\n"
			
		return res.encode("utf-8")