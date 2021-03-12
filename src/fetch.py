import feedparser
etag_prev = ""
def get_rss():
    NewsFeed = feedparser.parse("https://www.animenewsnetwork.com/all/rss.xml?ann-edition=in")
    entries = []
    summary = []
    for i in range(10):
        entry = NewsFeed.entries[i]
        print(entry.link)
        #entries.append(entry.title)
        #summary.append(entry.summary)
    #print(NewsFeed.etag)
    #etag_prev = NewsFeed.entries[0].id
    #return entries#,summary
    print(entries,summary)
def check_rss():
    NewsFeed = feedparser.parse("https://animeschedule.net/subrss.xml")
    print(NewsFeed)

check_rss()
