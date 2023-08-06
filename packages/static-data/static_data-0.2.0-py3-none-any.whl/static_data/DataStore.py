class DataStore():
    
    def __init__(self, data):
        self.data = data
        
    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl
        
    @property
    def image(self):
        return self.imageUrl +self.data["image"]["group"] + "/" + self.data["image"]["full"]
    
    @property
    def sprite(self):
        return (self.imageUrl + "sprite/" + self.data["image"]["sprite"],self.data["image"]["x"],self.data["image"]["y"])
    
    @property
    def name(self):
        return self.data["name"]
    



class Champion(DataStore):
    pass

class Item(DataStore):
    pass

class Map(DataStore):
    
    @property
    def name(self):
        return self.data["MapName"]

class Summoner(DataStore):
    pass