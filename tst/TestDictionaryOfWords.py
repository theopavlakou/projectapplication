'''
Created on 30 May 2014

@author: theopavlakou
'''
import unittest
from DictionaryOfWords import DictionaryOfWords

class TestDictionaryOfWords(unittest.TestCase):


    def setUp(self):
        self.words = ["theo", "is", "very", "cool", "theo", "cool", "cool"]
        self.otherWords = ["john", "what", "very", "cool", "john", "cool", "cool"]
        pass


    def tearDown(self):
        pass


    def testAddToDictionary(self):
        dToTest = DictionaryOfWords()
        for word in self.words:
            dToTest.addToDictionary(word)
        self.assertEqual(dToTest.dict,{'theo': 2, 'very':1, 'cool':3, 'is':1}, "Not populated correctly")

    def testAddFromSet(self):
        dToTest = DictionaryOfWords()
        dToTest.addFromSet(self.words)
        self.assertEqual(dToTest.dict,{'theo': 2, 'very':1, 'cool':3, 'is':1}, "Not populated correctly")

    def testGetMostPopularWordsAndRank(self):
        dToTest = DictionaryOfWords()
        dToTest.addFromSet(self.words)
        self.assertEqual(dToTest.getMostPopularWordsAndRank(2), {'theo':1, 'cool':0}, "The ranking system doesn't work")

    def testGetDifferenceInWords(self):
        pass
#         dToTest = DictionaryOfWords()
#         dToTest.addFromSet(self.words)
#         self.assertEqual(dToTest.getMostPopularWordsAndRank(2), {'theo':1, 'cool':0}, "The ranking system doesn't work")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()