import hashlib; 
import math;

# parse password file
# MADE NEW TXT FILE: throwing error on full file.
file1 = open('../rockyou.txt/rockyoucopy.txt', 'r')
lines = file1.readlines()
file1.close()
pass_list = []

#add each sample password to pass_list
for line in lines: 
    line = line.rstrip('\n')
    pass_list.append(line)
    
#parse hash file
file2 = open('../formspring/formspring.txt', 'r')
lines2 = file2.readlines()
file2.close()
hash_list = []

#add each hash to array of hash strings

for line in lines2:
    line = line.rstrip('\n')
    hash_list.append(line)

    
hash_list.sort()

# open file to write
filewrite = open('../formspring/sortedcrack.txt', 'w')

control = ["cristianoronaldo"]

k = 0
# for each password
for pw in pass_list:
    # generate salt 00 - 99 
    i = 0
    br = 'false'
    while(i<100):
        if(i<10):
            salt = "0" + str(i)
        else:
            salt = str(i)
        # append salt to password, hash
        pwsalt = salt + pw
        pwhashed = hashlib.sha256(pwsalt.encode('utf-8')).hexdigest()
                
        upper = len(hash_list)-1
        lower=0
        # find hash in list
        while(upper>=lower):
            mid = math.floor((upper+lower)/2 )
    
            hash = hash_list[mid]
            if(pwhashed == hash):
                filewrite.write(hash + " " + pw + "\n")
                print("PASSWORD MATCH")
                k+=1
                br = 'true'
                break # don't compare any more hashes bc already found
            elif(pwhashed>hash):
                lower = mid +1
            else:
                upper = mid-1
        if(br == 'true'):
            break
        i+=1  
    if(k == 100): # 100 passwords found (if only)
        break 
        

filewrite.close()

