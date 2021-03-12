import pyrebase
from MALUser import *
config = {
  "apiKey": "APIKEY",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "DB_URL",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "serviceAccount.json"
}

firebase = pyrebase.initialize_app(config)
### USER DATABASE ###
returning_list=[]
class UserDatabase():
    def __init__(self):
        # self.firebase = pyrebase.initialize_app(config)
        self.database = firebase.database().child('users')
# users = db.child('users').get()
# print(users.val())
    async def Update(self):
        self.database = firebase.database().child('users')
        # self.returning_list=[]
    async def GetData(self,user_id):
        await self.Update()
        returning_list = []
        try:
            anime_list = self.database.child(user_id).get()
            # print(anime_list)
            for user in anime_list.each():
                returning_list.append(user.val()) # {name": "Mortimer 'Morty' Smith"}
        # to_add_list.append(to_add)
            self.returning_list = returning_list
        except: #Exception as e:
            # print(e)
            returning_list = None
        return returning_list
    async def UpdateData(self,user_id,data):
        # self.update()
        # print(self.get_data_from_user(user_id))
        existing_data = await self.GetData(user_id)
        #existing_data.append(data)
        if existing_data != None:
            if len(existing_data) == 10:
                return -1
            elif data in existing_data:
                return -2
            existing_data.append(data)
            print(existing_data)
            print(data)
            # to_update = [x.lower() for x in to_update]
            # to_update = set(to_update)
            # to_update = [x.title() for x in to_update]
            self.database.child('users').update({user_id:existing_data})
            return 1
        else:
            existing_data = []
            existing_data.append(data)
            self.database.child('users').child(user_id).set(existing_data)
            return 1
        # self.database.update({user_id:existing_data})
    async def RemoveData(self,user_id,data):
        existing_data = await self.GetData(user_id)
        if existing_data == -1:
            return -1
        try:
            existing_data.pop(data)
        except:
            return -2
        self.database.child('users').update({user_id:existing_data})
        return 1

### SERVER DATABASE ### 

class ServerDatabase():
    def __init__(self):
        self.nice = "nice"
        pass

class UserRecDatabase():
    def __init__(self):
        self.database = firebase.database().child('users_rec')
    async def Update(self):
        self.database = firebase.database().child('users_rec')
    async def GetData(self,user_id):
        await self.Update()
        returning_list = []
        try:
            anime_list = self.database.child(user_id).get()
            # print(anime_list)
            for user in anime_list.each():
                returning_list.append(user.val()) # {name": "Mortimer 'Morty' Smith"}
        # to_add_list.append(to_add)
            # self.returning_list = returning_list
        except: #Exception as e:
            # print(e)
            returning_list = None
        return returning_list

    async def UpdateData(self,user_id,data):
        # self.update()
        # print(self.get_data_from_user(user_id))
        existing_data = await self.GetData(user_id)
        #existing_data.append(data)
        if existing_data != None:
            if len(existing_data) == 10:
                return -1
            elif data in existing_data:
                return -2
            existing_data.append(data)
            # print(existing_data)
            # to_update = [x.lower() for x in to_update]
            # to_update = set(to_update)
            # to_update = [x.title() for x in to_update]
            self.database.child('users_rec').update({user_id:existing_data})
            return 1
        else:
            existing_data = []
            existing_data.append(data)
            self.database.child('users_rec').child(user_id).set(existing_data)
            return 1
        # self.database.update({user_id:existing_data})
    async def RemoveData(self,user_id,data):
        existing_data = await self.GetData(user_id)
        if existing_data == -1:
            return -1
        try:
            existing_data.pop(data)
        except:
            return -2
        self.database.child('users_rec').update({user_id:existing_data})
        return 1

class AnimeStoreRss():
    def __init__(self):
        self.database = firebase.database().child('last_anime')
    async def Update(self):
        self.database = firebase.database().child('last_anime')
    async def updateAnime(self,arg1):
        new_list = await self.lastAnime()
        new_list.append(arg1)
        # new_list = set(new_list)
        print(new_list)
        # self.database.child('last_anime').set(new_list)
        self.database.child('last_anime').set(new_list)
        new_list=[]
    async def lastAnime(self):
        # last_anime = self.database.get()
        await self.Update()
        returning_list=[]
        anime_list = self.database.get()
        # print(anime_list.val())
            # print(anime_list)
        try:
            for user in anime_list.each():
                returning_list.append(user.val()) # {name": "Mortimer 'Morty' Smith"}
        except:
            returning_list=[]
        return returning_list

class UserMAL():
    def __init__(self):
        self.database = firebase.database().child('users_mal')
    async def Update(self):
        self.database = firebase.database().child('users_mal')
    async def GetData(self,user_id):
        await self.Update()
        return self.database.child(user_id).get().val()
    async def SetProfile(self,user_id,user_name):
        await self.Update()
        self.database.child(user_id).set(user_name)
    async def CheckUser(self,user_id):
        await self.Update()
        returning_data = self.database.get()
        # print(returning_data.val())
        if user_id in returning_data.val():
            return -1
        else:
            return 1
