#
# Stored Credential Harvester
#
# Henry Samuelson 6/2/2020
#
# The idea here is this script reads through  plaintext files, looking for varaibles that
# look like passwords and are assigned from filepaths.
# The script then trys to access the filepaths with its user premissions; if the script can
# get access to the password file, then you could also have access. The script then returns
# the filepath of the password and it returns the line of the source file the reference was 
# found on.
#** This is still test code
import re
import os
import sys

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
        q = re.findall(r'\/.*\.[\w:]+', str(line))
        if q != []:
            q1 = re.findall(r"[Pp]assword=|pwd=|PWD=|[Pp]ass=|[Cc]red=|[Cc]reds=|[Cc]redential=|[Cc]redentials=|[Aa]dmin=|passwrd=|[Kk]ey=|[Kk]eys=|private.*[Kk]ey$=",line)
            q2 = re.findall(r"[Pp]assword =|pwd =|PWD =|[Pp]ass =|[Cc]red =|[Cc]reds =|[Cc]redential =|[Cc]redentials =|[Aa]dmin =|passwrd =|[Kk]ey =|[Kk]eys =|private.*[Kk]ey$ =",line)
            if (q1 != [] and q1 != ['"']) | (q2 != [] and q2 != ['"']): insecure_ref.append(poke_dir(q,l_num))

os.system("clear")
print("")
print("     --> StoredCredential Harvester <--")
print("~H.E.Samuelson")
print("")
parse_file(sys.argv[0])