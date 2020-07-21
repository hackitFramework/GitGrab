#
# Insecure File-path data sink
#
# Henry Samuelson 6/2/2020

import re
import os

def poke_dir(file_path,ln):
    fp = "cat" + file_path[0] + " > /dev/null 2>&1"
    if int(os.system(fp)) == 0:
        print("[HIT] @ ln:(" + str(ln)+") --> " + str(file_path[0]))
        return [ln,fp]

def parse_file(file):
    f = open(file, 'r')
    insecure_ref=[]
    l_num = 0
    while(True):
        l_num+=1
        line = f.readline().strip()
        if line.split() == []: break
        q = re.findall(r'\/.*\.[\w:]+'. str(line))
        if q != []:
            q1 = re.findall(r"[Pp]assword=|pwd=|PWD=|[Pp]ass=|[Cc]red=|[Cc]reds=|[Cc]redential=|[Cc]redentials=|[Aa]dmin=|passwrd=|[Kk]ey=|[Kk]eys=|private.*[Kk]ey$=",line)
            q2 = re.findall(r"[Pp]assword =|pwd =|PWD =|[Pp]ass =|[Cc]red =|[Cc]reds =|[Cc]redential =|[Cc]redentials =|[Aa]dmin =|passwrd =|[Kk]ey =|[Kk]eys =|private.*[Kk]ey$ =",line)
            if (q1 != [] and q1 != ['"']) | (q2 != [] and q2 != ['"']): insecure_ref.append(poke_dir(q,l_num))