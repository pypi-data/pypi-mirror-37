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
    


spellToKeyHelper = {
    0:"Q",
    1:"W",
    2:"E",
    3:"R"
}

class Champion(DataStore):
    BASE_URL = "http://ddragon.leagueoflegends.com/cdn/"
    
    def __init__(self, data):
        self.data = data
        if "spells" in self.data:
            self.loadSpells()
            
    def loadSpells(self):
        self.spellById = {}
        self.spellByName = {}
        self.spellByKey = {}
        self.spellBySlot = {}
        for k,s in enumerate(self.data["spells"]):
            spell = Spell(s)
            
            self.spellById[s["id"]] = spell
            self.spellByName[s["name"]] = spell
            self.spellByKey[spellToKeyHelper[k]] = spell
            self.spellBySlot[k + 1] = spell
            
    def spell(self, sp):
        if isinstance(sp, int) or sp.isdigit():
            return self.spellBySlot[int(sp)]
        elif len(sp)==1:
            return self.spellByKey[sp]
        elif sp in self.spellByName:
            return self.spellByName[sp]
        elif sp in self.spellById:
            return self.spellById[sp]
            
    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl
        for s in self.spellById:
            self.spellById[s].setImageUrl(imageUrl)
            

class Item(DataStore):
    pass

class Map(DataStore):
    @property
    def name(self):
        return self.data["MapName"]

class Summoner(DataStore):
    pass

class Icon(DataStore):
    @property
    def name(self):
        return None
    
class Spell(DataStore):
    pass

class Rune():
    
    def __init__(self, data):
        self.data = data
        
    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl
        
    @property
    def image(self):
        return self.imageUrl +self.data["icon"]
    
    @property
    def name(self):
        return self.data["name"]