# -*- coding: UTF-8 -*-

import sys, getopt
import os

def help_out():
	print("help: \'python -m selfcmp.spw -s <dir_name>\'")
	
dir_name = ''
	
def check_file(argv):
	try:
		opts, args = getopt.getopt(argv,"-h-s:",["--help"])
	except getopt.GetoptError:
		help_out()
		sys.exit(2)
	
	for opt,val in opts:
		if opt in ('-h','--help'):
			help_out()
			sys.exit()
		elif opt == '-s':
			dir_name = val
			os.makedirs(dir_name)
	

if __name__ == "__main__" :
	check_file(sys.argv[1:])