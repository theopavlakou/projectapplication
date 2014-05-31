'''
Created on 30 May 2014

@author: theopavlakou
'''
import unittest
from DictionaryComparator import DictionaryComparator


class Test(unittest.TestCase):


    def setUp(self):
        self.dictOld = {'theo': 0, 'pamela': 1, 'run': 2, 'sleep': 3}
        self.dictCurrent = {'theo': 0, 'jump': 1, 'pamela': 2, 'eat': 3}
        self.dc = DictionaryComparator(self.dictOld, self.dictCurrent)

        pass

    def tearDown(self):
        pass

    def testGetCurrentWordsNotInOld(self):
        self.assertEqual(self.dc.getCurrentWordsNotInOld(), {'jump', 'eat'})

    def testGetOldWordsNotInCurrent(self):
        self.assertEqual(self.dc.getOldWordsNotInCurrent(), {'run', 'sleep'})

    def testGetCommonWords(self):
        self.assertEqual(self.dc.getCommonWords(), {'theo', 'pamela'})

    def testGetIndexChangesFromOldToCurrent(self):
        self.assertEqual(self.dc.getIndexChangesFromOldToCurrent(), {0:0, 1:2})

    def testGetIndexOfWordsNotInOld(self):
        self.assertEqual(self.dc.getIndexOfWordsNotInOld(), {3, 1})

    def testGetIndexOfWordsNotInCurrent(self):
        self.assertEqual(self.dc.getIndexOfWordsNotInCurrent(), {2, 3})

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()