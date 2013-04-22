#!/usr/bin/env python
# encoding: utf-8
"""
checkAlleles.py

Take the alleles found in the individuals and create two dictionarys one on the form {<sequence> : alleleID} and one with {individualNr : [alleleId:s]}, also print to a file on the form:

nr	ID	Species	Type(homo/hetero)	Allele1		Allele2


This script alter the alleles in way in the way that we copy and paste the problematic poly-c region in the exon.

Created by Måns Magnusson on 2011-04-13.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

def getType(indId, individuals):
	"""Returns the sampletype of the individual"""
	sampleType='unknown'
	indCode=individuals[indId]
	if indCode[0] in ['z','m','H','p','L','r']:
		sampleType='Hair'
	elif indCode[0] in ['B','K','T']:
		if indCode[0:3] != 'Kan':
			sampleType='FTA'
		else:
			sampleType='not our'
	elif indCode[0] in ['P','A','F']:
		sampleType = 'not our'
	return sampleType

def get_seq(infile):
	"""Put all sequences in a dictionary on the form:{<seqId>:<sequence>}
	Input: A FASTA file with the sequences for an individual
	Output: A dictionary on the form {<seqId>:<sequence>}"""

	individualDict={}
	f=open(infile, 'r')
	seqId=""
	sequence=""
	j=0
	for line in f:
		line=line.rstrip()
		if len(line)>0:
			if line[0] == ">":
				if j != 0:
					individualDict[seqId]=sequence
					seqId=line[1:]
					sequence = ''
				elif j == 0:
					seqId=line[1:]
					j+=1
			elif line[0] != ">": 
				sequence+=line
	individualDict[seqId]=sequence
	f.close()
	return individualDict


def read_ids(fileName):
	"""Read a file with indNr and indId:s and put them in a dictionary on the form: <indNr>:<indId>"""
	indIds={}
	f=open(fileName,'r')
	i=1
	for line in f:
		line=line.rstrip()
		indIds[str(i)]=line
		i+=1
	f.close()
	return indIds

def addAlleles(alleleDict,alleles,newNr,knownAlleles):
	"""Adds the found alleles to a dictionary if they are new"""
	for allele in alleles:
		if allele not in alleleDict:
			alleleName = 'New'+str(newNr)
			alleleDict[allele] = alleleName
			newNr += 1
			g=open(knownAlleles,'a')
			g.write('>'+alleleName+"\n")
			g.write(allele+"\n")
			g.close()
		else: 
			print alleleDict[allele] 
	return alleleDict,newNr

def make_seq_dict(inFile):
	"""Puts the infiles in a dictionary with sequence as key and Id as value(we know that these sequences are unique)."""
	acc=''
	seq=''
	beg=1
	seqDict={}
	f = open(inFile,'r')
	for line in f:
		line = line.rstrip()
		if len(line)>0:
			if beg == 1:
				acc += line[1:]#Accession is here the allele ID
				beg = 0
			else:
				if line[0] == '>':
					seqDict[seq] = acc
					acc = line[1:]
					seq = ''
				else:
					seq = line
	seqDict[seq] = acc
	acc = line[1:]
	return seqDict

def getSeqId(idString):
	"""Returns the Id"""
	seqId=''
	i=0
	while idString[i] in ['0','1','2','3','4','5','6','7','8','9']:
		seqId += idString[i]
		i+=1
	return seqId

def make_ind_dict(foundAlleles):
	"""Sorts the info from a Fasta file on the form {<indId> : [<Alleleseqs>]
	Indata: A FASTA file with indnr. as acc, and alleleseq.
	Output: A dictionary on the form {<indId> : [<Allele1>(,<Allele2>)]"""
	
	individualDict	=	{}
	f				=	open(foundAlleles, 'r')
	seqId			=	""
	sequence		=	""
	beg 			=	 1
	for line in f:
		line=line.rstrip()
		if len(line) > 0:
			#Here we just deal with the case that we are in beg. in file:
			if beg == 1:
				oldacc = line.split()
				oldacc = oldacc[0][1:]
				beg = 0
			else:
				if line[0] == ">":
					acc = line.split()
					acc = acc[0][1:]
					if oldacc in individualDict:
							individualDict[oldacc].append(sequence)
					else:
						individualDict[oldacc]=[sequence]
					oldacc = acc
				else:
					sequence = line
					#sequence = sequence[0:144] + 'ACTCCCCCA' + sequence[153:262] + 'GAAATGTG'
					#print sequence[145:154]
		else:
			beg = 1
	if oldacc in individualDict:
		individualDict[oldacc].append(sequence)
	else:
		individualDict[oldacc]=[sequence]	
		f.close()
	return individualDict

def main():
	#Initializing
	#
	#These are the sequnces that we have generated from before:
	found_alleles	= '../results/2012-03-14/all_alleles.fa'
	#This is the new individual table: 
	out_file		= '../results/2012-03-14/ind_table.txt'
	#This is the known alleles from litterature:
	known_alleles 	= 'DogAndWolfRaw120314.fa'
	#Each rownr has an Id assigned to it
	individual_file	= '../data/indivID.txt' 
	f				= open(out_file,'w')
	print >>f, "nr".center(6), "Id".center(8), "Zygote".center(8), "Allele1".center(12), "Allele2".center(12), "Method".center(8), "NrOfSeq".center(10)
	#
	#
	#
	individuals = read_ids(individual_file)
	old_alleles = make_seq_dict(known_alleles)#Seq is key and id is value.
	new_nr = 1
	ind_dict = make_ind_dict(found_alleles)
	#
	#
	#
	for ind_id, alleles in ind_dict.items():
		for allele in alleles:
			if allele not in old_alleles:
				allele_name 		= 'New'+str(new_nr)
				old_alleles[allele] = allele_name
				new_nr 				+= 1
				g					= open(known_alleles,'a')
				g.write('>'+allele_name+"\n")
				g.write(allele+"\n")
				g.close() 
		getID			  = '../results/2012-03-04/sequences_aligned_noref/' + ind_id + '.fa'
		getIndDict		  = get_seq(getID) 
		sampleType 		  = getType(ind_id,individuals)
		if len(alleles) == 1:
			zygosity = 'Homo'
			allele1 = old_alleles[alleles[0]]
			allele2 = '-'
		else:
			zygosity = 'Hetero'
			allele1 = old_alleles[alleles[0]]
			allele2 = old_alleles[alleles[1]]
		
		print >>f, ind_id.center(6), individuals[ind_id].center(8), zygosity.center(8), allele1.center(12), allele2.center(12), sampleType.center(8), str(len(getIndDict)).center(10)
	f.close()


if __name__ == '__main__':
	main()

