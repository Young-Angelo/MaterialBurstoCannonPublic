import feedparser

def get_rss_live():
    NewsFeed = feedparser.parse("https://www.livechart.me/feeds/episodes")
    entry = []
    for i in range(10):
        entry.append(NewsFeed.entries[i].title)

    #print(entry.keys())
    #print(NewsFeed.keys())
    #print(entry.title)
    #print(NewsFeed.headers)
    #print(NewsFeed.headers['If-Modified-Since'])

    return entry
#get_rss_live()
