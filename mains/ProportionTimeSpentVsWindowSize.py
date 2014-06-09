'''
Created on 31 May 2014

@author: theopavlakou
'''
import matplotlib.pyplot as plt

if __name__ == '__main__':
    windowSizes = [100, 500, 1000, 2500, 5000, 7500, 10000, 20000, 50000]
    propPopMatrix = [0.043, 0.224, 0.404, 0.561, 0.666, 0.712, 0.744, 0.789, 0.800 ]
    propCalcSPCA = [0.271, 0.262, 0.184, 0.152, 0.095, 0.063, 0.042, 0.018, 0.009]

    fig = plt.figure()
    plt.xlabel("Size of window/Number of Tweets")
    plt.ylabel("Proportion of time spent in portion of code")
    plt.title("How proportion of time spent in each portion of code changes with the size of window")
    plt.ion()

    a = plt.plot(windowSizes, propPopMatrix, color='r', label="t1")
    b = plt.plot(windowSizes, propCalcSPCA, color='b', label="t2")
    redRect = plt.Rectangle((0, 0), 1, 1, fc="r")
    blueRect = plt.Rectangle((0, 0), 1, 1, fc="b")
    plt.legend([redRect, blueRect], ["Populate Matrix $\mathbf{S}$", "Calculate Sparse Principal Component"])

    plt.show(block=True)
