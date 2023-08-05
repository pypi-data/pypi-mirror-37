# -*- coding: UTF-8 -*-

import sys, getopt
import os

def help_out():
	print("help: \'python -m selfcmp.pro -n <soure/problem/data_name> -f <language/format_name> -d <data_maker_name> -o <system_name> -u <mode>\'\n mode:\n \'datamaker\' 数据生成器对拍\n\'datafile\' 输入输出数据对拍")
	
data_name = '_'
format_name = '_'
datamaker_name = '_'
ssystem_name = '_'
std_name = '_'
mode_name = '_'	

	
def check_file(argv):
#	try:
#		opts, args = getopt.getopt(argv,"-h-n:-f:-d:-o:-u:",["--help"])
#	except getopt.GetoptError:
#		help_out()
#		sys.exit(2)
	global data_name
	global format_name
	global datamaker_name
	global ssystem_name
	global std_name
	global mode_name
	global file_out
	l = len(argv)
	i = 0
	while i<l :
		if argv[i] in ('-h','--help'):
			help_out()
			sys.exit()
		elif argv[i] == '-n':
			i += 1
			data_name = argv[i]
			if not os.path.exists(data_name+'-data'): os.makedirs(data_name+'-data')
			if not os.path.exists(data_name+'-soure'): os.makedirs(data_name+'-soure')
		elif argv[i] == '-f':
			i += 1
			format_name = argv[i]
		elif argv[i] == '-d':
			i += 1
			datamaker_name = argv[i]
		elif argv[i] == '-o':
			i += 1
			ssystem_name = argv[i]
		elif argv[i] == '-u':
			i += 1
			mode_name = argv[i]
			if not ( mode_name in ('datamaker','datafile') ):
				print('mode_name error!\n')
				help_out()
				sys.exit()
		i+=1
	file_out = open('conj.yaml','w')
	if not os.path.exists(data_name+'-std') :
		os.makedirs(data_name+'-std')
	file_out.write(data_name+'\n')
	file_out.write(ssystem_name+'\n')
	file_out.write(datamaker_name+'\n')
	path_name = data_name +'-soure/' + data_name +'.' + format_name +' ' 
	if format_name == 'cpp' :
		if ssystem_name == 'windows' :file_out.write('g++ ' + path_name + '-o '+ data_name + '-soure/' + data_name +'.exe')
		elif ssystem_name == 'linux' :file_out.write('g++ ' + path_name + '-o '+data_name + '-soure/' + data_name)
	if ssystem_name == 'windows' : runner_sp = open('runner.bat','w')
	elif ssystem_name == 'linux' : runner_sp = open('runner.sh','w')
	if mode_name == 'datamaker':			
		runner_sp.write('python -m selfcmp.work -t 10\npause')
	elif mode_name == 'datafile':
		runner_sp.write('python -m selfcmp.filewk -s 1 -t 10\npause')

if __name__ == "__main__" :
	check_file(sys.argv[1:])