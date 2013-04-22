#!/usr/bin/env python
# encoding: utf-8
"""
parse_alleles.py

Look at how the alleles are distributed, how many there are, how many where found in one etc...


Created by Måns Magnusson on 2012-07-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os

def make_sequence_dict(sequences):
	"""Put all the sequences in a sequence dict."""
	seq_dict			= {}
	for line in open(sequences,'r'):
		line=line.rstrip()
		if len(line)>0:
			if line[0] != ">":
				sequence	= line
				if sequence in seq_dict:
					seq_dict[sequence]	+= 1
				else:
					seq_dict[sequence]	= 1
	return seq_dict

def check_frequencies(seq_dict):
	"""Check the frequencies of the alleles."""
	freq_dict	= {}
	for seqs, number in seq_dict.items():
		if number in freq_dict:
			freq_dict[number] += 1
		else:
			freq_dict[number]  = 1
	for number, freq in freq_dict.items():
		print number, freq

def check_with_known(unknown, known):
	"""Check how many of the new alleles that where known"""
	new 	= 0
	for seq in unknown:
		if seq not in known:
			new += 1
	print 'New alleles:', new

def main():
	alleles		= sys.argv[1]
	known		= sys.argv[2]
	sequences	= make_sequence_dict(alleles)
	known		= make_sequence_dict(known)
	check_with_known(sequences, known)
	check_frequencies(sequences)
	print 'Number of alleles: ', len(sequences)


if __name__ == '__main__':
	main()

