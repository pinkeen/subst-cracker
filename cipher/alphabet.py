# -*- coding: utf-8 -*-

''' !!! works only if python was compiled with UCS2 unicode !!! '''
uni_range = 0xFFFF

default_a_string = u"abcdefghijklmnopqrstuvwxyząćęłńóśżź "

class Alphabet:
	
	def __init__(self, a_string):
	
		self.a_string = a_string
		self.uni_lut = [-1 for i in xrange(0, uni_range)]
		
		for i in xrange(0, len(self.a_string)):
			self.uni_lut[ord(self.a_string[i])] = i
		
		'''self.uni_lut = {}
		for i in xrange(0, uni_range):
			c = unichr(i)
			self.uni_lut[c] = self.a_string.find(c)'''
	
	def lookup(self, uni_character):
		
		return self.uni_lut[ord(uni_character)]
		#return self.uni_lut[uni_character]
	
	
default_alphabet = Alphabet(default_a_string)