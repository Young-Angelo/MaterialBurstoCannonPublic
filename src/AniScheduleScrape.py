from bs4 import BeautifulSoup
import requests
async def GetAnimeSchedule():
    url='https://animeschedule.net'
    response = requests.get(url)
    # print(response.status_code)
    # html = response.text
    soup = BeautifulSoup(response.content, 'lxml')
    # print(soup)
    div = soup.find("div",{'id':'active-day'})
    eps = div.find_all("span",'show-episode')
    time = div.find_all("span","show-air-time")
    # print(time)
    # div = soup.find("div","Monday")
    # print(div)
    # name = div.text.strip()
    # print(time[0].text)
    name = div.find_all(['h2'])
    AnimeWithEp = []
    for i in range(len(name)):
        new_time = time[i].text.replace('\n',"")
        new_eps = eps[i].text.replace('\n',':')
        AnimeWithEp.append((name[i].text,new_eps[:-1],new_time))
    return AnimeWithEp
# print(name[0].text)
# print(type(name))
# name = name.split('\n')
# print(soup)
# print(name.split('\n'))
# print(name)
# print(set(name))
# content = str(name)
# print(content)

# res = []
# for i in name:
    # if i not in res:
        # res.append(i)
# printing list after removal  
# res.remove('')
# res.remove('N/A')
# print(res)
