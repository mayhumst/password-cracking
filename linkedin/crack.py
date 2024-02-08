import hashlib; 

# parse password file
# MADE NEW TXT FILE: throwing error on full file.
file1 = open('../rockyou.txt/first120.txt', 'r')
lines = file1.readlines()
file1.close()
pass_list = []

#add each sample password to pass_list
for line in lines: 
    line = line.rstrip('\n')
    pass_list.append(line)
    
#parse hash file
file2 = open('../linkedin/SHA1.txt', 'r')
lines2 = file2.readlines()
file2.close()
hash_list = []

#add each hash to array of hash strings
for line in lines2:
    line = line.rstrip('\n')
    hash_list.append(line)


# open file to write
filewrite = open('../linkedin/crackedlistlinkedin.txt', 'w')

i=1
k=0
for pw in pass_list:
    j=1
    pwhashed = hashlib.sha1(pw.encode('utf-8')).hexdigest()
    pwhashCut = pwhashed[5::]
    pwhashFinal = "00000" + pwhashCut
    for hs in hash_list:
        if pwhashFinal == hs:
            print("PASSWORD MATCH! Password " + pw + " on line " + str(i) + " hash " + hs + ' on line ' + str(j))
            filewrite.write(hs + " " + pw + "\n")
            k+=1
        j+=1
        if (k == 100): #when 100 passwords are cracked
            break
    i+=1

filewrite.close()

