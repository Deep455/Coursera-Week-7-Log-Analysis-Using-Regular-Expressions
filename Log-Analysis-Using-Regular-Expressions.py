#!/usr/bin/env python3
import re, csv, operator

error_count={}
username_info={}
username_error={}

file = open("syslog.log", 'r')
lines = file.readlines()
for line in lines:
    line = line.strip()
    res = re.search(r"ERROR ([\w ']*) \(", line)
    if res!=None:
        err=re.findall(r"ERROR ([\w ']*) \(", line)
        error=err[0]
        if error in error_count.keys():
            error_count[error]+=1
        else:
            error_count[error]=1
        
        user = re.findall(r"\(([\w.]*)\)", line)
        username=user[0]
        if username in username_info.keys():
            username_error[username]+=1
        else:
            username_error[username]=1
        
        if username not in username_info.keys():
            username_info[username]=0
        
    res=re.search(r"INFO", line)
    if res!=None:
        user=re.findall(r"\(([\w.]*)\)", line)
        username=user[0]
        if username in username_info.keys():
            username_info[username]+=1
        else:
            username_info[username]=1

        if username not in username_error.keys():
            username_error[username]=0

file.close()

fh1=open("error_message.csv", 'w')
csvwriter=csv.writer(fh1)
header=["Error", "Count"]
csvwriter.writerow(header)
items=sorted(error_count.items(), key=operator.itemgetter(1), reverse=True)
for item in items:
    rw=[item[0], item[1]]
    csvwriter.writerow(rw)

fh1.close()

fh2=open("user_statistics.csv", 'w')
csvwriter=csv.writer(fh2)
header=["Username", "INFO", "ERROR"]
csvwriter.writerow(header)
items=sorted(username_info.items())
for item in items:
    rw=[item[0], item[1], username_error[item[0]]]
    csvwriter.writerow(rw)

fh2.close()
