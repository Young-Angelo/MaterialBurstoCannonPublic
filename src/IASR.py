class IASR():
    def __init__(self):
        self.status = False
    async def Start(self,event_title):
        self.title = event_title
        self.status = True
    async def AddData(self,data):
        pass
