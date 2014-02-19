#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import cipher
from cipher.stats import Stats
from cipher.key import Key
from cipher.pool import Pool

if __name__ == "__main__":
	
	ek = Key()
	ek.load_from_file("random_key.txt")
	
	plaintext = unicode(sys.stdin.read(), "utf-8").lower()
	ciphertext = ek.encdec(plaintext)
	
	pool = Pool(ciphertext, ("single_stats_pl.txt", "double_stats_pl.txt"), max_pop = 14, stat_file = "test_stats.txt", naive_key = False, dict_file = "dict.txt")
	
	gkeys = pool.era(100000)

	ek.reverse()
	for i, key in enumerate(gkeys):
		print "Key(%d): hit_count = %d" % (i, key.compare(ek))

	
	
	
