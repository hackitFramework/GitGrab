#
# Insecure File-path data sink
#
# Henry Samuelson 6/2/2020

import re
import os

def parse(filename):
    '''
    Parameters: filename-takes a string
    Returns:    list of possible lines to attack
    '''
    assert type(filename) == str

    file = open(filename, 'r')
    line_num = 0
    nums = []
    pass_lines = []
    while(True):
        line_num += 1
        line = file.readline().strip()
        if line.split() == []: break
        query = re.findall(r"[\/.][a-zA-Z0-9\s]{1,100}(\"|/|$)",line) #/something/
        query.append(re.findall(r"[\/.][a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}(\"|/|$)",line)) #/something/something
        query.append(re.findall(r"[\/.][a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}(\"|/|$)",line)) # /something/something/something


        line_valid = False
        for i in range(0,len(query)):
            # for each found query. Requery the line for password declarations.
            rq1 = re.findall(r"password=|pwd=|pass=|cred=|creds=|credentials=|admin=|passwrd=|key=|keys=|pkey=|private[Kkey]=|private.*[Kk]ey$=",line)
            rq2 = re.findall(r"password =|pwd =|pass =|cred =|creds =|credentials =|admin =|passwrd =|key =|keys =|pkey =|private[Kkey] =|private.*[Kk]ey$ =",line)
            if rq1 != []:
                line_valid = True
                break
            elif rq2 != []:
                line_valid = True
                break
        if line_valid: 
            pass_lines.append(line)
            nums.append(line_num)



    file.close()
    return nums, pass_lines

print(parse("insecure.sh"))
x = parse("insecure.sh")

def poke_directory(lines):
    nums = lines[0]
    lines = lines[1]
    #reparse and find the directory name, then check if access exsists
    hits = []
    for i in range(0, len(lines)):
        line = lines[i]
        # this is inexusable code, I recognize this is horrid in practice.
        query = re.findall(r"[\/.][a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}(\"|/|$)",line) # /something/something/something
        if query == []:
            query = re.findall(r"[\/.][a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}(\"|/|$)",line) #/something/something
            if query == []:
                query = re.findall(r"[\/.][a-zA-Z0-9\s]{1,100}(\"|/|$)",line) #/something/
            if(query != []):
                direc = query[0] 
                direc = "cd " + direc
                if(int(os.system(direc))==0):
                    hits.append([nums[i], direc])
                    print("[HIT] @ ln:(" + str(nums[i]) + ") -->" + direc)
    
    return hits

poke_directory(x)