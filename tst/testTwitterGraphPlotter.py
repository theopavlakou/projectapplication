'''
Created on 23 May 2014

@author: theopavlakou
'''
import unittest
from TwitterGraphPlotter import TwitterGraphPlotter

class Test(unittest.TestCase):


    def setUp(self):
        self.dummyData = []
        self.dummyData.append((["word1", "word2", "word3"], 3, "startDate0", "endDate0"))
        self.dummyData.append((["word1", "word2", "word3"], 3, "startDate1", "endDate1"))
        self.dummyData.append((["word1", "word2", "word3"], 2, "startDate2", "endDate2"))
        self.dummyData.append((["word1", "word2", "word3"], 1, "startDate3", "endDate3"))
        self.dummyData.append((["word1", "word2", "word3"], 15, "startDate4", "endDate4"))
        self.dummyData.append((["word1", "word2", "word3"], 16, "startDate5", "endDate5"))
        self.dummyData.append((["word1", "word2", "word3"], 2, "startDate6", "endDate6"))
        self.dummyData.append((["word1", "word2", "word3"], 3, "startDate7", "endDate7"))


    def tearDown(self):
        pass


    def testConstructorData(self):
        gp = TwitterGraphPlotter(self.dummyData)
        self.assertEqual(self.dummyData, gp.data, "The data passed in is not equal to the data upon construction")

    def testConstructorColour(self):
        gp = TwitterGraphPlotter(self.dummyData)
        self.assertEqual(gp.currentColour, gp.colours["no_event"], "The colour is wrong upon construction")




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()