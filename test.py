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


mcp3008=ctypes.cdll.LoadLibrary("./mcp3008.so")



init=mcp3008.init
getListenerData=mcp3008.getListenerData
getListenerData.restype=ctypes.POINTER(ctypes.c_int32)

ArrayType = ctypes.c_int32*50000



listener=mcp3008.listener
detect=mcp3008.detect

DataBuf=(ctypes.c_int*50000)()
DataBuf_point=ctypes.cast(DataBuf, ctypes.POINTER(ctypes.c_int))

#ipcrm --all=msg

def plot():
    
    print("\nstart getListenerData")
    pointer=getListenerData()
    print("pointer:",pointer.contents)
    array_pointer = ctypes.cast(pointer, ctypes.POINTER(ArrayType))
    data= np.frombuffer(array_pointer.contents,dtype=np.int32)
    print(data)
    print("start plot")
    plt.plot(range(len(data)),data)
    plt.savefig(datetime.datetime.now().isoformat()+".jpeg")
    plt.cla()  


init()

'''
thread2=Process(target=mcp3008.listener,args=(DataBuf_point,))
thread2.start()
thread2.join()

thread1=threading.Thread(target=mcp3008.detect)
thread1.start()


'''
thread3=Process(target=plot)

#thread3.start()

listener(DataBuf_point)

thread2=Process(target=detect)

thread2.start()
#detect()
while(1):
    plot()

'''
print("\nstart getListenerData")
pointer=getListenerData()
array_pointer = ctypes.cast(pointer, ctypes.POINTER(ArrayType))
data= np.frombuffer(array_pointer.contents,dtype=np.int32)
print(data)
print("start plot")
plt.plot(range(len(data)),data)
plt.savefig(datetime.datetime.now().isoformat()+".jpeg")
plt.show()
'''








