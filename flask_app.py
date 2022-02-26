# A very simple Flask Hello World app for you to get started with...
from datetime import datetime, timedelta

from flask import Flask, render_template
from sqlalchemy import create_engine, select, MetaData, Table, and_
from sqlalchemy.orm import sessionmaker
from db_worker import getSortedVideosListFromDB

# Database connection
engine = create_engine('mysql://Taffer:3kpSf42b@Taffer.mysql.pythonanywhere-services.com/Taffer$competitors')
metadata = MetaData(bind=None)

app = Flask(__name__)

@app.route('/')

def getVideoDataFromDB():
    results = getSortedVideosListFromDB()
    uploaded = []
    titles = []
    vph = []
    for i in results:
        uploaded.append(i['publishedAt'])
        titles.append(i['title'])
        vph.append(i['VPH'])

    return render_template('test.html', len=len(results), published_at=uploaded, vid_titles=titles, vph=vph)

if __name__ == "__main__":
    app.run(debug=True)