#!/usr/bin/env python
# encoding: utf-8
"""
checkEriksDogs.py

Created by Måns Magnusson on 2012-03-29.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os

def get_id(name):
	"""Returns the correct name."""
	first 	= name[0]
	name	= name[1:]
	while name[0] == '0':
		name = name[1:]
	newname = first+name
	return newname

def parse_eriks_hundar(infile):
	"""Lägg eriks hundar i något slags dictionary för att jämföra med våra.
	{<id>:[<zygosity>,<allel 1>,<allel 2>]}"""
	eriks_dict	= {}
	i			= 1
	for line in open(infile,'r'):
		if line[0]	!= '#':
			line 	= line.rstrip().split()
			hund	= get_id(line[0])
			zygos	= line[4]
			allel1	= line[5]
			if len(line) > 6:
				allel2	= line[6]
			else:
				allel2	= 'NA'
			eriks_dict[hund]=[zygos,allel1,allel2]
			i += 1
	return eriks_dict
	
def parse_our_dogs(infile):
	"""Kolla våra hundar på samma sätt"""
	our_dict	= {}
	i			= 1
	for line in open(infile,'r'):
		if line[0]	!= '#':
			line 	= line.rstrip().split()
			hund	= line[1]
			number	= line[0]
			zygos	= line[3]
			allel1	= line[4]
			allel2	= line[5]
			our_dict[hund]=[zygos,allel1,allel2,number]
			i += 1
	return our_dict

def print_dogs(eriks,ours,out):
	"""Print the dogs to a file."""
	f	= open(out,'w')
	f.write('#nr\t'.center(10)+'ID\t'.center(10)+'Erik1\t'.center(10)+'Our1\t'.center(10)+'Erik2\t'.center(10)+'Our2\n'.center(10))
	for ind,value in eriks.items():
		if ind in ours:
			our_info	= ours[ind]
			f.write(our_info[3].center(10) +'\t'+ ind.center(10)+'\t'+ value[1].center(10)+'\t'+ our_info[1].center(10)+'\t'+ value[2].center(10)+'\t'+ our_info[2].center(10)+'\n')
		else:
			f.write('-'.center(10) +'\t'+ ind.center(10)+'\t'+ value[1].center(10)+'\t'+ '-'.center(10) +'\t'+ value[2].center(10)+'\t'+ '-\t'.center(10)+ 'NOT IN OURS!' +'\n')
			print "Not found!,", ind
	f.close()

def main():
	eriks_hundar	= sys.argv[1]
	our_dogs		= sys.argv[2]
	outfile			= sys.argv[3]
	eriks			= parse_eriks_hundar(eriks_hundar)
	ours			= parse_our_dogs(our_dogs)
	#print eriks
	print_dogs(eriks,ours,outfile)


if __name__ == '__main__':
	main()

