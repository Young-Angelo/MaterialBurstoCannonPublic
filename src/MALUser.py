from bs4 import BeautifulSoup
import requests

async def MalAuthUser(user_name):
    url = "https://myanimelist.net/profile/"
    # user_name = input()
    url+= user_name
    response = requests.get(url)

    # html = response.text
    soup = BeautifulSoup(response.content,'lxml')
    # print(soup)
    div = soup.find_all("span","user-status-data di-ib fl-r")
    # print(div.text)
    return_data = None
    results=[]
    try:
        for i in range(len(div)):
            results.append(div[i].text)
        return_data=results
    except:
        return_data=-1
    return return_data
# print(soup)

# span class="user-status-data di-ib fl-r">London</span
