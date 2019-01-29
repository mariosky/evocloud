from requests_oauthlib import OAuth2Session
import os
import urllib

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

EXPERIMENT_ID = '1548775365'
START='2019-01-29T15:21:51.958131694Z'
END=  '2019-01-29T15:25:36.748962385Z'
METRIC='execution_count'
# 'execution_times', 'execution_count','user_memory_bytes',


redirect_uri = "https://localhost"
scope = 'https://www.googleapis.com/auth/monitoring'
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scope)
from requests.utils import requote_uri


def get_token():
    authorization_url, state = oauth.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        # access_type and prompt are Google specific extra
        # parameters.
        access_type="offline", prompt="select_account")

    print ('Please go to %s and authorize access.' % authorization_url)
    authorization_response = input('Enter the full callback URL')
    token = oauth.fetch_token(
        'https://accounts.google.com/o/oauth2/token',
        authorization_response=authorization_response,
        # Google specific extra parameter used for client
        # authentication
        client_secret=client_secret)
    return token

token = get_token()

#url_string = 'https://monitoring.googleapis.com/v3/projects/evocloud/timeSeries?filter=metric.type%3D%22cloudfunctions.googleapis.com%2Ffunction%2Fexecution_count%22&interval.endTime=2019-01-22T22%3A28%3A50.996508940Z&interval.startTime=2019-01-12T22%3A28%3A47.364942912Z'
url_string = 'https://monitoring.googleapis.com/v3/projects/evocloud/timeSeries?filter=metric.type%3D%22cloudfunctions.googleapis.com%2Ffunction%2F{}%22&interval.endTime={}&interval.startTime={}'.format( METRIC, urllib.parse.quote(END),urllib.parse.quote(START))

r = oauth.get(url_string)



with open('../experiment_data/{}-{}.json'.format(METRIC,EXPERIMENT_ID), 'w') as outfile:
    outfile.write(r.text)