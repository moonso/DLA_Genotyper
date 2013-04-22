#!/usr/bin/env python
# encoding: utf-8
"""
countIdentical.py

Count the number of unique reads in a fasta file.

'-' should count as a wild card?

Created by Måns Magnusson on 2012-05-21.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import glob
import numpy as np
#import matplotlib.pyplot as plt

class Individual:
	"""Individual holds some information about the uniqueness of reads of an individualself."""
	def __init__(self, file_name):
		self.seq_ids			= {}
		seq_id					= ""
		sequence				= ""
		j						= 0
		for line in open(file_name,'r'):
			line=line.rstrip()
			if len(line)>0:
				if line[0] == ">":
					if j != 0:
						if seq_id != 'ref':
							self.seq_ids[seq_id]	= sequence
						seq_id		= line[1:]
						sequence 	= ''
					elif j == 0:
						seq_id		= line[1:]
						j+=1
				elif line[0] != ">":
					sequence	+=line
		if seq_id != 'ref':
			self.seq_ids[seq_id]	= sequence
		self.nr_of_seq			= len(self.seq_ids)
		if self.nr_of_seq == 0:
			self.nr_of_seq	= 1
		self.nr_of_unique_seq	= 0
		self.fraq_of_unique_seq	= 0
	
	def check_unique(self):
		"""Chec how many of the sequences in this individual that are unique."""
		temp_seq		= self.seq_ids
		sequences		= self.seq_ids.values()
		nr_of_unique	= 0
		for ids, seq in temp_seq.items():
			sequences	= self.seq_ids
			del sequences[ids]
			sequences	= sequences.values()
			unique		= True
			for seq2 in sequences:
				if self.compare_strings(seq,seq2):
					unique = False
					break
			if unique:
				nr_of_unique += 1	
		self.nr_of_unique 		= nr_of_unique
		self.fraq_of_unique_seq	= self.nr_of_unique/self.nr_of_seq 
	
	def compare_strings(self,seq1,seq2):
		"""Compares two seuences of the same length. Return True if they are the same, with the exception that '-' can match anything, and False otherwise."""
		if len(seq1) != len(seq2):
			return False
		for i in range(len(seq1)):
			if seq1[i] != '-':
				if seq2[i] != '-':
					if seq1[i] != seq2[i]:
						return False
		return True
	

def main():
	path_indata = sys.argv[1]
	outfile		= sys.argv[2]
	uniques		= []
	for in_file in glob.glob(os.path.join(path_indata,'*.*')):
		if os.path.getsize(in_file) > 0:
			myInd	= Individual(in_file)
			#myInd.check_unique()
			#uniques.append(myInd.fraq_of_unique_seq)
			uniques.append(myInd.nr_of_seq)
	f			= open(outfile,'w')
	for obj in uniques:
		print >>f, obj
	f.close()
	#for key, value in myInd.sequences.items():
	#	print key, value
	#myInd.check_unique()
	#print 'Nr of Seq: ',myInd.nr_of_seq 
	#print 'Nr of unique: ',myInd.nr_of_unique 
	#print 'Fraction of unique: ',myInd.fraq_of_unique_seq 


if __name__ == '__main__':
	main()

