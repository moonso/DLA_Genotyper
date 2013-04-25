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
from DLA_Genotyper.sequences import Sequences

class Fasta_Parser(object):
	"""Parse a fasta file"""
	def __init__(self, fasta_file):
		super(Fasta_Parser, self).__init__()
		self.ind_id = os.path.basename(fasta_file)[:-3]
		self.sequences = Sequences()
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
							self.sequences.add_sequence(seq_id, sequence)
							seq_id = line[1:]
							sequence = ""
						else: 
							sequence += line
			self.sequences.add_sequence(seq_id, sequence)
	
	def find_alleles(self):
		"""Find the alleles of this individual"""
		self.sequences.find_alleles()
	
	def get_sequences(self):
		"""Return the sequence obejct"""
		return self.sequences
	

def main():
	parser = argparse.ArgumentParser(description="Put the fasta files in a dictionar")
	parser.add_argument('fasta_file', type=str, nargs=1, help='Specify the the path to a fasta file containing sequences.')
	parser.add_argument('-write_alleles', '--write_alleles', type=str, nargs=1, help='Specify the path to a fastafile where we write the results.')
	args = parser.parse_args()
	infile = args.fasta_file[0]
	my_fasta_sequences = Fasta_Parser(infile)
	my_fasta_sequences.find_alleles()
	if args.write_alleles:
		my_sequences.print_fasta(args.write_alleles[0], ind_id)

if __name__ == '__main__':
	main()

