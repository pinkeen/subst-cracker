# -*- coding: utf-8 -*-

import random
import sys
from copy import deepcopy
from alphabet import default_alphabet

class Key:
	def __init__(self, alphabet = default_alphabet):

		self.alphabet = alphabet
		self.alen = len(alphabet.a_string)
		self.data = [i for i in xrange(0, self.alen)]
		
	def randomize(self):

		used = [False] * self.alen

		for i, letter in enumerate(self.alphabet.a_string):

			pos = random.randint(0, self.alen - 1)

			while used[pos]:
				pos = random.randint(0, self.alen - 1)

			used[pos] = True
			self.data[i] = pos
			
	def reverse(self):
	
		tmp = [0] * self.alen
		
		for a, b in enumerate(self.data):
			tmp[b] = a
			
		self.data = tmp
			
	def encdec(self, in_text):
	
		out_text = u""

		key = list(self.data)
		
		for i, char in enumerate(in_text):
			pos = self.alphabet.lookup(char)
			
			if pos == -1: 
				out_text += in_text[i]
				continue

			out_text += self.alphabet.a_string[key[pos]]

		return out_text
			
	def compute_naive(self, s_expected, s_observed):
		
		exp = [(a, b) for a, b in enumerate(s_expected.singlef)]
		obs = [(a, b) for a, b in enumerate(s_observed.singlef)]
		
		''' sort in descending order '''
		exp.sort(lambda x, y: int((y[1] - x[1]) * 1000.0))
		obs.sort(lambda x, y: int((y[1] - x[1]) * 1000.0))
		
		for i in xrange(0, self.alen):
		
			(exp_p, value) = exp[i]
			(obs_p, value) = obs[i]
			
			self.data[exp_p] = obs_p

	def save_to_file(self, filename):

		f = open(filename, "w")

		for ap, bp in enumerate(self.data):
			a = self.alphabet.a_string[ap]
			b = self.alphabet.a_string[bp]

			if a == u" ": a = "_"
			if b == u" ": b = "_"

			line =  u"%s -> %s\n" % (a, b)
			f.write(line.encode("utf-8"))

	def load_from_file(self, filename):
		f = open(filename, "r")

		for line in f:
			line = unicode(line, "utf-8")
			(a, b) = line.split(u"->")

			a = a.strip()
			b = b.strip()
			
			if a == u"_": a = " "
			if b == u"_": b = " "
			
			self.data[self.alphabet.lookup(a)] = self.alphabet.lookup(b)

	def swap_one(self, other, pos):

		a = self.data[pos]
		b = other.data[pos]

		''' we make a swap so there are no double occurences '''
		self.data[filter(lambda i: i[1] == b, enumerate(self.data))[0][0]] = a
		other.data[filter(lambda i: i[1] == a, enumerate(other.data))[0][0]] = b

		self.data[pos] = b
		other.data[pos] = a

	def crossover_broken(self, other):

		
		a = 0 
		b = int(((self.alen - 1) / 4.0))

		swap_len = random.randint(a, b)
		start_pos = random.randint(0, self.alen - swap_len)

		for pos in xrange(start_pos, start_pos + swap_len):
			self.swap_one(other, pos)
			
	def crossover(self, other):

		swap_len = int(float(self.alen) * 0.2)
		start_pos = random.randint(0, self.alen - swap_len)

		for pos in xrange(start_pos, start_pos + swap_len):
			tmp = self.data[pos]
			self.data[pos] = other.data[pos]
			other.data[pos] = tmp

	def smart_crossover(self, other, exp_freq, ciph_freq):
	
		C1 = self.smart_crossover_direction(other, exp_freq, ciph_freq, True)
		C2 = self.smart_crossover_direction(other, exp_freq, ciph_freq, False)
		
		self.data = C1
		other.data = C2
		
	def smart_crossover_direction(self, other, exp_freq, ciph_freq, forward):
	
		I = [-1 for i in xrange(0, self.alen)]
				
		if forward: rng = xrange(0, self.alen)
		else: rng = xrange(self.alen - 1, -1, -1)
		
		for i in rng:
			d1 = abs(ciph_freq[i] - exp_freq[self.data[i]])
			d2 = abs(ciph_freq[i] - exp_freq[other.data[i]])

			if d1 < d2: 
				char1 = self.data[i]
				char2 = other.data[i]
			else:
				char1 = other.data[i]
				char2 = self.data[i]
				
				
			''' if first char is already present 
			    then use the second one; in case
			    the second char is present leave
			    it as blank (==-1) '''
			if not char1 in I:
				I[i] = char1
			elif not char2 in I:
				I[i] = char2
				
		missing = []
		
		for i in xrange(0, self.alen):
			if not i in I: missing.append(i)

		''' fill in the missing pieces '''
		for i in xrange(0, self.alen): 
			if I[i] == -1:
				''' find the best match '''
				minm = missing[0]
				mind = 123456789
				
				for m in missing:
					d = abs(ciph_freq[i] - exp_freq[m])
					if d < mind:
						mind = d
						minm = m
						
				I[i] = minm
				missing.remove(minm)
			

		return I
  

	def shuffle(self, swap_count = 1):
	
		for i in xrange(0, swap_count):
			a = random.randint(1, self.alen) - 1
			b = random.randint(1, self.alen) - 1
			
			tmp = self.data[a]
			
			self.data[a] = self.data[b]
			self.data[b] = tmp
			
	def shuffle_short(self, swap_count = 1):
	
		for i in xrange(0, swap_count):
			a = random.randint(1, self.alen) - 1
			b = a + 1
			b = b % self.alen
						
			tmp = self.data[a]
			
			self.data[a] = self.data[b]
			self.data[b] = tmp

			
	def compare(self, other):
		
		count = 0
		for i in xrange(0, self.alen):
			if self.data[i] == other.data[i]: count += 1
			
		return count
	
			
	def clone(self):
	
		n = Key(self.alphabet)
		n.data = list(self.data)
		return n


	def __str__(self):

		res = u"|"

		for ap, bp in enumerate(self.data):
			res += u" %s -> %s |" % (self.alphabet.a_string[ap], self.alphabet.a_string[bp])
		
		return res.encode("utf-8")


	
	
