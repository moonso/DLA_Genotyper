#!/usr/bin/env python
# encoding: utf-8
"""
sequence.py

This is a class that will have info and methods for dealing with sequences.

Created by Måns Magnusson on 2012-03-10.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import glob

class Sequences:
	"""Alleles holds information about the allele candidates found in a set of sequences."""
	def __init__(self, variable_positions_treshold = 0.2):
		self.seq_dict = {}
		self.variable_positions_treshold = variable_positions_treshold
		self.nr_of_seq = len(self.seq_dict)
		self.frequence_dict = {}
		self.variable_positions	= {}
		self.sequences_sorted = {}
		self.consensus = '' # The consensus sequence of the sequences in this object
		self.allele_1 = ''
		self.allele_2 = ''
	
	def add_sequence(self, sequence_id, sequence):
		"""Add a sequence to the sequence dict."""
		self.seq_dict[sequence_id] = sequence
		self.nr_of_seq = len(self.seq_dict)
	
	def make_own_frequencies(self):
		"""Make the frequence dict for all sequences"""
		self.frequence_dict = self.make_frequencies(self.seq_dict)
	
	def make_frequencies(self, sequence_dict):
		"""Make a dictionary with the frequencies of each position"""
		frequence_dict = {}
		pos_dict = {}
		nr_of_seq = len(sequence_dict)
		for ids, seq in sequence_dict.items():
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
			if nr_of_seq == 0:
				nr_of_seq	= 1
			A	= values['A']/nr_of_seq
			C	= values['C']/nr_of_seq
			G	= values['G']/nr_of_seq
			T	= values['T']/nr_of_seq
			N	= (values['N'] + values['-'])/nr_of_seq
			frequence_dict[pos]=[A,C,G,T,N]
		return frequence_dict
	
	def make_seq_dict(self, seq_ids):
		"""Make a sequence dict from the sequence ids in a list."""
		seq_dict	= {}
		for sequence_id in seq_ids:
			seq_dict[sequence_id]	= self.seq_dict[sequence_id]
		return seq_dict
	
	def find_variable_positions(self):
		"""Picks out the variable positions, based on the frequence of the positions in one individual."""
		def get_variants(frequency, variable_positions_treshold):
			"""Returns a string with the nucloetides, eg. 'AC'"""
			variants	= ''
			if frequency[0] > variable_positions_treshold:
				variants	+= 'A'
			if frequency[1] > variable_positions_treshold:
				variants	+= 'C'
			if frequency[2] > variable_positions_treshold:
				variants	+= 'G'
			if frequency[3] > variable_positions_treshold:
				variants	+= 'T'
			return variants
		
		def indel_position(position):
			"""Returns a boolean depending on if the position has more than 10% indels or if the two positions surrounding the present have more than 10% indels. Input: A dictionary with freq for each position Output: A boolean depending on if the positions are variable"""
			indel_position	= False
			for i in range(position-1,position+2):
				if self.frequence_dict[i][4] > 0.1: #If more than 10% of sequences have indel in any position around.
					indel_position = True
			return indel_position
		
		for pos in self.frequence_dict:
		#We look at the second max so we can see if there is distribution
		#between more than one nucleotide.
			if pos > 30 and pos < 270:# Avoid looking at the tags
				if not indel_position(pos):
					variants	= get_variants(self.frequence_dict[pos], self.variable_positions_treshold)#Variants is a string with the two bases.
					second_max	= sorted(self.frequence_dict[pos][:4])[2]
					if second_max > self.variable_positions_treshold:
						self.variable_positions[pos] = variants
	
	def sort_sequences(self, position):
		"""Divide the sequences into groups based on the position given. Returns a list with two sequence dictionarys."""
		groups = {}
		for sequence_id in self.seq_dict:
			nucleotide = self.seq_dict[sequence_id][position-1]
			if nucleotide in self.variable_positions[position]:# Check if the nucleotide is one of the two variants
				if nucleotide in groups:
					groups[nucleotide].append(sequence_id)
				else:
					groups[nucleotide] = [sequence_id]
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
	
	def get_highest_frequency(self, frequencies):
		"""Returns the nucleotide with the highest frequency."""
		highest = 0
		for i in range(len(frequencies)):
			if frequencies[i] > highest:
				highest = i
		if highest == 0:
			return 'A'
		elif highest == 1:
			return 'C'
		elif highest == 2:
			return 'G'
		elif highest == 3:
			return 'T'
		elif highest == 4:
			return '-'
	
	def print_sequences(self):
		"""Prints the sequences to strdout"""
		for ids,seq in self.seq_dict.items():
			print ids
			print seq
			print len(seq)
			print ''
	
	def find_alleles(self):
		"""Find the alleles for these sequences."""
		self.make_own_frequencies()
		self.find_variable_positions()
		previous_position = 0
		for position in range(1,len(self.frequence_dict)+1):
			if position in self.variable_positions:
				if previous_position != 0:
					freq_dicts = []
					sequence_groups = self.sort_sequences(position)
					for group in sequence_groups:
						sequence_dict = self.make_seq_dict(sequence_groups[group])
						freq_dicts.append(self.make_frequencies(sequence_dict))
					for freq in freq_dicts:
						print position
						print freq[position]
					previous_position = position
				else:
					self.allele_1 += self.variable_positions[position][0]
					self.allele_2 += self.variable_positions[position][1]
					previous_position = position
			else:
				nucleotide = self.get_highest_frequency(self.frequence_dict[position])
				self.allele_1 += nucleotide
				self.allele_2 += nucleotide
		print self.allele_1
		print self.allele_2


def main():
	pass


if __name__ == '__main__':
	main()

