import feedparser
# import time
# import asyncio
# from datetime import datetime
# def get_rss_live_from_livechart():
    # print(datetime.now())
    # NewsFeed = feedparser.parse("https://www.livechart.me/feeds/episodes")
    # print(NewsFeed.entries[0].title)
    # print(NewsFeed['entries'])
# async def periodic():
    # while True:
        # get_rss_live_from_anischedule()()
        # await asyncio.sleep(10)

# def stop():
    # task.cancel()

# loop = asyncio.get_event_loop()
# loop.call_later(5, stop)
# task  = loop.create_task(periodic())
# try:
    # loop.run_forever()
# except asyncio.CancelledError:
    # pass

# def get_rss_live_from_livechart_modified():
    # # print(datetime.now())
    # #print("Hello")
    # NewsFeed = feedparser.parse("https://www.livechart.me/feeds/episodes")
    # print(NewsFeed['headers']['last-modified'])
    # return NewsFeed['headers']['last-modified']
# # anischedule

# if last_anime != NewsFeed['entries'][-1]['title']:
    # print(NewsFeed['entries'][-1]['title'])
    # status = True
    # entry_title = NewsFeed['entries'][-1]['title']
    # entry_link = NewsFeed['entries'][-1]['link']
async def get_rss_live_from_anischedule(last_anime):
    status = False
    # print(NewsFeed['updated'],"This is Anischedule")
    entry_link = ""
    entry_title = ""
    try:
        NewsFeed = feedparser.parse("https://animeschedule.net/subrss.xml")
        entry_title = NewsFeed['entries'][-1]['title']
        entry_link  = NewsFeed['entries'][-1]['link']
        print(entry_link)
        print(entry_title)
    except: #Exception as e:
        # print(e)
        entry_title = last_anime
    if last_anime != entry_title:
        status = True
    return entry_title,entry_link,status

async def get_rss_live_from_anischedule_modified():
    # print(datetime.now() , "This is modified")
    try:
        NewsFeed = feedparser.parse("https://animeschedule.net/subrss.xml")
        a = NewsFeed['updated']
    except:
        a = None
    return a
