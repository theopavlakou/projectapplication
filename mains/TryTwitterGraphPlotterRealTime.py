'''
Created on 6 Jun 2014

@author: theopavlakou
'''
import matplotlib.pyplot as plt
from TwitterGraphPlotter import TwitterGraphPlotter
if __name__ == '__main__':


    data = [(1, 2), (2, 3), (3, 4)]
    fig = plt.figure()
    plt.xlabel("Time")
    plt.ylabel("Information")
    plt.ion()
    plt.scatter([x for (x, y) in data], [y for (x, y) in data], c="b")
    for i in range(10):
        plt.scatter(i+3, i+4)
    plt.show(block =True)

#     x.append(i)
#     y.append(eigenvalue)
#     if eigenvalue >150:
#         plt.arrow(i, eigenvalue, 1, 4, width=0.005, head_width=0.05, head_starts_at_zero=False)
#         plt.annotate("this is 100", (i, eigenvalue+4))
#         plt.scatter(i,eigenvalue, c="red")
#     else:
#         plt.scatter(i,eigenvalue, c="blue")
#     i = i + 1
#     plt.draw()
#     time.sleep(0.005)
# plt.show()