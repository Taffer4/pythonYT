from test_db import VandN
from googleapiclient.discovery import build

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Google API Variables
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_key = "AIzaSyASLGLshTfMXlHoTKG9VpPg6esWJb-q15I"
api_service_name = "youtube"
api_version = "v3"

# Database connection
engine = create_engine('mysql://Taffer:3kpSf42b@Taffer.mysql.pythonanywhere-services.com/Taffer$competitors')

def GetVideosList():
    videos_pack = (getVideosDataFromYT(None))
    pack_items = videos_pack['items']

    dateUploaded = []
    titles = []
    view_count = []

    #Now the session goes up!
    Session = sessionmaker(bind = engine)
    session = Session()

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

    for i in range(len(titles)):
        v_and_n = VandN(datetime.today(), dateUploaded[i], titles[i], view_count[i])
        session.add(v_and_n)
        session.commit()

def getVideosDataFromYT(nextPageToken):
    #Setting YouTube API

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

def getVideosStats(video_id):
    #Setting YouTube API

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

GetVideosList()