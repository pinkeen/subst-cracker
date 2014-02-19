# -*- coding: utf-8 -*-

from key import Key
from stats import Stats
from dictionary import Dictionary
from alphabet import default_alphabet

import random
import datetime
import signal
import sys

default_params = {}
default_params["mutation_swap_count"] = 1
default_params["mutations_percent"] = 40
default_params["crossover_percent"] = 50

''' max_pop must be an even number ! '''

class Pool:

	def signal_handler(self, signal, frame):
		self.end = True
		print 'You pressed Ctrl+C!'
		

	def __init__(self, ciphertext, stats_filenames, dict_file, max_pop = 10, params = default_params, alphabet = default_alphabet, stat_file = None, naive_key = True):
	
		self.params = params
		self.alphabet = alphabet
		self.single_stats_filename, self.double_stats_filename = stats_filenames
		self.ciphertext = ciphertext
		self.max_pop = max_pop
		
		self.exp_stats = Stats(self.alphabet)
		self.exp_stats.load_singlef_from_file(self.single_stats_filename)
		self.exp_stats.load_doublef_from_file(self.double_stats_filename)

		self.ciph_stats = Stats(self.alphabet)
		self.ciph_stats.process_text(self.ciphertext)
		
		self.initialize(naive_key)
		self.stat_file = None
				
		if stat_file != None:
			self.stat_file = open(stat_file, "w")
			self.stat_file.write("gen\tworst\tavg\tbest\tderiv\n")
			
		self.sliding_table = []
		self.end = False
		
		self.dictionary = Dictionary(dict_file)
		self.temp_stats = Stats(self.alphabet)
		
		signal.signal(signal.SIGINT, self.signal_handler)


	def compute_sliding_deriv(self, current_value, maxlen):
		
		self.sliding_table.append(current_value)
		
		slen = len(self.sliding_table)
		
		if slen > maxlen:
			self.sliding_table = self.sliding_table[slen - maxlen:]
			
		slen = len(self.sliding_table)
		
		return (self.sliding_table[slen - 1] - self.sliding_table[0]) / float(slen)  

	''' the smaller the better '''
	def get_fitness(self, key):
	
		deciphered = key.encdec(self.ciphertext)
		
		
		self.temp_stats.process_text(deciphered)
		
		#print deciphered.encode("utf-8")

		corr =  self.exp_stats.compute_difference(self.temp_stats)
		
		return corr
		#return self.dictionary.count(deciphered) / 100.0 + corr * 0.1
		
		
	def initialize(self, naive):

		self.keys = []
		
		naive_key = Key(self.alphabet)
		naive_key.compute_naive(self.exp_stats, self.ciph_stats)
		naive_key.reverse()
		
		for i in xrange(0, self.max_pop):
			if naive:
				new_key = naive_key.clone()
				new_key.shuffle(3)
			else:
				new_key = Key(self.alphabet)
				new_key.randomize()

			self.keys.append(new_key)
		
	def process_mutations(self):
	
		count = int((self.params["mutations_percent"] * len(self.keys)) / 100)
		maxp = len(self.keys) - 1
		
		for i in xrange(0, count):
			p = random.randint(0, maxp)
			n = self.keys[p].clone()
			n.shuffle(self.params["mutation_swap_count"])
			self.keys.append(n)
	
	def make_step(self):
	
		crossovers = int(self.params["crossover_percent"] * self.max_pop / 100)
		
		for i in xrange(0, crossovers):
			ai = int(round(random.triangular(0, self.max_pop - 1, 0)))
			bi = ai
			#ai = random.randint(0, self.max_pop - 1)
			#bi = ai
			
			while bi == ai:
				bi = int(round(random.triangular(0, self.max_pop - 1, 0)))
				
			nka = self.keys[ai].clone()
			nkb = self.keys[bi].clone()
			
			nka.smart_crossover(nkb, self.exp_stats.singlef, self.ciph_stats.singlef)
			
			self.keys.append(nka)
			self.keys.append(nkb)

		self.process_mutations()

		ranking = []
		
		for i in xrange(0, len(self.keys)):
			ranking.append((self.get_fitness(self.keys[i]), self.keys[i]))
			
		ranking.sort(reverse=True)
		
		worst_fitness = ranking[len(ranking) - 1][0]
		best_fitness = ranking[0][0]
		avg_fitness = reduce(lambda x, y: x + y[0], ranking, 0.0) / float(len(ranking))
		
		ranking = ranking[:self.max_pop]
		self.keys = map(lambda x: x[1], ranking)
		
		
		return (worst_fitness, avg_fitness, best_fitness)
		
		
	def era(self, steps):
	
		deriv_maxlen = 20
		
		t0 = datetime.datetime.now()

		print "Starting an era..."
		
		self.end = False
		
		i = 0
		while i <= steps and not self.end:
			i += 1
			
			(worst, avg, best) = self.make_step()

			if i == 0: sworst, savg, sbest = (worst, avg, best)

			deriv = self.compute_sliding_deriv(best, deriv_maxlen)
			
			if self.stat_file != None:
				self.stat_file.write("%04d\t%.4f\t%.4f\t%.4f\t%f\n" % (i + 1, worst, avg, best, deriv))
			
			print "Step %04d/%d worst/avg/best/best_speed: %.2f %.2f %.2f %f" % (i + 1, steps, worst, avg, best, deriv)
			
			print "Best decode: ", self.keys[0].encdec(self.ciphertext).encode("utf-8")
			
		delta_t = datetime.datetime.now() - t0 
		
		print "Time:", delta_t
		print "Time per step:", (delta_t.seconds + delta_t.microseconds / 1000000.0) / float(i + 1), "seconds"
			
		return self.keys
			
