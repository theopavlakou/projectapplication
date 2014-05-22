'''
Created on 22 May 2014

@author: theopavlakou
'''
import pickle, pprint
if __name__ == '__main__':
    pkl_file = open('pCPickle.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pprint.pprint(data1)
    pkl_file.close()