# from os import stat
import feedparser
#etag_prev = ""
def get_rss():
    NewsFeed = feedparser.parse("https://www.animenewsnetwork.com/all/rss.xml?ann-edition=in")
    entries = []
    summary = []
    links = []
    for i in range(6):
        entry = NewsFeed.entries[i]
        entries.append(entry.title)
        summary.append(entry.summary)
        links.append(entry.link)
    #print(NewsFeed.etag)
    #etag_prev = NewsFeed.entries[0].id
    return entries,summary,links
#def check_rss():
#    NewsFeed = feedparser.parse("https://www.livechart.me/feeds/episodes")
#    etag_new = NewsFeed.entries[0].id
#if etag_new == etag_prev:
#        return True
#    else:
#        return False


#get_rss()
#print(check_rss())

def get_rss_modified(last_modified):
    status = False
    try:
        NewsFeed = feedparser.parse("https://www.animenewsnetwork.com/all/rss.xml?ann-edition=in")
        updated = NewsFeed['updated']
        if last_modified != updated:
            status = True
            last_modified = updated
    except:
        status = False
    return status,last_modified
