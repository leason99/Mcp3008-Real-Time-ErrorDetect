import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Pdf")
import matplotlib.pyplot as plt
from tqdm import tqdm, trange


     
def generate(self):
    chnum=3
    samples=50000
    if not os.path.exists("./pic"):
        os.mkdir("./pic")
    fileList=os.listdir("./data")
    bar=tqdm(fileList)
    for x,filename in enumerate( fileList):
        
        #print("\n",filename)
        file=open("./data/{}".format(filename),mode='r')
        Str=file.readline()



        #data=np.array([int(n) for n in Str.split(",")[:-1]],dtype=int)
        strData= Str.split(",")
        data=np.array([int(n) for n in strData[:-1]],dtype=int)

        samplerate=strData[-1]
        #data struct [ch][samples]
        res=np.reshape(data,(chnum,samples)) 
        plt.figure(figsize=(20,10))
        plt.suptitle("samplerate: {}".format(strData[-1]))
        bar.set_description("\rgenerator pic for {}  ".format(filename))
        bar.update(1)
        
        for i in range(chnum):
            
        
            plt.subplot(chnum, 1, i+1)
            plt.plot(range(len(res[i])), res[i])
            plt.title('ch{}'.format(i))
            plt.ylim((0,1030))

        plt.savefig("./pic/{}.jpeg".format(filename))
        plt.close('all')


if __name__ == "__main__":
    picGenerator=PicGenerator()
    picGenerator.generate()