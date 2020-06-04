#
# Insecure File-path data sink
#
# Henry Samuelson 6/2/2020

import re

def parse(filename):
    '''
    Parameters: filename-takes a string
    Returns:    list of possible lines to attack
    '''
    assert type(filename) == str

    file = open(filename, 'r')
    line_num = 0
    possible_lines = []
    pass_lines = []
    while(True):
        line_num += 1
        line = file.readline().strip()
        query = re.findall(r"\/[a-zA-Z0-9\s]{1,100}\/",line) #/something/
        query.append(re.findall(r"\/[a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}",line)) #/something/something
        query.append(re.findall(r"\/[a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}\/[a-zA-Z0-9\s\-]{1,100}",line)) # /something/something/something

        print(query)
        if(line.split() == []):
            break
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
            pass_lines.append(line_num)
            possible_lines.append(line)


    file.close()
    return pass_lines, possible_lines

print(parse("insecure.sh"))

