# A very simple Flask Hello World app for you to get started with...
import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from test_db import User
from googleapiclient.discovery import build
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

app = Flask(__name__)

@app.route('/')

def GetVideosList():
    videos_pack = (getVideosDataFromYT(None))
    pack_items = videos_pack['items']

    dateUploaded = []
    titles = []
    view_count = []

    for i in pack_items:
        dateUploaded.append(i['snippet']['publishedAt'])
        titles.append(i['snippet']['title'])
        video_stats = getVideosStats(i['id']['videoId'])
        view_count.append(video_stats)

    key = 'nextPageToken'

    while(videos_pack.get(key) is not None):
        videos_pack = getVideosDataFromYT(videos_pack[key])
        pack_items = videos_pack['items']
        for i in pack_items:
            dateUploaded.append(i['snippet']['publishedAt'])
            titles.append(i['snippet']['title'])
            video_stats = getVideosStats(i['id']['videoId'])
            view_count.append(video_stats)

    return render_template('test.html', len = len(titles), publushTime = dateUploaded, vid_titles = titles, viewCount = view_count)

def getVideosDataFromYT(nextPageToken):
    #Setting YouTube API
    api_key = "AIzaSyAd8FR7xkoUK2UE0VsVK9TQCwakDBFFnhM"
    api_service_name = "youtube"
    api_version = "v3"

    client = build(api_service_name, api_version, developerKey=api_key)

    if(nextPageToken == None):
        request = client.search().list(
            part="snippet",
            channelId="UCppy4jafHu51iCMl-7qVbFA",
            type="video",
            maxResults=50,
            order ='date'
        )
    else:
        request = client.search().list(
            part="snippet",
            channelId="UCppy4jafHu51iCMl-7qVbFA",
            type="video",
            maxResults=50,
            order ='date',
            pageToken = nextPageToken
        )


    #Requesting data from YT
    json_data = request.execute()
    return json_data
    #user = User(datetime.today(), json_data)

    #Database stuff
    #Here we create engine
    #engine = create_engine('mysql://Taffer:189gk642@Taffer.mysql.pythonanywhere-services.com/Taffer$test_youtubue')

    #Now the session goes up!
    #Session = sessionmaker(bind = engine)

    #session = Session()
    #session.add(user)
    #session.commit()

def getVideosStats(video_id):
    #Setting YouTube API
    api_key = "AIzaSyAd8FR7xkoUK2UE0VsVK9TQCwakDBFFnhM"
    api_service_name = "youtube"
    api_version = "v3"

    client = build(api_service_name, api_version, developerKey=api_key)

    request = client.videos().list(
        part ='statistics',
        id = video_id
    )

    video_stats = request.execute()

    viewCount = []

    for i in video_stats["items"]:
        b = i["statistics"]
        viewCount.append(b["viewCount"])

    return viewCount

if __name__ == "__main__":
    app.run(debug=True)