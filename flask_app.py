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

def getVideosDataFromYT(nextPageToken):
    #Setting YouTube API
    api_key = "AIzaSyDReRsRej0OfdaOUOfq5z_PHvqqKepIDLU"
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
    #dumped_json = json.dumps(json_data)
    #user = User(datetime.today(), json_data)

    #Database stuff
    #Here we create engine
    #engine = create_engine('mysql://Taffer:189gk642@Taffer.mysql.pythonanywhere-services.com/Taffer$test_youtubue')

    #Now the session goes up!
    #Session = sessionmaker(bind = engine)

    #session = Session()
    #session.add(user)
    #session.commit()

    videos_list = json_data['items']
    return json_data

def printVideosList(videos_list):
    ids = []
    titles = []

    for i in videos_list:
        ids.append(i['id']['videoId'])
        titles.append(i['snippet']['title'])
        return render_template('test.html', len = len(ids), video_ids = ids, vid_titles = titles)

def GetVideosList():
    videos = getVideosDataFromYT(None)
    key = 'nextPageToken'

    while(videos.get(key) is not None):
        videos.update(getVideosDataFromYT(videos['nextPageToken']))
        printVideosList(videos)

GetVideosList()