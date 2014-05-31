'''
Created on 21 May 2014

@author: theopavlakou
'''
from numpy import dot
from numpy import array
from scipy import *
from numpy.linalg import *
from scipy.sparse import *

class MatrixBuilder:
    '''
    A class to construct a (sparse) Matrix on the go.
    '''


    def __init__(self, numberOfRows, numberOfCols):
        '''
        Constructor
        '''
        self.noRows = numberOfRows
        self.noCols = numberOfCols
        self.matrix = lil_matrix((self.noRows, self.noCols), dtype = float)


    def addElement(self, row, col, value):
        """
        Adds an element to the matrix. If it is successful, it returns 0, else it returns
        -1.
        Inputs
            row:        The row index
            col:        The column index
            value:      The value
        Outputs
            0 if successful
            -1 if unsuccessful
        """
        if row < self.noRows and col < self.noCols:
            self.matrix[row, col] = value
            return 0
        else:
            return -1

    def getCooccurrenceMatrix(self):
        """ Returns the hollow cooccurrence matrix given by S'*S - diag(S'*S)."""
        cooccurrenceMatrix = dot(self.matrix.transpose(), self.matrix).todense()
        for i in range(self.noCols):
            cooccurrenceMatrix[i, i] = 0
        return cooccurrenceMatrix
