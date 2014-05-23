'''
Created on 22 May 2014

@author: theopavlakou
'''
import pickle, pprint
import matplotlib.pyplot as plt
import time
fig = plt.figure()
xCurrent = 0
plt.ion()
x = []
y = []
plt.axis([0, 100, -1, 500])
plt.xlabel("Time")
plt.ylabel("Information")
plt.show()
plt.ion()


if __name__ == '__main__':
    pkl_file = open('pCPickle.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pprint.pprint(data1)
    pkl_file.close()

    i = 0
    prevEigVal = data1[0][1]
    currentColour = "blue"
    for dataPoint in data1:
        eigVal = dataPoint[1]

        if eigVal > prevEigVal*5:
            currentColour = "red"
            plt.annotate("Event starts here", (i, eigVal+20))
        elif prevEigVal > eigVal*5:
            currentColour = "blue"
            plt.annotate("Event ends here", (i, eigVal+20))
        prevEigVal = eigVal
        plt.scatter(i,eigVal, c=currentColour)
        i = i + 1
        plt.draw()
        time.sleep(0.05)

plt.show(block=True)
