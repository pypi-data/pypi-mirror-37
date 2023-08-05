# -*- coding: UTF-8 -*-

import os
import sys


def help():
    print("help:\'python -m selfcmp.datamk --init <problem_name> <language>\':这是初始化,初始化系统类型默认为\'windows\',\'<problem_name>\'表示你的题目名称,\'<language>\'表示源程序语言类型，如\'cpp\'表示C++语言,默认为\'cpp\',两个之间要有空格\n 按照格式填好配置文件\'set.yaml\'后使用\'python -m selfcmp.datamk -s <data_st> -t <data_en>\'一键生成数据，其中\'data_st,data_en\'表示数据开始与结束编号，注意开始编号必须严格小于等于结束编号")

def init_data(file_name, language):
    os.makedirs(file_name)
    dir_name = file_name + "\\"  
    os.makedirs(dir_name + file_name + "-data")
    os.makedirs(dir_name + file_name + "-soure")
    file_set = open(dir_name + "set.yaml","w")
    file_set.write(file_name + '\n')
    file_set.write("windows\n")
    file_set.write(file_name + "-data" + '\n')
    file_set.write(file_name + "-ans" + '\n')
    file_set.write("g++ " + dir_name + file_name + "-soure\\" + file_name + "-data." + language + " -o " + dir_name + file_name + "-soure\\" + file_name + "-data" + ".exe\n")
    file_set.write("g++ " + dir_name + file_name + "-soure\\" + file_name + "-ans." + language + " -o " + dir_name + file_name + "-soure\\" + file_name + "-ans" + ".exe\n")
    file_set.write("下面每行写入数据生成器的参数：如你的数据生成器读入一个n，生成n个数字，你就在每行写入该组的参数n,你可以按照wiki的说明更改此配置文件内容，但是最后的EOF结束符不能删去，且必须放在单独一行;如果数据生成器无需参数，那么对于每一组写\'_\'占行\n")
    file_set.write("EOF")

st = -1
en = -1
datamaker_name = ''
ansmaker_name = ''
ssystem_name = ''


def work(argv):
    l = len(argv)
    i = 0
    global st
    global en
    global datamaker_name
    global ansmaker_name
    global ssystem_name
    while i<l :
        if argv[i] in ('-h','--help'):
            help()
            sys.exit()
        elif argv[i] == '--init':
            i += 1
            if i+1 >= l : argv.append("cpp")
            init_data(argv[i],argv[i+1])
            sys.exit()
        elif argv[i] == '-s':
            i += 1
            st = int(argv[i])
        elif argv[i] == '-t':
            i += 1
            en = int(argv[i])
        i += 1
    if st == -1 and en == -1 :
        st = 0
        en = 0
    if st == -1 : st=en
    if en == -1 : en=st
    data_in = open("set.yaml","r")
    file_name = data_in.readline().strip()
    ssystem_name = data_in.readline().strip()
    ram = data_in.readline().strip()
    if ssystem_name == 'windows' : datamaker_name = file_name + '-soure\\' + ram + '.exe'
    elif ssystem_name == 'linux' : datamaker_name = file_name + '-soure\\' + ram
    ram = data_in.readline().strip()
    if ssystem_name == 'windows' : ansmaker_name = file_name + '-soure\\' + ram + '.exe'
    elif ssystem_name == 'linux' : ansmaker_name = file_name + '-soure\\' + ram
    ram = data_in.readline().strip()
    os.system(ram)
    ram = data_in.readline().strip()
    os.system(ram)
    format_in = data_in.readline().strip()
    format_ans = data_in.readline().strip()
    i = st
    while ram != "EOF":
        ram = data_in.readline().strip()
        data_ini = open("data_ini.yaml","w")
        data_ini.write(ram)
        os.system(datamaker_name + "< " + " data_ini.yaml " + "> " + file_name + "-soure\\" + file_name + str(i) + format_in)
        os.syetem(ansmaker_name + "< " + file_name + "-soure\\" + file_name + str(i) + format_in + " > " + file_name + "-soure\\" + file_name + str(i) + format_ans)
        i += 1
        if i>en : break

if __name__ == "__main__":
    work(sys.argv[1:])
        
        
