'''
Created on 26 May 2014

@author: theopavlakou
'''

import numpy as np
class EventProbabilityCalculator():
    '''
    Converts the value of lambda to a probability of an event
    '''


    def __init__(self, weightingVector):
        '''
        Constructor
        '''
        self.w = weightingVector

    def probabilityOfEventWithLambda(self, l):
        return 1.0/(1.0 + np.exp(-self.w[0] - self.w[1]*l))