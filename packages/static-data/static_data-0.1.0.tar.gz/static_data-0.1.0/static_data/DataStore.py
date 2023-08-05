class Champion():
    
    def __init__(self, data):
        self.data = data
        
    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl
        
    @property
    def image(self):
        return self.imageUrl + "champion/" + self.data["image"]["full"]
    
    @property
    def sprite(self):
        return (self.imageUrl + "sprite/" + self.data["image"]["sprite"],self.data["image"]["x"],self.data["image"]["y"])
    
    @property
    def name(self):
        return self.data["name"]
        
        

class Item():
    
    def __init__(self, data):
        self.data = data
        
        
    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl
        
    @property
    def image(self):
        return self.imageUrl + "item/" + self.data["image"]["full"]
    
    @property
    def sprite(self):
        return (self.imageUrl + "sprite/" + self.data["image"]["sprite"],self.data["image"]["x"],self.data["image"]["y"])
    
    @property
    def name(self):
        return self.data["name"]