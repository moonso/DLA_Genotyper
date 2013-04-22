#!/usr/bin/env python
# encoding: utf-8
"""
fasta_parser.py

Class for make .fasta parsers. Creates sequence objects out of each line on the form {<seq_id>: sequence}

Created by Måns Magnusson on 2013-04-22.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import argparse
from DLA_Genotyper.sequence import sequence

class Fasta_Parser(object):
	"""Parse a fasta file"""
	def __init__(self, fasta_file):
		super(Fasta_Parser, self).__init__()
		self.sequences = {}
		with open(fasta_file, 'r') as f:
			seq_id = ""
			sequence = ""
			beginning = True
			for line in f:
				line = line.rstrip()
				if len(line)>0:
					if beginning:
						seq_id = line[1:]
						beginning = False
					else:
						if line[0] == ">":
							self.sequences[seq_id] = sequence
							seq_id = line[1:]
							sequence = ""
						else: 
							sequence += line
			self.seq_dict[seq_id] = sequence
	

def main():
	parser = argparse.ArgumentParser(description="Put the fasta files in a dictionar")
	parser.add_argument('fasta_file', type=str, nargs=1, help='Specify the the path to a fasta file containing sequences.')
	args = parser.parse_args()
	my_fasta_sequences = Fasta_Parser(args.fasta_file[0])

if __name__ == '__main__':
	main()

