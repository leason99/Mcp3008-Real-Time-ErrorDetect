import numpy as np
import ctypes 
import matplotlib
matplotlib.use("Pdf")
import matplotlib.pyplot as plt
import datetime
import threading
import multiprocessing 
from multiprocessing import Process
import time

chnum=3
samples=50000
# command line: ipcrm --all=msg

# init c lib
mcp3008=ctypes.cdll.LoadLibrary("./mcp3008.so")
init=mcp3008.init
listener=mcp3008.listener
detect=mcp3008.detect
freeme=mcp3008.freeme
getListenerData=mcp3008.getListenerData
#c return type
getListenerData.restype=ctypes.POINTER(ctypes.c_int32)





def plot():
    
    print("\nstart getListenerData")
    pointer=getListenerData()
    print("pointer:",pointer.contents)
    # pointer to c memory array 
    ArrayType = ctypes.c_int32*samples*chnum
    array_pointer = ctypes.cast(pointer, ctypes.POINTER(ArrayType))
    data= np.frombuffer(array_pointer.contents,dtype=np.int32)
    
    #data struct [ch][samples]
    res=np.reshape(data,(chnum,samples)) 
    print(data)
    print("start plot")
    
    plt.figure(figsize=(20,10))
    for i in range(chnum):
        
        plt.subplot(chnum, 1, i+1)
        plt.plot(range(len(res[i])), res[i])
        plt.title('ch{}'.format(i))
        plt.ylim((0,1030))
    
    plt.savefig(datetime.datetime.now().isoformat()+".jpeg")
    plt.clf()  
    freeme(pointer)


init()


listener()

thread2=Process(target=detect)
thread2.start()
#detect()
'''
while(1):
    plot()

'''








