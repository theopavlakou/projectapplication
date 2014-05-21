'''
Created on 21 May 2014

@author: theopavlakou
'''
import unittest
from MatrixBuilder import MatrixBuilder
from scipy.sparse import csc_matrix, lil_matrix


class TestMatrixBuilder(unittest.TestCase):


    def setUp(self):
        # Construct a matrix with 10 rows and 5 columns
        self.numberRows = 10
        self.numberCols = 5
        self.MatrixBuilder = MatrixBuilder(self.numberRows, self.numberCols);


    def tearDown(self):
        pass

    def testConstructorWorks(self):
        self.assertTrue(self.MatrixBuilder.noRows == self.numberRows, "The number of rows is not correct")
        self.assertTrue(self.MatrixBuilder.noCols == self.numberCols, "The number of columns is not correct")
        self.assertTrue(isinstance(self.MatrixBuilder.matrix, lil_matrix), "A sparse matrix was not created")

    def testAddElementWorksForInBoundIndex(self):
        self.assertTrue(self.MatrixBuilder.addElement(3, 2, 10.3) == 0, "Did not return 0")
        self.assertTrue(self.MatrixBuilder.matrix[3, 2] == 10.3, "The number returned is not correct")

    def testAddElementFailsForOutOfBoundIndex(self):
        self.MatrixBuilder.addElement(3, 20, 10.3)
        self.assertTrue(self.MatrixBuilder.addElement(3, 20, 10.3) == -1, "Did not return -1")

    def testGetCooccurenceMatrix(self):
        cooccurenceMatrix = self.MatrixBuilder.getCooccurrenceMatrix()
        self.assertTrue(cooccurenceMatrix.shape == (self.numberCols, self.numberCols) )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()