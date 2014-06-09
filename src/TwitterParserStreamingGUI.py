'''
Created on 9 Jun 2014

@author: theopavlakou
'''

###########################################################################################################################
## A parser for the twitter data file with all the JSON data. Reads in the JSON
## data, each line representing a Tweet, in a streaming manner and finds words
## that most probably best describe an event that is taking place.
## Each window alongside the set of words, the score and the dates are stored
## in a pickle file.
############################################################################################################################
from DictionaryOfWords import DictionaryOfWords
from TweetRetriever import TweetRetriever
from MatrixBuilder import MatrixBuilder
from TPowerAlgorithm import TPowerAlgorithm
import time
import pickle
from copy import deepcopy
from DictionaryComparator import DictionaryComparator
import matplotlib.pyplot as plt
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import os


class TwitterStreamingApp(object):

    def __init__(self):

        self.initialised = False

        #####################################################
        #####################################################
        ################ Setup GUI stuff ####################
        #####################################################
        #####################################################
        self.root = Tk()
        self.height = 1360
        self.width = 820
        self.root.geometry(str(self.height)+"x"+str(self.width)+"+40+40")

        # Graph
        self.figure = Figure(figsize=(5,4), dpi=100)
        self.graph = self.figure.add_subplot(111)
        self.graph.set_title('Eigenvalue vs Window Number')
        self.graph.set_xlabel('Window Number')
        self.graph.set_ylabel('Eigenvalue')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=LEFT,fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack( fill=BOTH, expand=1)

        ######################################################
        # Input Frame
        ######################################################
        self.inputContainer = Frame(self.root)
        self.inputContainer.pack(side=TOP,fill=X, pady=4)
        self.textBoxRowSpan = 6

        # Text
        self.textBox = Text(self.inputContainer, bg="#CFDAE3", height=40, state=DISABLED)
        self.textBox.grid(row=0, column=0, rowspan=self.textBoxRowSpan, columnspan=2, sticky=W+E+N+S)

        # File input text box
        self.fileInput = Entry(self.inputContainer, width=10)
        self.fileInput.grid(row= self.textBoxRowSpan+1, column=0, columnspan=2, sticky=W+E)
        self.fileInput.delete(0, END)
        self.fileInput.insert(0, "Enter file directory for Tweets")


        # Window size text box
        self.windowSizeInput = Entry(self.inputContainer, width=10)
        self.windowSizeInput.grid(row=self.textBoxRowSpan+2, column=0, columnspan=2, sticky=W+E)
        self.windowSizeInput.delete(0, END)
        self.windowSizeInput.insert(0, "Enter number of Tweets per window")

        # Shift size text box
        self.batchSizeInput = Entry(self.inputContainer, width=10)
        self.batchSizeInput.grid(row=self.textBoxRowSpan+3, column=0, columnspan=2, sticky=W+E)
        self.batchSizeInput.delete(0, END)
        self.batchSizeInput.insert(0, "Enter number of Tweets to shift by")

        # Shift size text box
        self.sparsityInput = Entry(self.inputContainer, width=10)
        self.sparsityInput.grid(row=self.textBoxRowSpan+4, column=0, columnspan=2, sticky=W+E)
        self.sparsityInput.delete(0, END)
        self.sparsityInput.insert(0, "Enter the desired sparsity")

        # Button Plotting
        self.button1 = Button(self.inputContainer, command = self.startStreaming, width=15)
        self.button1.grid(row=self.textBoxRowSpan+5, column=0, sticky=W+E)
        self.button1.focus_force()
        self.button1.configure(text = "Start Plotting!")

        # Button Got Files
        self.buttonFiles = Button(self.inputContainer, command= self.initialise, width=15)
        self.buttonFiles.grid(row=self.textBoxRowSpan+5, column=1, sticky=W+E)
        self.buttonFiles.configure(text = "Print this!")
        self.root.mainloop()

    def printToTextBox(self, string):
        self.textBox.configure(state=NORMAL)
        self.textBox.insert(INSERT,string+"\n")
        self.textBox.configure(state=DISABLED)

    def printInputs(self):
        v = self.fileInput.get()+"\n"
        self.printToTextBox(v)

    def initialise(self):
        ####################################################
        #  Initialize the objects
        ####################################################
        # TODO: Get rid of ./Pickles as this isn't in the repository.
        # The output pickle file name. CHANGE to the desired location.
        self.pickleFileName = "./Pickles/pCPickle.pkl"
        # Controls the message output. A higher value means that more will be displayed.
        self.verbose = 3
        #####################################################
        # Initialise thresholds.
        # These control whether the words of the pcs should be
        # printed.
        #####################################################
        self.eigenvalueThreshold = 130
        # This should be between 0 and 1 and gives the
        # similarity of two principal components.
        self.dotProductThreshold = 0.85
        self.smallPCOld = {}
        # Get the file name from the text box
        fileName = self.fileInput.get()
        if os.path.exists(fileName):
            self.jsonFileName = fileName
            self.printToTextBox(self.jsonFileName + " is a valid path")
        else:
            # TODO: Make a popup box appear here instead.
            self.printToTextBox("== Please input a directory with Tweets in it ==\n")
            self.printToTextBox(fileName + ' is not a valid path')
            return

        try:
            self.sizeOfWindow = int(self.windowSizeInput.get())
        except ValueError as ve:
            print("------ " + str(ve) + " ------ ")
            print("------ Could not convert " + self.windowSizeInput.get() + " to an integer. ------")
            print("------ Setting size of window to 10000. ------")
            self.sizeOfWindow = 10000

        try:
            self.batchSize = int(self.batchSizeInput.get())
        except ValueError as ve:
            print("------ " + str(ve) + " ------ ")
            print("------ Could not convert " + self.batchSizeInput.get() + " to an integer. ------")
            print("------ Setting size of window to 10000. ------")
            self.batchSize = 1000

        try:
            self.desiredSparsity = int(self.sparsityInput.get())
        except ValueError as ve:
            print("------ " + str(ve) + " ------ ")
            print("------ Could not convert " + self.sparsityInput.get() + " to an integer. ------")
            print("------ Setting size of window to 10000. ------")
            self.desiredSparsity = 10

        self.numberOfWords = 3000

        self.tweetRetriever = TweetRetriever(self.jsonFileName, self.sizeOfWindow, self.batchSize)
        self.tweetRetriever.initialise()
        self.tPAlgorithm = TPowerAlgorithm()
        self.matrixBuilder = MatrixBuilder(self.sizeOfWindow, self.numberOfWords)
        self.printInputs()
        self.initialised = True

    def startStreaming(self):
        if not self.initialised:
            # TODO: make a popup box here
            return
        ####################################################
        #  Load the Tweets from the file
        ####################################################
        toSave = []
        count = 0

        ####################################################
        #  Initialize times associated with various parts
        #  of the code.
        ####################################################
        tLoadTweets = 0
        tLoadCommonWords = 0
        tPopMat = 0
        tBuildCooccurenceMatrix = 0
        tCalculateSPCA = 0
        eigenvalues = []
        while not self.tweetRetriever.eof:
            count+=1
            tIterationStart = time.time()
            if self.verbose > 1:
                print("--- Loading Tweets ---")
            tLoadTweetsStart = time.time()
            (tweetSet, oldBatch) = self.tweetRetriever.getNextWindow()
            if self.verbose == 3:
                print("--- Number of Tweets: " + str(len(tweetSet)) + " ---")
            if self.verbose > 1:
                print("--- Finished loading Tweets ---")
            tLoadTweetsEnd = time.time()
            tLoadTweets += (tLoadTweetsEnd - tLoadTweetsStart)/10

            ########################################################
            #  Make a list of the 3000 most common words in the
            #  Tweets which will be the columns of the matrix.
            #  The Bag-Of-Words.
            ########################################################
            if self.verbose > 1:
                print("--- Loading most common words in the Tweets ---")
            tLoadCommonWordsStart = time.time()

            dictOfWordsOld = DictionaryOfWords()

            # This part of the count will be common to both the current and previous window
            for tweet in tweetSet[0:-len(oldBatch)]:
                dictOfWordsOld.addFromSet(tweet.listOfWords())

            # Ensure a copy is made, not just a reference and also to the dictionary in it => deepcopy
            dictOfWordsCurrent = deepcopy(dictOfWordsOld)

            # The old dictionary of words
            for tweet in oldBatch:
                dictOfWordsOld.addFromSet(tweet.listOfWords())

            # The current dictionary of words
            for tweet in tweetSet[-len(oldBatch):]:
                dictOfWordsCurrent.addFromSet(tweet.listOfWords())

            wordDictOld = dictOfWordsOld.getMostPopularWordsAndRank(self.numberOfWords)
            wordDictCurrent = dictOfWordsCurrent.getMostPopularWordsAndRank(self.numberOfWords)
            dictionaryComparator = DictionaryComparator(wordDictOld, wordDictCurrent)
            indexChanges = dictionaryComparator.getIndexChangesFromCurrentToOld()

            tLoadCommonWordsEnd = time.time()
            tLoadCommonWords += (tLoadCommonWordsEnd - tLoadCommonWordsStart)/10

            if self.verbose > 1:
                print("------ That took " + str(tLoadCommonWordsEnd - tLoadCommonWordsStart) + " seconds to complete ------")
                print("--- Finished loading most common words in the Tweets ---")
        #     ########################################################
        #     #  Open the file to output the words with their index.
        #     ########################################################
        #     print("--- Opening file to output index of words to ---")
        #     wordsFile = open("Data/cwi", "w")
        #     # Matlab starts indexing from 1
        #     i = 1
        #     for (word, occurrence) in listOfWords:
        #         if isinstance(word, unicode):
        #             word = word.encode('utf-8','ignore')
        #         else:
        #             print(word)
        #         wordsFile.write(str(i) + " " + word + " " + str(occurrence) + "\n")
        #         i = i + 1
        #     print("--- Closing file to output index of words to ---")
        #     wordsFile.close()

            ########################################################
            #  Create Sparse Matrix
            ########################################################
            self.matrixBuilder.resetMatrix()

            ############################################################################################
            #  Populate the S matrix. This is the matrix with rows the Tweets and columns
            #  the Bag-Of-Words.
            ############################################################################################
            if self.verbose > 1:
                print("--- Populating matrix ---")
            tPopMatStart = time.time()
            tweetNumber = 0
            # Get the start and end date of the current tweet set
            startDate = tweetSet[0].date
            endDate = tweetSet[len(tweetSet)-1].date
            # Get the current Bag-Of-Words
            currentBagOfWords = wordDictCurrent.keys()

            for tweet in tweetSet:
                # Get the list of words in the tweet
                tweetWordList = tweet.listOfWords()
                for word in tweetWordList:
                    if word in currentBagOfWords:
                        self.matrixBuilder.addElement(tweetNumber, wordDictCurrent[word], 1)
                # Next row
                tweetNumber = tweetNumber + 1
            tPopMatEnd = time.time()
            tPopMat += (tPopMatEnd - tPopMatStart)/10
            if self.verbose > 1:
                print("--- Finished populating matrix ---")
                print("------ That took " + str(tPopMatEnd - tPopMatStart) + " seconds to complete ------")

            ############################################################################################
            # Now calculate the Co-occurrence matrix.
            ############################################################################################
            tBuildCooccurenceMatrixStart = time.time()
            cooccurrenceMatrix = self.matrixBuilder.getCooccurrenceMatrix()
            tBuildCooccurenceMatrixEnd = time.time()
            tBuildCooccurenceMatrix += (tBuildCooccurenceMatrixEnd - tBuildCooccurenceMatrixStart)/10

            ############################################################################################
            # Run the Sparse PCA algorithm on the Co-occurrence matrix.
            ############################################################################################
            tCalculateSPCAStart = time.time()
            [sparsePC, eigenvalue] = self.tPAlgorithm.getSparsePC(cooccurrenceMatrix, self.desiredSparsity)
            tCalculateSPCAEnd = time.time()
            tCalculateSPCA += (tCalculateSPCAEnd - tCalculateSPCAStart)/10
            if self.verbose > 1:
                print("--- Sparse Eigenvector ---")
                print(sparsePC.nonzero()[0])

            ###########################################################################
            # Save all the words corresponding to the indices of the supports returned.
            ###########################################################################
            pCWords = []
            smallPC = {}
            for index in sparsePC.nonzero()[0]:
                smallPC[index] = sparsePC[index].todense()[0,0]
                for word, rank in wordDictCurrent.iteritems():
                    if rank == index:
                        pCWords.append(word)
            if self.verbose > 3:
                print("--- Printing small PCs --- ")
                print(smallPC)
                print(self.smallPCOld)

            ###########################################################################
            # Get the dot product between the old principal component and the current.
            ###########################################################################
            dotProductOldCurrent = 0
            if count > 1:
                if self.verbose > 3:
                    print("--- Printing index changes ---")
                    print(indexChanges)
                for index in smallPC.keys():
                    if indexChanges.has_key(index):
                        if self.smallPCOld.has_key(indexChanges[index]):
                            dotProductOldCurrent += smallPC[index]*self.smallPCOld[indexChanges[index]]

            if self.verbose > 3:
                print("--- Printing dot product ---")
                print(dotProductOldCurrent)

            smallPCOld = smallPC
            if self.verbose > 1 or (eigenvalue > self.eigenvalueThreshold and dotProductOldCurrent < self.dotProductThreshold):
                print(pCWords)
                print("--- Eigenvalue ---")
                print(eigenvalue)
                print("--- Start Date - End Date ---")
                print(startDate + " - " + endDate)

            #################################################################
            #  Append the data to be saved in the pickle file.
            #################################################################
            toSave.append((pCWords, eigenvalue, startDate, endDate))
            tIterationEnd = time.time()
            if self.verbose > 1:
                print ("Time for iteration: " + str(tIterationEnd - tIterationStart))

            ##############################################
            # Graph plotting stuff
            ##############################################
            #TODO: Make it such that it doesn't freeze.
            eigenvalues.append(eigenvalue)
            if eigenvalue > self.eigenvalueThreshold:
                if dotProductOldCurrent < self.dotProductThreshold:
                    self.graph.scatter(count,eigenvalue, c="red")
                else:
                    self.graph.scatter(count,eigenvalue, c="yellow")
            else:
                self.graph.scatter(count,eigenvalue, c="blue")

            self.canvas.show()

        totalTime = tLoadCommonWords + tLoadTweets + tPopMat + tBuildCooccurenceMatrix + tCalculateSPCA

        ###########################################################
        #  Print final statistics for time spent in each portion
        #  of the code.
        ###########################################################
        if self.verbose > 1:
            print("Average proportion of time loading Tweets = " + str(tLoadTweets/totalTime))
            print("Average proportion of time loading common words = " + str(tLoadCommonWords/totalTime))
            print("Average proportion of time populating matrix = " + str(tPopMat/totalTime))
            print("Average proportion of time building co-occurrence matrix = " + str(tBuildCooccurenceMatrix/totalTime))
            print("Average proportion of time calculating Sparse PCA = " + str(tCalculateSPCA/totalTime))
            print("Average time per iteration = " + str(totalTime/len(toSave)))
        outputPickle = open(self.pickleFileName, 'wb')
        pickle.dump(toSave, outputPickle)
        outputPickle.close()
        print("--- End ---")


m = TwitterStreamingApp()
