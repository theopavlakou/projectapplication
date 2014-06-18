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
from Queue import Queue
from threading import Thread
import tkMessageBox

class TwitterStreamingApp(object):
    """
    This is the GUI part of the Twitter Streaming Application.
    It takes care of the GUI and the plotting of the graph once points have
    been calculated from its member CalculatorThread.
    """
    def __init__(self):

        self.initialised = False
        self.windowNumbers = []
        self.windowNumber = 0

        # Callback delay (refresh rate) for graph plotting
        self.callbackDelay = 1000
        # TODO: Should not be in this class
        self.previousEigenvalue = 0
        self.stopCallback = False
        self.setupGUI()

    def setupGUI(self):
        """
        Sets up the GUI and starts it up.
        """
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
        self.textBox = Text(self.inputContainer, bg="#CFDAE3", height=40, state=DISABLED, fg="black")
        self.textBox.grid(row=0, column=0, rowspan=self.textBoxRowSpan, columnspan=2, sticky=W+E+N+S)
        self.textBox.tag_add("event_colour", "1.0", "1.4")
        self.textBox.tag_config("event_colour", background="yellow", foreground="red")

        # File input text box
        self.fileInput = Entry(self.inputContainer, width=10)
        self.fileInput.grid(row= self.textBoxRowSpan+1, column=0, columnspan=2, sticky=W+E)
        self.fileInput.delete(0, END)
        #TODO: Change this
