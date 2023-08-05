# -*- coding: UTF-8 -*-

import os
import sys, getopt
# import filecmp

conj_y = open('conj.yaml','r')
compile_order = ''
data_name = ''
ssy_name = ''
datamaker_name = ''
file_name = ''
filein_name = ''
fileout_name = ''
fileans_name = ''
ans_suf = '.ans'
input_suf = '.in'
ram1 = ''
ram2 = ''
st = 0
en = 0
ok = 0

def help_out():
	print('help: python -m selfcmp.filewk -n <file_name> -s <start_num> -t <end_num> -a <ans_format> -i <input_format>\n 输入输出数据请用如\'name1.in\'和\'name1.ans\'格式,name可自行替换,如果为\"1.in\",则输入`_`，否则使用默认的目录名作为输入输出文件名。<ans_format>为答案文件后缀，默认为`.ans`,无后缀可输入`_`,`input_format`为输入文件后缀，同理，默认为`.in`')

def init(argv) :
	# try:
	# 	opts, args = getopt.getopt(argv,"-h-s:-t:",["--help"])
	# except getopt.GetopeError:
	# 	help_out()
	# 	sys.exit(2)
	global ok
	global ans_suf
	global input_suf
	l = len(argv)
	i = 0
	while i<l :
		if argv[i] in ('-h','--help') :
			help_out()
			sys.exit()
		elif argv[i] == '-s' :
			i += 1
			st = int(argv[i])
		elif argv[i] == '-t' :
			i += 1
			en = int(argv[i])
		elif argv[i] == '-n' :
			i += 1
			file_name = argv[i]
			ok = 1
			if file_name == '_' : file_name = ''
		elif argv[i] == '-a' :
			i += 1
			ans_suf = argv[i]
			if ans_suf == '_' : ans_suf = ''
		elif argv[i] == '-i' :
			i += 1
			input_suf = argv[i]
			if input_suf == '_' : input_suf = ''
		i+=1
	data_name = conj_y.readline().strip()
	ssy_name = conj_y.readline().strip()
	datamaker_name = conj_y.readline().strip() # not use
	compile_order = conj_y.readline()
	os.system(compile_order)
	if ok == 0 : file_name = data_name
	filein_name = data_name + '-data\\\\' + file_name
	fileout_name = data_name + '-data\\\\' + data_name + '.out'
	fileans_name = data_name + '-data\\\\' + file_name
	if not os.path.exists(fileout_name) : open(fileout_name,'w')
	loginfo = open('log.info','w')
	flag = -1
	for i in range(st,en + 1):
		if flag != -1 : break
		f1 = open(fileans_name+str(i)+ans_suf)
		f2 = open(fileout_name)
		if not os.path.exists(filein_name+str(i)+input_suf):
			print(str(i)+'th Input not found!')
			continue
		if not os.path.exists(fileans_name+str(i)+ans_suf):
			print(str(i)+'th Output not found!')
			continue
		if ssy_name == 'windows' :
			 os.system(data_name+'-soure\\\\'+data_name+'.exe'+' < '+filein_name+str(i)+input_suf+' > '+fileout_name)
		elif ssy_name == 'linux' :
			os.system(data_name+'-soure\\\\'+data_name+' < '+filein_name+str(i)+input_suf+' > '+fileout_name)
		ram1 = f1.readlines()
		ram2 = f2.readlines()
		if ram1 != ram2 : flag = i
		else : 	print('test '+str(i)+' is AC')
	if flag != -1 :
		print('You Have WA!! QAQ!!')
		loginfo.write('This '+str(flag)+'.in'+' is WA')
	else : loginfo.write(str(st)+'~'+str(en)+' test is all right!')

if __name__ == "__main__":
	init(sys.argv[1:])
