#!/usr/bin/env python
# encoding: utf-8
"""
sort_alleles.py

Created by Måns Magnusson on 2012-12-22.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os

def make_seq_dict(fasta_file):
	"""Put the sequences from a FASTA file in a dictionary"""
	seq_dict	= {}
	seq_id		= ""
	sequence	= ""
	beginning 	= True
	number_of_seq	= 0
	for line in open(fasta_file,'r'):
		if len(line)>1:
			line=line.rstrip()
			if beginning:
				seq_id		= line[1:]
				beginning	= False
			else:
				if line[0] == ">":
					seq_dict[sequence]		= seq_id
					seq_id					= line[1:]
					sequence 				= ''
					number_of_seq			+= 1
				elif line[0] != ">": 
					sequence				+=line
	seq_dict[sequence]		= seq_id
	print number_of_seq
	return seq_dict

def check_alleles(new_alleles, old_alleles):
	"""Check if the new alleles exist, else create a new one."""
	seq_dict	= {}
	for sequence in old_alleles:
		if sequence not in seq_dict:
			seq_dict[sequence] 	= 1
		else:
			seq_dict[sequence] += 1
	for sequence in new_alleles:
		if sequence not in seq_dict:
			seq_dict[sequence] 	= 1
		else:
			seq_dict[sequence] += 1
	return seq_dict

def main():
	known_seq_file	= sys.argv[1]
	new_seq_file	= sys.argv[2]
	old_alleles		= make_seq_dict(known_seq_file)
	new_alleles		= make_seq_dict(new_seq_file)
	all_alleles		= check_alleles(new_alleles, old_alleles)
	for key, value in all_alleles.items():
		print key
		print value
	print 'old_alleles:', str(len(old_alleles)), 'new_alleles:', str(len(new_alleles)), 'all_alleles:', str(len(all_alleles)),


if __name__ == '__main__':
	main()

