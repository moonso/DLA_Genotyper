#!/usr/bin/env python
# encoding: utf-8
"""
Sequences.py

This is a class that will have info and methods for dealing with sequences.
The primary function is to store the sequences, this is done in a dictionary called seq_dict.

Created by Måns Magnusson on 2012-03-10.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import glob

class Sequences:
	"""Alleles holds information about the allele candidates found in a set of sequences."""
	def __init__(self, sequences, mode = 'file'):
		self.seq_dict			= {}
		if mode == 'file':
			seq_id						= ""
			sequence					= ""
			beginning 					= True
			for line in open(sequences,'r'):
				line=line.rstrip()
				if len(line)>0:
					if beginning:
						seq_id		= line[1:]
						beginning	= False
					else:
						if line[0] == ">":
							self.seq_dict[seq_id]	= sequence
							seq_id					= line[1:]
							sequence 				= ''
						elif line[0] != ">": 
							sequence				+=line
			self.seq_dict[seq_id]		= sequence
		elif mode == 'dict':
			self.seq_dict			= sequences
		self.nr_of_seq				= len(self.seq_dict)
		self.frequence_dict			= {}
		self.variable_positions		= {}
		self.sequences_sorted		= {}
		self.consensus				= '' # The consensus sequence of the sequences in this object
		self.make_frequencies()
	
	def make_frequencies(self):
		"""Make a dictionary with the frequencies of each position"""
		pos_dict			= {}
		for ids, seq in self.seq_dict.items():
			i = 1
			for nucleotide in seq:
				if i in pos_dict:
					pos_dict[i][nucleotide] += 1
				else:
					if nucleotide in ['A','a']:
						pos_dict[i] = {'A':1,'C':0,'G':0,'T':0,'-':0,'N':0}
					elif nucleotide in ['C','c']:
						pos_dict[i] = {'A':0,'C':1,'G':0,'T':0,'-':0,'N':0}
					elif nucleotide in ['G','g']:
						pos_dict[i] = {'A':0,'C':0,'G':1,'T':0,'-':0,'N':0}
					elif nucleotide in ['T','t']:
						pos_dict[i] = {'A':0,'C':0,'G':0,'T':1,'-':0,'N':0}
					elif nucleotide in ['-','N','n']:
						pos_dict[i] = {'A':0,'C':0,'G':0,'T':0,'-':1,'N':0}
				i += 1
		for pos,values in pos_dict.items():
			# To avoid division with zero:
			if self.nr_of_seq == 0:
				self.nr_of_seq	= 1
			A	= values['A']/self.nr_of_seq
			C	= values['C']/self.nr_of_seq
			G	= values['G']/self.nr_of_seq
			T	= values['T']/self.nr_of_seq
			N	= (values['N'] + values['-'])/self.nr_of_seq
			self.frequence_dict[pos]=[A,C,G,T,N]
	
	def indel_position(self,position):
		"""Returns a boolean depending on if the position has alot of indels or if the two positions surrounding the present have alot of indels.
		Input: A dictionary with freq for each position
		Output: A boolean depending on if the positions are variable"""
		
		indel_position	= False
		for i in range(position-1,position+2):
			if self.frequence_dict[i][4] > 0.1: #If more than 10% of sequences have indel in any position around.
				indel_position = True
		return indel_position
	
	def make_seq_dict(self, seq_ids):
		"""Make a sequence dict from the sequence ids in a list."""
		seq_dict	= {}
		for sequence_id in seq_ids:
			seq_dict[sequence_id]	= self.seq_dict[sequence_id]
		return seq_dict
	
	def get_variants(self, frequency, var_pos_treshold):
		"""Returns a string with the nucloetides, eg. 'AC'"""
		variants	= ''
		if frequency[0] > var_pos_treshold:
			variants	+= 'A'
		if frequency[1] > var_pos_treshold:
			variants	+= 'C'
		if frequency[2] > var_pos_treshold:
			variants	+= 'G'
		if frequency[3] > var_pos_treshold:
			variants	+= 'T'
		return variants
	
	def find_variable_positions(self,var_pos_treshold):
		"""Picks out the variable positions, based on the frequence of the positions in one individual."""
		for pos,dist in self.frequence_dict.items():
		#We look at the second max so we can see if there is distribution
		#between more than one nucleotide.
			if len(self.variable_positions) < 21:
				if pos > 30 and pos < 270:# Avoid looking at the tags
					if not self.indel_position(pos):
						variants	= self.get_variants(dist, var_pos_treshold)#Variants is a string with the two bases.
						second_max	= sorted(dist[:4])[2]
						if second_max > var_pos_treshold:
							#print second_max, self.var_pos_treshold, pos
							self.variable_positions[pos] = variants
	
	def sort_sequences(self, variable_position=0):
		"""Divide the sequences into TWO groups based on the first variable position, or the position sent to sort sequences. Returns a list with two Sequence objects"""
		groups	= []
		if len(self.variable_positions) == 0:
			groups.append(self.seq_dict)
			groups.append(self.seq_dict)
		else:
			sorted_positions	= sorted(self.variable_positions.keys())
			position_number = sorted_positions[0]
			for seq in self.seq_dict:
				tag	= self.seq_dict[seq][position_number-1]
				if tag in self.sequences_sorted:
					self.sequences_sorted[tag].append(seq)
				else:
					self.sequences_sorted[tag]=[seq]
		for tag, sequences in self.sequences_sorted.items():
		 	groups.append(self.make_seq_dict(sequences))
		return groups
	
	def make_consensus(self):
		"""Make the consensus sequence of self.sequences. If there are less than 10% of information for a position we let that one be unknown(insert -)."""
		if len(self.frequence_dict) == 0:
			self.make_frequencies()
		for pos, frequencies in self.frequence_dict.items():
			position	= 0
			highest		= 0
			i			= 0
			for frequency in frequencies:
				if frequency > highest:
					highest		= frequency
					position	= i
				i += 1
			if position == 0:
				self.consensus += 'A'
			elif position == 1:
				self.consensus += 'C'
			elif position == 2:
				self.consensus += 'G'
			elif position == 3:
				self.consensus += 'T'
			elif position in [4,5]:
				self.consensus += '-'
	
	def hamming_distance(self,seq1,seq2):
		"""Counts the hamming distance (how many positions they share) of two sequences with the same length."""
		score 	= 0
		i		= 0
		for base in seq1:
			if base == seq2[i]:
				score += 1
			i += 1
		return score
	
	def print_sequences(self):
		"""Prints the sequences to strdout"""
		for ids,seq in self.seq_dict.items():
			print ids
			print seq
			print len(seq)
			print ''
	
	def print_statistics(self):
		"""Prints the statistics for each position to strdout."""
		positions = sorted(self.statistic_dict.keys())
		for i in positions:
			print i, self.statistic_dict[i]
	

def main():
	pass


if __name__ == '__main__':
	main()

