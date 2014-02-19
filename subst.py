#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import cipher
from cipher.stats import Stats
from cipher.key import Key
from cipher.pool import Pool

		
if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage:", sys.argv[0], "<enc|dec> <key_filename>"
		print "Plaintext is lowercased."
		print "Characters not present in the alphabet aren't processed."
		sys.exit()

	txt = unicode(sys.stdin.read(), "utf-8")
	keyfile = sys.argv[2]
	
	key = Key()
	key.load_from_file(keyfile)

	if sys.argv[1] == "enc":
		pass
	elif sys.argv[1] == "dec":
		key.reverse()
	else:
		print "Unknown mode:", sys.argv[1]
		sys.exit()

	sys.stdout.write(key.encdec(txt).encode("utf-8"))


	
	
	
