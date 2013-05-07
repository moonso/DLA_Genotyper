#!/usr/bin/env python
# encoding: utf-8
"""
see_length.py

Created by Måns Magnusson on 2013-05-06.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import argparse



def main():
	parser = argparse.ArgumentParser(description="Print the lengths of sequences to stdout.")
	parser.add_argument('fasta_file', type=str, nargs=1, help='Specify the the path to a fasta file containing sequences or a directory with fasta files.')
	args = parser.parse_args()
	my_length = 305
	with open(args.fasta_file[0], 'r') as f:
		for line in f:
			if line[0] != '>':
				if len(line) != my_length:
					print len(line)
	


if __name__ == '__main__':
	main()

