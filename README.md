# password-cracking

*Password cracking, hash algorithms, SHA-1, SHA-256, salting and peppering*

---

This project takes previously published lists of password leaks from hacks on Formspring, LinkedIn, and Yahoo and explores different techniques to "crack" and dehash these passwords with the intent of viewing real users' passwords in plaintext. This project was associated with the class Computer Security / ISP in the cybersecurity department of NYU Tandon in Fall 2023. 

Each program accomplishes the following: 

1. Parse the given password dump txt file
2. Considering the formatting and encoding specific to each leak, employ various techniques to crack the passwords
3. Output the cracked passwords to another txt file

**Note:** For the sake of time and resources for this project, I terminated the program after decoding exactly 100 passwords from each leak. 

**Note 2:** Although not shown in the project files, I also utilized the program hashcat to further examine the files. I also used the publicly available *rockyou.txt* file as a database for possible password instead of generating my own. 

**Note 3:** Due to Github's file limits, the original files for *rockyou.txt* and LinkedIn's leak file *SHA1.txt* are too large to upload in their entirety. For the sake of demonstration I cut all but a small sample of *SHA1.txt* and created other files in the *rockyou.txt* folder with smaller subsets of the database. 

## Yahoo

These passwords were stored as plaintext, literally listed as the password next to the user email address. They were formatted like MySQL tables. I could have copy/pasted but I decided to write a short script that found the line where the passwords started then isolated the password itself using the built in “:” delimiter. If they really were stored as plaintext, the security is obviously terrible and no hacking is necessary to sign into a user’s account simply by finding their email address in the file.  

## LinkedIn

These passwords were stored in a file as hashed strings using sha1 hashing. I ran “password” through an online sha1 hash generator and attempted to find it in the sha1.txt file, but no strings matched. I figured out how to use hashcat and ran the command comparing a small amount of the sha1.txt hashes with the online rockyou.txt file. Surprisingly, hashcat returned several matches, including one for “password”. The matched hash for “password” was different from the online generated one. Upon comparing them I realized the only difference was that the stored hash took the true sha1 hash and replaced the first 5 digits with “00000”. I have no idea why, and I have no idea how hashcat still recognized it. I’d like to know more about hashcat’s techniques.  

Obviously after that I realized most of the stored hashes had their first five digits replaced with zeros, so it seemed like all the password hashes used this technique. I modified my python file to splice the password hash strings accordingly and this returned more than 100 matches almost instantly. 

## Formspring

I ran one of the hashes through an online hash detector and it returned sha256, but the produced sha256 hash for “password” again yielded no results. Hashcat also yielded nothing. I googled the Formspring leak and it mentioned that the passwords were salted before being hashed. You can salt a password before hashing by appending a random string, commonly 8 digits long, and then pass it through the hash function. You can also salt it after it’s hashed, but the result would contain some delimiter 
like “:” or “$” and these hashes did not. Additionally, the salt can be added in many different ways like salt + pw, pw + salt, or salt+pw+salt.  

I found a hashcat method where you can input two password files and it would concatenate each combination. I used this method to test a salt value of one utf-8 digit appended after the password. (i.e. password1, where 1 is the salt value.) This did not work, and neither did changing the order (1password). I tried appending a two digit long salt after the password (no results) and then before. This hashcat command ran very slowly but returned a few matches over time. I got five matches before I terminated the command. Each match used two random numbers 0-9 as the salt, so I wrote a program that appended a string 00-99 to each password in rockyou.txt and searched for it in the hash file. This took astronomically long and I barely got through three passwords in ten minutes so I tried again with only 1000 hashes instead of the full hash file. This took around ten minutes to complete but it matched seven passwords. (Very slow!) 

Fun fact: When I was first looking at the formspring.txt file I noticed the first few hashes all contained the string “5be” in the 57th, 58th, and 59th place. I wasted some time on this unfortunately before I realized not every hash had this feature. I’m fairly sure the list is arranged alphabetically/chronologically by last 8 digits, but starting from the middle of the order and looping back around. This is useless infrmation, EXCEPT this made me think of sorting the hash list chronologically and using binary search instead to try to speed up the process. When I ran the new script against the first 1000 hashes and my rockyou file, it returned all seven previously found hashes in about a minute. This was quicker than expected, so I tried the full hash file instead of just 1000 of them. I expected this to take a long time again, but it only took 46 seconds to crack 100 passwords.  

Salting the passwords made the Formspring passwords much harder to crack than the others, even though they used a weak salt in my opinion. Other salts are longer and use all 127 ascii values instead of 10 numerical digits. Finding the salt was the hard part. Once the pattern became clear however, the passwords were easy to crack. Salting as a method of increasing security is not a very strong technique but can be effective in combination with strong hash algorithms.  