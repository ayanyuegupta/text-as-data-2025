import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


def video_request(term, client, max_results=10, lang='en'):
    
    #### construct request to retrieve videos that a returned by our search term
    #### https://developers.google.com/youtube/v3/docs/videos/list
    request = client.search().list(
            part='snippet',
            maxResults=max_results,
            q=term,
            relevanceLanguage=lang
            )
    
    #### make request
    return request.execute()


def get_vid_comments(d, client, max_results=10):
    
    results = {}
    for vid in d['items']:
#        print('####')
#        print(vid['id'])
#        print('####')
#        print(vid['snippet'])
        
        #### filter out channels and get video id
        if vid['id']['kind'] == 'youtube#channel': continue
        vid_id = vid['id']['videoId']

        #### construct request to retrieve comments from a video
        #### https://developers.google.com/youtube/v3/docs/commentThreads/list
        request = client.commentThreads().list(
                part='id,snippet,replies',
                videoId=vid_id,
                maxResults=max_results
                )

        #### make request
        comments_d = request.execute()
        
        #### making sense of request results
#        print(comments_d.keys())
#        print('####')
        #### skip videos with no comments
        if len(comments_d['items']) == 0: continue

#        print(comments_d['items'][0])
#        print('####')
#        print(comments_d['items'][0]['id'])
#        print(comments_d['items'][0]['snippet'])
#        if 'replies' in comments_d['items'][0]:
#            print(comments_d['items'][0]['replies'])
        
        #### construct results dictionary
        for item in comments_d['items']:
            comment_info = item['snippet']['topLevelComment']['snippet']
            content = comment_info['textDisplay']
            user = comment_info['authorDisplayName']
            date = comment_info['publishedAt']
            results[item['id']] = {
                    'video_id': vid_id,
                    'content': content,
                    'user': user,
                    'date': date
                    }
#            print(results)
#            quit()
        
    return results


def main():

    #### specify/create directory for collected data
    data_dir = f'{os.getcwd()}/data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    #### create api client
    api_key = 'AIzaSyDcRnH0wEv2zUWqrPkdOaHmMkNKLb6x0ic'
    client = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    #### search for youtube videos
    d = video_request('covid', client)

    #### making sense of video_request() results
#    print(d.keys())
#    print(d['items'][0])
    
    #### get youtube comments
    results = get_vid_comments(d, client)
    
    #### save results
    with open(f'{data_dir}/youtube_data.json', 'w') as f:
        json.dump(results, f)

if __name__ == '__main__':
    main()
