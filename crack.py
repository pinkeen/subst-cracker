#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import cipher
from cipher.stats import Stats
from cipher.key import Key
from cipher.pool import Pool

if __name__ == "__main__":

	if len(sys.argv) != 1:
		print "Just supply utf-8 ciphertext to stdin! No parameters expected."
		sys.exit()
		
	print "Hit CTRL+C (SIGINT) to halt early"
	
	ciphertext = unicode(sys.stdin.read(), "utf-8").lower()
	pool = Pool(ciphertext, ("single_stats_pl.txt", "double_stats_pl.txt"), max_pop = 14, stat_file = "test_stats.txt", naive_key = False, dict_file = "dict.txt")
	
	gkeys = pool.era(2000)

	print '-' * 50
	
	print "All keys:"
	
	for i, key in enumerate(gkeys):
		rkey = key.clone()
		rkey.reverse()
		print "\n\n", '(%02d/%02d)' % ((i + 1), len(gkeys)), '-' * 50
		print "Key:\n", rkey
		print "Deciphered:\n", key.encdec(ciphertext).encode("utf-8")
		

	
	
	