#         self.fileInput.insert(0, "Enter file directory for Tweets")
        self.fileInput.insert(0, '/Users/theopavlakou/Documents/Imperial/Fourth_Year/MEng_Project/TWITTER Research/Data (100k tweets from London)/ProjectApplication/src/Tweet_Files/police_murders')


        # Window size text box
        self.windowSizeInput = Entry(self.inputContainer, width=10)
        self.windowSizeInput.grid(row=self.textBoxRowSpan+2, column=0, columnspan=2, sticky=W+E)
        self.windowSizeInput.delete(0, END)
        self.windowSizeInput.insert(0, "Enter number of Tweets per window (Default = 10000)")

        # Shift size text box
        self.batchSizeInput = Entry(self.inputContainer, width=10)
        self.batchSizeInput.grid(row=self.textBoxRowSpan+3, column=0, columnspan=2, sticky=W+E)
        self.batchSizeInput.delete(0, END)
        self.batchSizeInput.insert(0, "Enter number of Tweets to shift by (Default = 1000)")

        # Shift size text box
        self.sparsityInput = Entry(self.inputContainer, width=10)
        self.sparsityInput.grid(row=self.textBoxRowSpan+4, column=0, columnspan=2, sticky=W+E)
        self.sparsityInput.delete(0, END)
        self.sparsityInput.insert(0, "Enter the desired sparsity (Default = 10)")

        # Button Plotting
        self.buttonStart = Button(self.inputContainer, command = self.initiateStartStreaming, width=15, bg="blue")
        self.buttonStart.grid(row=self.textBoxRowSpan+5, column=1, sticky=W+E)
        self.buttonStart.focus_force()
        self.buttonStart.configure(text = "Start Streaming!")

        # Button Got Files
        self.buttonFiles = Button(self.inputContainer, command= self.initialise, width=15)
        self.buttonFiles.grid(row=self.textBoxRowSpan+5, column=0, sticky=W+E)
        self.buttonFiles.configure(text = "Load Files")

        # Button Quit
        self.buttonQuit = Button(self.inputContainer, command= self.quit, width=30)
        self.buttonQuit.grid(row =self.textBoxRowSpan+6, column=0, columnspan=2, sticky=W+E)
        self.buttonQuit.configure(text = "Quit")

        self.root.mainloop()

    def quit(self):
        sys.exit()

    def printToTextBox(self, string):
        """
        Prints to the text box of the GUI.
        Inputs:
            string:    The string to be printed to the text box.
        """
        self.textBox.configure(state=NORMAL)
        self.textBox.insert(INSERT,string+"\n")
        self.textBox.configure(state=DISABLED)

    def initialiseThresholds(self, eigenvalueThreshold, dotProductThreshold):
        """
        Initialise the thresholds of the eigenvalue and the dot product.
        These are used to figure out which colour the graph should plot with.
        Inputs:
            eigenvalueThreshold:    Threshold for the eigenvalue associated with
                                    the principal components.
            dotProductThreshold:    Threshold for the dot product between the
                                    previous principal component and the current.
        """
        self.eigenvalueThreshold = eigenvalueThreshold
        # This should be between 0 and 1 and gives the
        # similarity of two principal components.
        self.dotProductThreshold = dotProductThreshold

    def initialise(self):
        """
        Takes all the inputs from the GUI and sets up member variables.
        Must be called before startStreaming.
        """

        # If already initialised, do nothing
        if self.initialised == True:
            self.printToTextBox("Cannot re-initialise. Must quit and then start again.")
            return
        # TODO: Don't hard code these
        # Are needed to print the graphs.
        self.initialiseThresholds(180, 0.85)


        # TODO: Must have better user checking than this
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
            print("------ Setting shift size to 1000. ------")
            self.batchSize = 1000

        try:
            self.desiredSparsity = int(self.sparsityInput.get())
        except ValueError as ve:
            print("------ " + str(ve) + " ------ ")
            print("------ Could not convert " + self.sparsityInput.get() + " to an integer. ------")
            print("------ Setting desired sparsity to 10 ------")
            self.desiredSparsity = 10

        self.initialiseCalculatorThread()
        self.initialised = True

    def printEvent(self, pCWords, startDate, endDate):
        """
        Print an event that occurs to the text box of the GUI.
        Inputs:
            pCWords:        A list of strings of words associated with the
                            sparse principal component.
            startDate:      The date of the first Tweet in the current window.
            endDate:        The date of the last Tweet in the current window.
        """
        pCWordsString = ""
        for word in pCWords:
            pCWordsString += word + ", "
        pCWordsString = pCWordsString[:-2]
        self.printToTextBox("===========================================================================")
        self.printToTextBox("Event with words: " + pCWordsString)
        self.printToTextBox("At: " + startDate+ " - " + endDate)
        self.printToTextBox("===========================================================================")

    def startStreaming(self):
        """
        Checks whether the shared queue with the calculatorThread has a new
        element (i.e. a new calculation has finished) and then plots the point.
        Keeps being called by the GUI once it is called the first time.
        """
        if not self.sharedQueue.empty():
            self.windowNumbers.append(self.windowNumber)
            self.windowNumber += 1
            # TODO: Should actually have a whole new GraphPlotter class for this
            item = self.sharedQueue.get_nowait()
            if isinstance(item, StopCallbackCommand):
                self.stopCallback = True
            else:
                (pCWords, eigenvalue, dotProductOldCurrent, startDate, endDate) = item
                if eigenvalue > self.eigenvalueThreshold:

                    if dotProductOldCurrent < self.dotProductThreshold:
                        self.graph.scatter(self.windowNumber, eigenvalue, c="red")
                        self.printEvent(pCWords, startDate, endDate)
                    else:
                        if self.previousEigenvalue <= self.eigenvalueThreshold:
                            self.graph.scatter(self.windowNumber, eigenvalue, c="red")
                            self.printEvent(pCWords, startDate, endDate)
                        else:
                            self.graph.scatter(self.windowNumber, eigenvalue, c="yellow")
                else:
                    self.graph.scatter(self.windowNumber, eigenvalue, c="blue")
                self.previousEigenvalue = eigenvalue
                self.canvas.show()
        else:
            pass

        if self.stopCallback == False:
            # Calls again after self.callbackDelay ms
            self.root.after(self.callbackDelay, self.startStreaming)
        else:
            self.printToTextBox("---- Finished Streaming ----")

    def initiateStartStreaming(self):
        if not self.initialised:
            self.onError()
            return
        self.calculatorThread.start()
        self.printToTextBox("---- Starting to stream ----")
        self.startStreaming()

    def initialiseCalculatorThread(self):
        self.tweetRetriever = TweetRetriever(self.jsonFileName, self.sizeOfWindow, self.batchSize)
        self.tweetRetriever.initialise()
        self.tPAlgorithm = TPowerAlgorithm()
        # TODO: Don't hard code number of words
        numberOfWords = 3000
        self.matrixBuilder = MatrixBuilder(self.sizeOfWindow, numberOfWords)
        self.sharedQueue = Queue()
        self.calculatorThread = CalculatorThread(self.sharedQueue, self.desiredSparsity, self.tweetRetriever, self.tPAlgorithm, self.matrixBuilder)
        self.calculatorThread.daemon = True

    def onError(self):
        tkMessageBox.showerror("Error", "You have not loaded the files yet")

