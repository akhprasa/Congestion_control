import os
import sys

files = os.listdir('log_files/')
# stores sum of throughput for particular time
throughput_list=[]

# number of values obtained at that time -> to calculate the avg
count=[]
for f in files:
    log = open('log_files/'+f, 'r')
    lines = log.readlines()
    c=0
    for line in lines:
        data = line.split(' ')
        if(len(data)==2):
            if(c==len(throughput_list)):
                throughput_list.append(float(data[1]))
                count.append(1)
            else:
                throughput_list[c]+=(float(data[1]))
                count[c]+=1
            c+=1

for j in range(len(throughput_list)):
    throughput_list[j] = throughput_list[j]/count[j]

print(throughput_list)
    