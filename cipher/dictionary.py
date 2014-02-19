# -*- coding: utf-8 -*-

import re

class Dictionary:
	
	def __init__(self, dictfile):
		
		self.res = []
		
		f = open(dictfile, "r")
		
		for line in f:
			line = unicode(line, "utf-8").strip()
			
			if len(line) > 0:
				nre = re.compile(r"([\.]|\s|\A)" + line + r"([\.\n\r]|\s|\Z)", re.UNICODE | re.IGNORECASE)
				self.res.append(nre)
			
		self.allcount = len(self.res)
			
			
	def count(self, text):
	
		count = 0
		for r in self.res:
			
			#if r.search(text):
			#	count += 1
			
			count += len(r.findall(text))
				
		return float(count)
			
			
			