class CalculatorThread(Thread):
    """
    Performs the algorithmic part of the algorithm. It collects the Tweets, builds
    the matrix and then calculates the sparse principal components for the window.
    It keeps doing this, adding the results to a queue shared with the GUI.
    It runs as a separate thread so that the GUI doesn't freeze while it is
    calculating new points.
    """
    def __init__(self, sharedQueue, desiredSparsity, tweetRetriever, tPAlgorithm, matrixBuilder):
        Thread.__init__(self)
        self.queue = sharedQueue
        self.tweetRetriever = tweetRetriever
        self.tPAlgorithm = tPAlgorithm
        self.matrixBuilder = matrixBuilder
        self.desiredSparsity = desiredSparsity
        # TODO: Do not hard code this
        self.numberOfWords = 3000
        ####################################################
        #  Initialize the objects
        ####################################################
        # TODO: Get rid of ./Pickles as this isn't in the repository.
        # The output pickle file name. CHANGE to the desired location.
        self.pickleFileName = "./Pickles/pCPickle.pkl"
        self.verbose = 1

        self.currentWindowNumber = 0

    def loadTweets(self):
        """
        Loads the Tweets from the file specified.
        Outputs:
            tweetSet:    The set of Tweets from the current window.
            oldBatch:    Set of Tweets in previous window that aren't in the
                         current window.
        """
        if self.verbose > 1:
            print("--- Loading Tweets ---")
        (tweetSet, oldBatch) = self.tweetRetriever.getNextWindow()
        if self.verbose == 3:
            print("--- Number of Tweets: " + str(len(tweetSet)) + " ---")
        if self.verbose > 1:
            print("--- Finished loading Tweets ---")
        return (tweetSet, oldBatch)

    def getBagOfWords(self, tweetSet, oldBatch):
        """
        Creates the Bag-Of-Words using the current Tweets and the previous window.
        Inputs:
            tweetSet:    Set of current Tweets.
            oldBatch:    Set of Tweets in previous window that aren't in the
                         current window.
        Outputs:
            wordDictCurrent:     Bag-Of-Words for current window.
            indexChanges:        A dictionary which maps the indices of the current
                                 Bag-of-Words to the indices of the old
                                 Bag-of-Words for the words which are
                                 common to both. The keys are the current indices
                                 and the values are the old indices.
        """
        if self.verbose > 1:
            print("--- Loading most common words in the Tweets ---")
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
        if self.verbose > 1:
            print("--- Finished loading most common words in the Tweets ---")
        return (wordDictCurrent, indexChanges)

    def populateDataMatrix(self, tweetSet, wordDictCurrent):
        """
        Populates the data matrix with columns the indices of the words in the
        current Bag-Of-Words and rows the Tweets.
        Inputs:
            tweetSet:            The set of Tweets from the current window.
            wordDictCurrent:     Bag-Of-Words for current window.

        """
        if self.verbose > 1:
            print("--- Populating matrix ---")
        tweetNumber = 0

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

        if self.verbose > 1:
            print("--- Finished populating matrix ---")

    def getPCWordsAndIndicesFromPC(self, sparsePC, wordDictCurrent):
        """
        Gets the words and the indices of the words that the current principal
        component refers to.
        Inputs:
            wordDictCurrent:     Bag-Of-Words for current window.
            sparsePC:            Sparse principal component for current window.
        Outputs:
            pCWords:            A list of strings with the words associated with
                                the current principal component.
            smallPC:            A dictionary with key the index of the word in
                                and the current sparse principal component and
                                value the weighting of the loading of the word.

        """
        pCWords = []
        smallPC = {}
        for index in sparsePC.nonzero()[0]:
            smallPC[index] = sparsePC[index].todense()[0,0]
            for word, rank in wordDictCurrent.iteritems():
                if rank == index:
                    pCWords.append(word)
        return (pCWords, smallPC)

    def getDotProductOldCurrent(self, indexChanges, smallPCOld, smallPC):
        """
        Gets the dot product of the old principal component and the current
        principal component.
        Inputs:
            indexChanges:       A dictionary which maps the indices of the current
                                Bag-of-Words to the indices of the old
                                Bag-of-Words for the words which are
                                common to both. The keys are the current indices
                                and the values are the old indices.
            smallPCOld:         A dictionary with key the index of the word in
                                and the old sparse principal component and
                                value the weighting of the loading of the word.
            smallPC:            A dictionary with key the index of the word in
                                and the current sparse principal component and
                                value the weighting of the loading of the word.
        Outputs:
            dotProductOldCurrent:    The dot product between the old and current
                                     principal component.

        """
        dotProductOldCurrent = 0
        if self.currentWindowNumber > 1:
            if self.verbose > 3:
                print("--- Printing index changes ---")
                print(indexChanges)
            for index in smallPC.keys():
                if indexChanges.has_key(index):
                    if smallPCOld.has_key(indexChanges[index]):
                        dotProductOldCurrent += smallPC[index]*smallPCOld[indexChanges[index]]
        return dotProductOldCurrent


    def run(self):
        """
        Runs the algorithm. This is run on its own thread and the results are
        pushed onto a shared queue so as to not freeze the GUI.
        """
        while True:

            toSaveToPickle = []
            smallPCOld = {}
            ####################################################
            #  Initialize times associated with various parts
            #  of the code.
            ####################################################
            tLoadTweets = 0
            tLoadCommonWords = 0
            tPopMat = 0
            tBuildCooccurenceMatrix = 0
            tCalculateSPCA = 0

            while not self.tweetRetriever.eof:
                self.currentWindowNumber += 1
                tIterationStart = time.time()
                ################
                # Load Tweets
                ################
                tLoadTweetsStart = time.time()
                (tweetSet, oldBatch) = self.loadTweets()
                tLoadTweetsEnd = time.time()
                tLoadTweets += (tLoadTweetsEnd - tLoadTweetsStart)/10

                ########################################################
                #  Make a list of the 3000 most common words.
                #  This will be the Bag-Of-Words.
                ########################################################

                tLoadCommonWordsStart = time.time()
                (wordDictCurrent, indexChanges) = self.getBagOfWords(tweetSet, oldBatch)
                tLoadCommonWordsEnd = time.time()
                tLoadCommonWords += (tLoadCommonWordsEnd - tLoadCommonWordsStart)/10

                ########################################################
                #  Create Sparse Matrix
                ########################################################
                self.matrixBuilder.resetMatrix()

                ########################################################
                # Get the start and end date of the current tweet set
                ########################################################
                startDate = tweetSet[0].date
                endDate = tweetSet[len(tweetSet)-1].date

                ############################################################################################
                #  Populate the S matrix. This is the matrix with rows the Tweets and columns
                #  the Bag-Of-Words.
                ############################################################################################
                tPopMatStart = time.time()
                self.populateDataMatrix(tweetSet, wordDictCurrent)
                tPopMatEnd = time.time()
                tPopMat += (tPopMatEnd - tPopMatStart)/10

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
                (pCWords, smallPC) = self.getPCWordsAndIndicesFromPC(sparsePC, wordDictCurrent)

                if self.verbose > 3:
                    print("--- Printing small PCs --- ")
                    print(smallPC)
                    print(smallPCOld)

                ###########################################################################
                # Get the dot product between the old principal component and the current.
                ###########################################################################
                dotProductOldCurrent = self.getDotProductOldCurrent(indexChanges, smallPCOld, smallPC)

                if self.verbose > 3:
                    print("--- Printing dot product ---")
                    print(dotProductOldCurrent)

                smallPCOld = smallPC



                #################################################################
                #  Append the data to be saved in the pickle file.
                #################################################################
                dataPoint = (pCWords, eigenvalue, dotProductOldCurrent, startDate, endDate)
                toSaveToPickle.append(dataPoint)
                self.queue.put(dataPoint)
                tIterationEnd = time.time()

                if self.verbose > 1:
                    print ("Time for iteration: " + str(tIterationEnd - tIterationStart))



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
                print("Average time per iteration = " + str(totalTime/len(toSaveToPickle)))
            outputPickle = open(self.pickleFileName, 'wb')
            pickle.dump(toSaveToPickle, outputPickle)
            outputPickle.close()
            self.queue.put(StopCallbackCommand())
            print("--- End ---")

            break

class StopCallbackCommand:
    def __init__(self):
        self.description = "Stopping callback..."

m = TwitterStreamingApp()
