'''
Created on 23 May 2014

@author: theopavlakou
'''
import unittest
import json
from Tweet import Tweet

class TestTweet(unittest.TestCase):


    def setUp(self):
        self.decoder = json.JSONDecoder()
        self.jsons = []
        self.jsonFile = open("/Users/theopavlakou/Documents/Imperial/Fourth_Year/MEng_Project/TWITTER Research/Data (100k tweets from London)/ProjectApplication/src/twitter_data", 'r')
        self.jsons.append(self.jsonFile.readline())
        self.jsons.pop()
        self.jsons.append(self.jsonFile.readline())
        self.jsons.append(self.jsonFile.readline())
        pass


    def tearDown(self):
        pass


    def testTweetConstructor(self):
        jsonObject = self.decoder.decode(self.jsons[0])
        tweet = Tweet(jsonObject["text"], jsonObject["created_at"])
        print(tweet.content)
        print(tweet.date)
        self.assertTrue(tweet.content != "", "No content")
        self.assertTrue(tweet.date != "", "No date")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()