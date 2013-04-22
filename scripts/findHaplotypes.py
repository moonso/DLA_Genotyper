#!/usr/bin/env python
# encoding: utf-8
"""
findHaplotypes.py

Uses the classes individual and Sequences to find the haplotypes of all dogs.

Created by Måns Magnusson on 2012-06-13.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import argparse
import Individual
import glob
import math
import pickle
import matplotlib.pyplot as plt

def get_id(infile):
	"""Returns a string that is the id of a individual.
	Input: String with path to a file. 
	Output: The individuals number"""

	full_name	= os.path.basename(infile)
	new_id		= ""
	i			= 0
	while full_name[i] != ".":
		new_id	+= full_name[i]
		i		+= 1
	return new_id
	
def get_zygosity(samples, treshold = 0.25, sequence_nr_treshold = 20):
	"""Prints the number of hetero and homozygotes to screen."""
	hetero	= 0
	homo	= 0
	total	= 0
	for sample in samples:
		if sample.nr_of_seq >= sequence_nr_treshold:
			sample.get_zygosity(treshold)
			if sample.nr_of_var_positions > 0:
				hetero	+= 1
			else:
				homo	+= 1
			total += 1
	#out_file	= open('zygotes_' + str(sequence_nr_treshold)+'.txt', 'a')
	print "Total:", total
	print "Treshold:",treshold
	#out_file.write(str(treshold)+'\t')
	print 'Heterozygotes:', hetero
	#out_file.write(str(hetero)+'\t')
	print 'Homozygotes:', homo
	#out_file.write(str(homo)+'\n')
	#out_file.close()

def get_sequence_stats(samples):
	"""Prints some statistics of the number of sequences to the screen"""
	nr_of_samples 	= len(samples)
	seq				= []
	all_seq			= 0
	max_seq			= 0
	for sample in samples:
		seq.append(sample.nr_of_seq)
		all_seq	+= sample.nr_of_seq
		if sample.nr_of_seq > max_seq:
			max_seq = sample.nr_of_seq
	mean			= all_seq/nr_of_samples
	sd				= math.sqrt(sum((x-mean)**2 for x in seq)/nr_of_samples)
	print 'Number of samples:', nr_of_samples
	print 'Max number of seq:', max_seq
	print 'Mean number of seq:', mean
	print 'Stddev number of seq:', sd
	width			= 0.20
	x				= range(nr_of_samples)
	plt.bar(x,seq,width,color='b')
	plt.ylabel('Number of ind')
	plt.show()


def main():
	parser = argparse.ArgumentParser(
		prog="findHaplotypes",
		description='''Finds the alleles for individuals. Specify the path to a fasta file for an individual or to a directory with fasta files.''')
		
	parser.add_argument("sample",metavar="path/to/sample(s)",help="Use the file with a sample or directory of samples specified here.")
	parser.add_argument("-oa","--oldalleles",default='../../data/DogAndWolfRawOnlyWithTags.fa',help="Specify the path to the set of old alleles.")
	parser.add_argument("-o","--out",default="./",help="Path to outdir")
	parser.add_argument("-v","--verbosity",action="store_true",help="Show more output")
	parser.add_argument("-t","--treshold",type=float,default=0.25,help="Set the treshold for a variable position. Default = 0.25")
	parser.add_argument("-a", "--find_alleles", action="store_true", help="Find the alleles for the samples")
	parser.add_argument("-cs", "--count_sequences", action="store_true", help="Count the number of sequences for the input set.")
	parser.add_argument("-p", "--pickle_samples", action="store_true",help="Save the instances to the file specified after this flag.")
	parser.add_argument("-up", "--use_pickle", action="store_true", help="Use stored instances from the filename specified")
	parser.add_argument("-vp", "--make_variable_positions", action="store_true", help="Show the variable positions for this individual")
	args = parser.parse_args()
	old_alleles	= args.oldalleles
	path_outdata= args.out
	samples		= []
	if os.path.exists(args.sample):
		if args.use_pickle:
			samples	= pickle.load(open(args.sample,"rb"))
		else:
			if os.path.isdir(args.sample):
				print args.sample, 'is a directory!'
				path_indata = args.sample
				# ind_file holds the FASTA files of an individual
				for ind_file in glob.glob(os.path.join(path_indata,'*.*')):
					# If there are sequences in the file:
					if os.path.getsize(ind_file) > 0:
						individual = get_id(ind_file) # individual is the id of an individual
						if individual not in ['1054','2394','4537','806','4058']:
							# Sample is a list with all individual objects
							samples.append(Individual.Individual(ind_file,old_alleles,individual))
			elif os.path.isfile(args.sample):
				print args.sample, 'is a file!'
				individual 	= get_id(args.sample) # individual is the id of an individual
				print 'Indid: ',individual
				samples.append(Individual.Individual(args.sample,old_alleles,individual))
	else:
		print "Non existing path.", args.sample
		sys.exit()
		
	if args.pickle_samples:
		pickle.dump(samples, open(args.pickle_samples,"wb"))
	if args.find_alleles:
		out_file = open('all_alleles.fa','w')
		for sample in samples:
			sample.find_alleles()
			# sample.print_alleles()
			sample.print_alleles(out_file)
		out_file.close()
	if args.count_sequences:
		get_sequence_stats(samples)
	if args.verbosity:
		get_zygosity(samples,args.treshold)
	if args.make_variable_positions:
		for sample in samples:
			sample.find_variable_positions()
			


if __name__ == '__main__':
	main()

