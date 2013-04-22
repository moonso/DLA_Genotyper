#!/usr/bin/env python
# encoding: utf-8
"""
parse_ind_table.py

Reads a ind_table file, and counts the frequencies of each alleles.

Created by Måns Magnusson on 2012-03-17.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
from operator import itemgetter

def checkSpecies(acc):
	"""Check what kind of species we are looking at"""
	sampleType='unknown'
	indCode=acc
	if indCode[0] in ['z','m','H','p','L','r','B','T','F','P']:
		sampleType='Dog'
	elif indCode[0] == 'A':
		sampleType = 'Austr'
	elif indCode[0] == 'K':
		if indCode[2] != 'n':
			sampleType='Dog'
		else:
			sampleType = 'Wolf'
	else:
		print acc
	return sampleType


def main():
	ind_table	=	sys.argv[1]
	new_table	=	sys.argv[2]
	alleles		=	{}
	individuals	=	{}
	size		=	10
	total		=	0
	start		=	True	
	for line in open(ind_table,'r'):
		line					= line.rstrip().split()
		if start:
			start_line	= line
			start		= False
		else:
			if line[5]	== 'not':
				line.remove('our')
				line[5]	= 'not our'			
			individuals[line[0]]	= line[1:]
			ind_alleles				= [line[3],line[4]]
			for allele in ind_alleles:
				if allele != '-':
					total += 1
					if allele in alleles:
						alleles[allele]	+= 1
					else:
						alleles[allele] = 1
	start_line.insert(2, 'Species')
	start_line.insert(6,'AlleleFreq')
	f	= open(new_table,'w')
	for i in start_line:
		f.write(i.center(size)+'\t')
	f.write('\n')
	for ind in sorted(individuals.keys()):
		info	= individuals[ind]
		freq	= str(alleles[info[2]])
		if info[3] != '-':
			freq	+= (', ' + str(alleles[info[3]]))
		info.insert(1,checkSpecies(info[0]))
		info.insert(5,freq)
		print info
		f.write(ind.center(size)+'\t')
		for i in info:
			f.write(i.center(size)+'\t')
		f.write('\n')
	f.close()	
				
	#for allele_tuple in sorted(alleles.items(), key=itemgetter(1)):
	#	print allele_tuple[0], int(allele_tuple[1])/total
	#print total
	#for allele, value in alleles.items():
	#	print allele, value
			


if __name__ == '__main__':
	main()

