projectapplication
==================
There are three folders in the parent directory: mains, src, tst. For user purposes only src is necessary. The main file in the src directory is TwitterParserStreaming.py.

To run the code, it can either be opened in an IDE such as LiClipse or alternatively can be run from the command line. To do this Python 2.6 at least must be installed. To find out more about how to do this go to https://www.python.org/download/. 

In the command line, go to the directory where the repository has been cloned. Then the code can be run as such:

python src/TwitterParserStreaming.py \<name_of_file_with_tweets_as_jsons\> \<number_tweets_per_window\> \<number_tweets_per_shift\> \<desired_sparsity_of_pc\>

where \<name_of_file_with_tweets_as_jsons\> is the name of the file that contains the Tweets represented by a JSON on each line and the rest are self explanatory.

Once this is done, the code should be running and a pickle file will be created at the end (see https://docs.python.org/2/library/pickle.html) which can be used to see the results or use them in another program. The pickle file will have the name pCPickle_\<w\>_\<i\>_.pkl}, where \<w\> is the size of the window specified and \<i\> is the size of the increment. The array returned by deserialising the pickle file has tuples as elements, where each tuple is given as 
(pc_words, eigenvalue, start_date, end_date), where start_date and end_date is the date of the first Tweet of the particular window and the date of the last Tweet in the particular window respectively.
