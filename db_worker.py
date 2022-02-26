from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, MetaData, Table, and_
from sqlalchemy.orm import sessionmaker
from operator import itemgetter

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

    for i in last_videos:
        last_view_count.append(i.view_count)

    for i in prev_videos:
        prev_view_count.append(i.view_count)

    calculated_vc = [x - y for x, y in zip(last_view_count, prev_view_count)]
    for i in calculated_vc:
        calculated_vc_dict_list.append({"VPH":i})

    for i, j in zip (last_videos, calculated_vc_dict_list):
        j.update({'publishedAt':i['published_at']})
        j.update({'title':i['title']})

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

    results = session.execute(stmt).fetchall()
    return results

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

    results = session.execute(stmt).fetchall()
    return results

getSortedVideosListFromDB()