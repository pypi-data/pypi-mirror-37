# -*- coding: UTF-8 -*-

import os
import sys, getopt
# import filecmp

conj_y = open('conj.yaml','r')
compile_order = '' 
data_name = ''
ssy_name = ''
datamaker_name = ''
filein_name = ''
fileout_name = ''
fileans_name = ''
run_times = 0
ram1 = ''
ram2 = ''

def help_out():
	print('help: python -m selfcmp.work -t <run_times>')

def init(argv) :
	try:
		opts, args = getopt.getopt(argv,"-h-t:",["--help"])
	except getopt.GetopeError:
		help_out()
		sys.exit(2)
	for opt,val in opts:
		if opt in ('-h','--help') :
			help_out()
			sys.exit()
		elif opt == '-t' :
			run_times = int(val)
	data_name = conj_y.readline().strip()
	ssy_name = conj_y.readline().strip()
	datamaker_name = conj_y.readline().strip()
	compile_order = conj_y.readline()
	os.system(compile_order)
	if ssy_name == 'windows' :os.system('g++ '+data_name+'-std\\\\std.cpp -o' + data_name + '-std\\\\std.exe')
	elif ssy_name == 'linux' :os.system('g++ '+data_name+'-std\\\\std.cpp -o' + data_name + '-std\\\\std')
	if ssy_name == 'windows' :os.system('g++ '+data_name+'-data\\\\'+datamaker_name+'.cpp -o ' + data_name + '-data\\\\'+datamaker_name+'.exe')
	elif ssy_name == 'linux' :os.system('g++ '+data_name+'-data\\\\'+datamaker_name+'.cpp -o ' + data_name + '-data\\\\'+datamaker_name)
	filein_name = data_name + '-data\\\\' + data_name + '.in'
	fileout_name = data_name + '-data\\\\' + data_name + '.out'
	fileans_name = data_name + '-data\\\\' + data_name + '.ans'
	if not os.path.exists(fileout_name) : open(fileout_name,'w')
	if not os.path.exists(fileans_name) : open(fileans_name,'w')
	f1 = open(fileout_name,'r')
	f2 = open(fileans_name,'r')
	loginfo = open('log.info','w')
	stdpath = data_name+'-std\\\\'+'std'
	flag = 0
	for i in range(0,run_times):
		if flag == 1 : break
		if ssy_name == 'windows' :
			 os.system(data_name+'-data\\\\'+datamaker_name+'.exe'+' > '+filein_name)
			 os.system(data_name+'-soure\\\\'+data_name+'.exe'+' < '+filein_name+' > '+fileout_name)
			 os.system(stdpath+'.exe'+' < '+filein_name+' > '+fileans_name)
		elif ssy_name == 'linux' :
			os.system(data_name+'-data\\\\'+datamaker_name+' > '+filein_name)
			os.system(data_name+'-soure\\\\'+data_name+' < '+filein_name+' > '+fileout_name)
			os.system(stdpath+' < '+filein_name+' > '+fileans_name)
		ram1 = f1.readlines()
		ram2 = f2.readlines()
		if ram1 != ram2 : flag = 1
		else : 	print(i + 1,'AC')	
	if flag == 1 : loginfo.write('This one is WA')
	else : loginfo.write(str(run_times)+' test is all right!')
		
if __name__ == "__main__":
	init(sys.argv[1:])