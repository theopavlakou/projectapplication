'''
Created on 22 May 2014

@author: theopavlakou
'''
import pickle, pprint
import matplotlib.pyplot as plt
from TwitterGraphPlotter import TwitterGraphPlotter



if __name__ == '__main__':
    windowSize = 15000
    incrementSize = 3000
    pkl_file = open('pCPickle_all_' + str(windowSize) + '_' + str(incrementSize) + '.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pprint.pprint(data1)
    pkl_file.close()

#     textFile = open('data_all.txt', 'w')
#     for (array, eigVal, startDate, endDate) in data1:
#         textFile.write(str(array) + '\t' + str(eigVal) +'\t' + startDate + '\t' + endDate + '\n')
#     textFile.close()
    fig = plt.figure()
    plt.axis([0, len(data1)+5, -1, 500])
    plt.xlabel("Time")
    plt.ylabel("Information")
    plt.ion()

    gp = TwitterGraphPlotter(data1, title="Sparse PC Eigenvalue vs Data Point. Window Size = " + str(windowSize) + ", Increment Size = " + str(incrementSize))
    gp.plotGraph(plotDates = False)
    gp.saveGraph("first.eps")
    gp.keepGraphLocked()
