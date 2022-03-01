from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, MetaData, Table, and_
from sqlalchemy.orm import sessionmaker
from operator import itemgetter
import pandas as pd

engine = create_engine('mysql://Taffer:3kpSf42b@Taffer.mysql.pythonanywhere-services.com/Taffer$competitors')
metadata = MetaData(bind=None)

def getSortedVideosListFromDB():
    last_videos = getLastVideoDataFromDB()
    prev_videos = getPrevVideoDataFromDB()
    result_list = computeViewCount(last_videos, prev_videos)

    return result_list

def computeViewCount(last_videos, prev_videos):
    last_view_count = []
    prev_view_count = []
    calculated_vc = []
    calculated_vc_dict_list = []

    for r in last_videos.index:
        print(last_videos.at[r])

    for r in last_videos.index:
        if last_videos.at[r, 'title'] == prev_videos.at[r, 'title']:
            last_view_count.append(last_videos.at[r, 'view_count'])
            prev_view_count.append(prev_videos.at[r, 'view_count'])

    calculated_vc = [x - y for x, y in zip(last_view_count, prev_view_count)]

    for i in calculated_vc:
        calculated_vc_dict_list.append({"VPH": i})

    for index_lv, row_lv in last_videos.iterrows():
        calculated_vc_dict_list[index_lv].update({'publishedAt': row_lv['published_at']})
        calculated_vc_dict_list[index_lv].update({'title': row_lv['title']})

    finished_list = sorted(calculated_vc_dict_list, key=itemgetter('VPH'), reverse=True)

    return finished_list

def getLastVideoDataFromDB():
    select_time = datetime.now() - timedelta(hours=1)

    table = Table(
        'vandn',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    stmt = select([
        table.columns.id,
        table.columns.date_time,
        table.columns.published_at,
        table.columns.title,
        table.columns.view_count
    ]).where(
        and_(table.columns.date_time > select_time, table.columns.date_time < datetime.now())
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.DataFrame(session.execute(stmt).fetchall())
    return df

def getPrevVideoDataFromDB():
    select_time_top = datetime.now() - timedelta(hours=1)
    select_time_bottom = datetime.now() - timedelta(hours=2)

    table = Table(
        'vandn',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    stmt = select([
        table.columns.id,
        table.columns.date_time,
        table.columns.published_at,
        table.columns.title,
        table.columns.view_count
    ]).where(
        and_(table.columns.date_time > select_time_bottom, table.columns.date_time < select_time_top)
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.DataFrame(session.execute(stmt).fetchall())
    return df

getSortedVideosListFromDB()