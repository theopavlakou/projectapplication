'''
Created on 23 May 2014

@author: theopavlakou
'''
from twython import Twython
from twython import TwythonStreamer

# TODO: Not actually working. Should fix.
class TwitterStreamer(TwythonStreamer):
    '''
    classdocs
    '''
#     def __init__(self):
#         '''
#         Constructor
#         '''
#         self.appKey = 'mY114DAnnXgjvZD2C58WOAfoA'
#         self.appSecret = 'NKawQSrLLzNsiP99gWrALlHnINfpRRn9ZMpXyikYG6k3oMcpsM'
#         self.twitter = Twython(self.appKey, self.appSecret, oauth_version=2)
#         self.accessToken = self.twitter.obtain_access_token()
#         self.twitter = Twython(self.appKey, access_token=self.accessToken)

#     def search(self, searchTerm="", geocodeIn=""):
#         return self.twitter.search(q=searchTerm, geocode=geocodeIn)
#
#     def searchGen(self, searchTerm="", geocodeIn=""):
#         search = self.twitter.search_gen(searchTerm, geocode=geocodeIn)
#         for result in search:
#             print result

    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code