import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

api_key = 'AIzaSyDcRnH0wEv2zUWqrPkdOaHmMkNKLb6x0ic'

client = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
request = client.search().list(
    part='snippet',
    maxResults=10,
    q='covid',
    relevanceLanguage='en'
)

print(request.execute())










