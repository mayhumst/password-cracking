# passwords are stored in regular text, not hashed

# read file until line recognized

file = open('../yahoo/password.file', 'r')
lines = file.readlines()
file.close()

filewrite = open('../yahoo/passlistyahoo.txt', 'w')

k=0
start="false"
for line in lines:
    line = line.rstrip('\n')
    if(line == "user_id   :  user_name  : clear_passwd : passwd"):
        start = "true"
        continue
    if(start == "true"):
        x = line.split(":")
        if(len(x)>1):
            print(x[2])
            filewrite.write(line + " " + x[2] + "\n")
            k+=1
    if(k==100):
        break

filewrite.close()
    