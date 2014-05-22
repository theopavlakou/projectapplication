'''
Created on 21 May 2014

@author: theopavlakou
'''
###########################################################################################################################
## A parser for the twitter data file with all the JSON data. Reads in the JSON data and prints out a matrix of the form:
# This prints out to the file in the following format:
# 1, 5, 7, 8
# 2,
# 3, 6
# which means that Tweet 1 contains words {5, 7, 8}, Tweet 2 contains no words in
# the bag of words and Tweet 3 contains word {6}.
############################################################################################################################

from DictionaryOfWords import DictionaryOfWords
from TweetRetriever import TweetRetriever
from MatrixBuilder import MatrixBuilder
from TPowerAlgorithm import TPowerAlgorithm

####################################################
##  The file containing the Tweets as JSONs
####################################################
jsonFileName = '/Users/theopavlakou/Documents/Imperial/Fourth_Year/MEng_Project/TWITTER Research/Data (100k tweets from London)/ProjectApplication/src/twitter_data'

####################################################
##  Initialize
####################################################
# TODO Change this to be smaller than the actual file.
sizeOfWindow = 10000000
batchSize = 5000
tweetRetriever = TweetRetriever(jsonFileName, sizeOfWindow, batchSize)
tweetRetriever.initialise()
tPAlgorithm = TPowerAlgorithm()
verbose = 3
####################################################
##  Load the Tweets from the file
####################################################
while not tweetRetriever.eof:
    print("--- Loading Tweets ---")
    tweetSet = tweetRetriever.getNextWindow()
    if verbose == 3:
        print("--- Number of Tweets: " + str(len(tweetSet)) + " ---")
    print("--- Finished loading Tweets ---")

    ########################################################
    ##  Make a list of the 3000 most common words in the
    ##  Tweets which will be the columns of the matrix.
    ########################################################
    print("--- Loading most common words in the Tweets ---")
    dictOfWords = DictionaryOfWords()
    for tweet in tweetSet:
        dictOfWords.addFromSet(tweet.listOfWords())
    listOfWords = dictOfWords.getMostPopularWordsAndOccurrences(3000)
#     wordRank = dictOfWords.getMostPopularWordsAndRank(3000)
    print("--- Finished loading most common words in the Tweets ---")

    ########################################################
    ##  Open the file to output the words with their index.
    ########################################################
    print("--- Opening file to output index of words to ---")
    wordsFile = open("cwi", "w")
    # Matlab starts indexing from 1
    i = 1
    for (word, occurrence) in listOfWords:
        if isinstance(word, unicode):
            word = word.encode('utf-8','ignore')
        else:
            print(word)
        wordsFile.write(str(i) + " " + word + " " + str(occurrence) + "\n")
        i = i + 1
    print("--- Closing file to output index of words to ---")
    wordsFile.close()
    ########################################################
    ##  Create Sparse Matrix
    ########################################################
    matrixBuilder = MatrixBuilder(sizeOfWindow, len(listOfWords))

    ############################################################################################
    # For each Tweet, find the index of the words that correspond to the words in the Tweet.
    ############################################################################################
    print("--- Populating matrix ---")
    tweetNumber = 0
    for tweet in tweetSet:
        # Get the list of words in the tweet
        tweetWordList = tweet.listOfWords()
        # The first number is the index of the tweet (the row number)
        # Check for each word in the list of unique words, if it is in the Tweet, then print the index of the word
        for wordNumber in range(len(listOfWords)):
            if listOfWords[wordNumber][0] in tweetWordList:
                matrixBuilder.addElement(tweetNumber, wordNumber, 1)
        # Next row
        tweetNumber = tweetNumber + 1
    print("--- Finished populating matrix ---")

    ############################################################################################
    # With the matrix populated run the algorithm on it
    ############################################################################################
    cooccurrenceMatrix = matrixBuilder.getCooccurrenceMatrix()
    [sparsePC, eigenvalue] = tPAlgorithm.getSparsePC(cooccurrenceMatrix, 5)
    print("--- Sparse Eigenvector ---")
    print(sparsePC.nonzero()[0])
    pCWords = [listOfWords[index][0] for index in sparsePC.nonzero()[0]]
#     for index in sparsePC.nonzero()[0]:
#         print (listOfWords[index][0])
    print(pCWords)
    print("--- Eigenvalue ---")
    print(eigenvalue)

print("--- End ---")


