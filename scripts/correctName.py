#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Måns Magnusson on 2011-10-10.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import glob

def main():
	indata	= '../results/2011-09-22/norefall/'
	outdata	= '../results/2011-10-10/noref_all/'
	for inFile in glob.glob(os.path.join(indata,'*.*')):
		j=0
		theFile = inFile[31:]
		letter=''
		newName=''
		while letter != 'a':
			newName	+=theFile[j]
			j		+=1
			letter	= theFile[j]
		os.system('cp '+inFile+' '+outdata+newName+'.fa')
	
	


if __name__ == '__main__':
	main()

