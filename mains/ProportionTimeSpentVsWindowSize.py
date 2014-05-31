'''
Created on 31 May 2014

@author: theopavlakou
'''
import matplotlib.pyplot as plt

if __name__ == '__main__':
    windowSizes = [100, 500, 2000, 3000, 5000, 7500, 10000, 20000, 50000]
    propPopMatrix = [0.058, 0.366, 0.706, 0.771, 0.815, 0.846, 0.875, 0.888, 0.902]
    propCalcSPCA = [0.263, 0.194, 0.120, 0.073, 0.051, 0.033, 0.021, 0.010, 0.004]

    fig = plt.figure()
    plt.xlabel("Size of window/Number of Tweets")
    plt.ylabel("Proportion of time spent in portion of code")
    plt.title("How proportion of time spent in each portion of code changes with the size of window")
    plt.ion()

    plt.plot(windowSizes, propPopMatrix, 'r')
    plt.plot(windowSizes, propCalcSPCA, 'b')
    plt.show(block=True)
    #TODO: Add legend here