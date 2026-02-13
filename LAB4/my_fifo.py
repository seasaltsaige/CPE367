#!/usr/bin/env python

############################################
# this EMPTY python fifo class was written by dr fred depiero at cal poly
# distribution is unrestricted provided it is without charge and includes attribution

import sys
import json

class my_fifo:
	
	
	############################################
	# constructor for signal history object
	def __init__(self,buff_len):
			
		self.buff_len = buff_len
		self.buff = []
		for k in range(buff_len): self.buff.append(0)
		# initialize more stuff, as needed	
	
	 
	############################################
	# update history with newest input and advance head / tail
	def update(self,current_in):
		
		# Pop oldest value
		self.buff.pop(0)
		# Apped new value at end
		self.buff.append(current_in)
		
		return True

	

	############################################
	# get value from the recent history, specified by age_indx
	def get(self,age_indx):

		# Newest value lives at M - 1
		# Oldest value lives at 0
		# Getting newest index should get M - 1, when age_indx = 0
		val = self.buff[self.buff_len - age_indx - 1]
		
		return val