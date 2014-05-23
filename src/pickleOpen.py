'''
Created on 22 May 2014

@author: theopavlakou
'''
import pickle, pprint
import matplotlib.pyplot as plt
from TwitterGraphPlotter import TwitterGraphPlotter



if __name__ == '__main__':
    pkl_file = open('pCPickle_15000_3000.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pprint.pprint(data1)
    pkl_file.close()

    fig = plt.figure()
    plt.axis([0, len(data1)+5, -1, 500])
    plt.xlabel("Time")
    plt.ylabel("Information")
    plt.ion()

    gp = TwitterGraphPlotter(data1, title="Sparse PC Eigenvalue vs Data Point. Window Size = 15000, Increment Size = 3000")
    gp.plotGraph()
    gp.saveGraph("first.eps")
    gp.keepGraphLocked()
