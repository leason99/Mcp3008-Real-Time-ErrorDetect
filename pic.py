import os
import numpy as np
import matplotlib
matplotlib.use("Pdf")
import matplotlib.pyplot as plt
chnum=3
samples=50000
if not os.path.exists("./pic"):
    os.mkdir("./pic")
fileList=os.listdir("./data")
for filename in fileList:
    
    print("\n",filename)
    file=open("./data/{}".format(filename),mode='r')
    Str=file.readline()
    
    data=np.array([int(n) for n in Str.split(",")[:-1]],dtype=int)
  
    

    #data struct [ch][samples]
    res=np.reshape(data,(chnum,samples)) 
    
    plt.figure(figsize=(20,10))
    for i in range(chnum):
        plt.subplot(chnum, 1, i+1)
        plt.plot(range(len(res[i])), res[i])
        plt.title('ch{}'.format(i))
        plt.ylim((0,1030))

    plt.savefig("./pic/{}.jpeg".format(filename))
    plt.close('all')