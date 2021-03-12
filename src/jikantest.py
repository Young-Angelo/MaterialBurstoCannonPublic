from jikanpy import Jikan
from jikanpy import AioJikan
jikan = Jikan()

def profile(user_name):
    try:
        user = jikan.user(
                username=user_name,
                request='animelist' ,
                argument='completed'
                )
        for i in user['anime']:
            print(i['title'])
    except:
        return -1

async def searchAnime(anime):
    async with AioJikan() as aio_jikan:
        result = await aio_jikan.search(
             'anime',
              anime
         )
    results = [[result['results'][i]['title'],result['results'][i]['url'],result['results'][i]['rated'],result['results'][i]['mal_id']] for i in range(5)]
    return results

# def searchAnime(anime):
    # result = jikan.search('anime',anime)
    # results = [(result['results'][i]['title'],result['results'][i]['url']) for i in range(5)]
    # links = [result['results'][i]['url'] for i in range(5)]
    # return results
#print(search_result['results'][0]['type']) 
        #print(search_result['results'][1].keys())
#   for i in user['anime']:
#        print(i['title'])

async def currently(user_name):
    async with AioJikan() as aio_jikan:
        user = await aio_jikan.user(
                username=user_name,
                request='animelist',
                argument='watching'
                )
        result = []
        result1 = []
    for i in range(0,len(user['anime'])):
        result.append(user['anime'][i]['title'])
        result1.append(user['anime'][i]['watched_episodes'])
    return result,result1


async def completed_anime(user_name):
    async with AioJikan() as aio_jikan:
        user = await  aio_jikan.user(
                username=user_name,
                request='animelist',
                argument='completed'
                )
    result = []
    for i in range(0,len(user['anime'])):
        result.append(user['anime'][i]['title'])
    return result

async def plantowatch(user_name):
    async with AioJikan() as aio_jikan:
        user = await aio_jikan.user(
                username=user_name,
                request='animelist',
                argument='ptw'
                )
    result = []
    for i in range(0,len(user['anime'])):
        result.append(user['anime'][i]['title'])
    return result
