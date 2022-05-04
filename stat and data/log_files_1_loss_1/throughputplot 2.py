import os
import sys
import matplotlib.pyplot as plt

files = os.listdir('log_files/')

#stores the count of throughputs for each time -> to calcualte avg
cnt = {
    'bbr':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'cubic':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'hybla':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'illinois':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'reno':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'vivace':{
        'r1':[],
        'r2':[],
        'r3':[]
    }

}


# stores sum of throughput for each time
my_dict = {
    'bbr':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'cubic':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'hybla':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'illinois':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'reno':{
        'r1':[],
        'r2':[],
        'r3':[]
    },
    'vivace':{
        'r1':[],
        'r2':[],
        'r3':[]
    }


}

# doing the sum of throughput
for f in files:
    name = f.split('_')
    cur_algo = name[2]
    cur_cli = name[1]
    log = open('log_files/'+f, 'r')
    lines = log.readlines()
    c=0
    for line in lines:
        data = line.split(' ')
        if(len(data)==2):
            if(c==len(my_dict[cur_algo][cur_cli])):
                my_dict[cur_algo][cur_cli].append(float(data[1]))
                cnt[cur_algo][cur_cli].append(1)
            else:
                my_dict[cur_algo][cur_cli][c]+=(float(data[1]))
                cnt[cur_algo][cur_cli][c]+=1
            c+=1

# calculating avg
for key, values in my_dict.items():
    for k, v in values.items():
        for j in range(len(v)):
            my_dict[key][k][j]=my_dict[key][k][j]/cnt[key][k][j]

# fairness dict
throughput={
    'bbr':[],
    'cubic':[],
    'hybla':[],
    'illinois':[],
    'reno':[],
    'vivace':[]
}

for key,values in my_dict.items():
    throughput[key]=my_dict[key]['r1']

throughput['pcc']=throughput['vivace']
throughput.pop('vivace')

xax = list(range(1,121))
print(len(xax))
for key, val in throughput.items():
    plt.plot(xax,throughput[key], label = key)
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mb/s)')
plt.title('loss={:.0%} and RTT=1ms'.format(0.01))
plt.show()

