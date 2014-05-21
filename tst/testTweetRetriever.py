'''
Created on 21 May 2014

@author: theopavlakou
'''
import unittest
from TweetRetriever import TweetRetriever

class TestTweetRetriever(unittest.TestCase):


    def setUp(self):
        jsonFileName = '/Users/theopavlakou/Documents/Imperial/Fourth_Year/MEng_Project/TWITTER Research/Data (100k tweets from London)/ProjectApplication/src/test_jsons'
        sizeOfWindow = 10
        batchSize = 5
        self.tweetRetriever = TweetRetriever(jsonFileName, sizeOfWindow, batchSize)
        self.tweetRetriever.initialise()
        pass


    def tearDown(self):
        pass


    def testReturnsMinusOneUponCompletion(self):
        """ A test to ensure that the sliding window works correctly. It makes sure that
        for a file of 15, a window size of 10 and a batch increment of 5, the 4th call
        to getNextWindow will return -1. """
        # Returns lines 1 to 10
        self.assertTrue(self.tweetRetriever.getNextWindow() != -1, "returned -1")
        # Returns lines 6 to 15
        self.assertTrue(self.tweetRetriever.getNextWindow() != -1, "returned -1")
        # Returns lines 6 to 15 again since it has run out of JSONS but will still
        # return the same window as before. The eof flag is set though.
        self.assertTrue(self.tweetRetriever.getNextWindow() != -1, "returned -1")
        # Fails here
        self.assertTrue(self.tweetRetriever.getNextWindow() == -1, "did not return -1")
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()