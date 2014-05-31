'''
Created on 23 May 2014

@author: theopavlakou
'''

from TwitterStreamer import TwitterStreamer
from twython import Twython

if __name__ == '__main__':
#     while 1:
#         print ts.search(searchTerm="london",geocodeIn="51.50,-0.1,30mi")
    londonGeoCode = "51.5, -0.1, 10mi"
    APP_KEY = 'mY114DAnnXgjvZD2C58WOAfoA'
    APP_SECRET = 'NKawQSrLLzNsiP99gWrALlHnINfpRRn9ZMpXyikYG6k3oMcpsM'

#     stream = Twython(APP_KEY, APP_SECRET,
#                     OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    accessToken = twitter.obtain_access_token()
    twitter = Twython(APP_KEY, access_token=accessToken)
    while 1:
        print twitter.search(q="london")["statuses"]
