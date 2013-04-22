#!/usr/bin/env python
# encoding: utf-8
"""
Here we will look at the disribution of alleles, new and old, among the different individuals presented in the indTable.txt to see how alleles are distributed.

Created by Måns Magnusson on 2011-03-30.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

def checkSpecies(acc):
	"""Check what kind of species we are looking at"""
	sampleType='unknown'
	indCode=acc
	if indCode[0] in ['z','m','H','p','L','r','B','T','F','P']:
		sampleType='Dog'
	elif indCode[0] == 'A':
		sampleType = 'Dingo'
	elif indCode[0] == 'K':
		if indCode[2] != 'n':
			sampleType='Dog'
		else:
			sampleType = 'Wolf'
	else:
		print acc
	return sampleType

def getInfo(inFile):
	"""Try to sort the info based on the different samples"""
	f 			= open(inFile,'r')
	g 			= open('../results/2011-11-02/allleInfo.txt','w')
	alleleDict 	= {}
	speciesDict ={'Dog':0,'Dingo':0,'Wolf':0}
	dingos		=[]
	dog			=0
	dingo		=0
	wolf		=0
	for line in f:
		line		=	line.rstrip().split()
		#words		=	line.split()
		if line[0]	!=	'nr':
			species		=	checkSpecies(line[1])
			speciesId	=	line[0]
			if species=='Dog':
				dog +=1
			elif species=='Dingo':
				dingo +=1
				dingos.append(speciesId)
			elif species=='Wolf':
				wolf +=1
			alleles=[line[3],line[4]]
			for allele in alleles:
				if allele != '-':
					if allele in alleleDict:
						if species != 'unknown':
							if alleleDict[allele][species] == 0:
								speciesDict[species]	+= 1
							alleleDict[allele][species]+=1
					else:
						if species != 'unknown':
							alleleDict[allele]={'Dog':0,'Wolf':0,'Dingo':0}
							alleleDict[allele][species] += 1
							if species in speciesDict:
								speciesDict[species] += 1
	f.close()
	print >>g,str(wolf)		+ ' Wolves with '+str(speciesDict['Wolf'])	+ ' alleles.' 
	print >>g,str(dingo)	+ ' Dingos with '+str(speciesDict['Dingo']) + ' alleles.' 
	print >>g,str(dog)		+ ' Dogs with '	 +str(speciesDict['Dog'])	+ ' alleles.' 
	g.close()
	print dingos
	return alleleDict

def main():
	inFile = '../results/2011-11-02/IndTable.txt'
	alleles = getInfo(inFile)
	g = open('../results/2011-11-02/allleInfo.txt','a')
	for allele,species in alleles.items():
		print >>g,allele,species
	g.close()


if __name__ == '__main__':
	main()

