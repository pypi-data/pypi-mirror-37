import requests
from enum import Enum

from .patch import PatchManager

from .DataStore import Champion, Item

class ddragonFiles(Enum):
    champions="champion.json"
    championsFull="championFull.json"
    items="item.json"
    maps="map.json"

class ddragon():
    
    BASE_URL = "http://ddragon.leagueoflegends.com/cdn/"
    
    def __init__(self, load=True, language="en_US"):
        self.language = language
        
        self.version=None
        self.pm = None
        if load:
            self.setVersion()
            self.load(ddragonFiles.champions)
            self.load(ddragonFiles.items)
            
    def setVersion(self, season=None, patch=None, version=None):
        if season==None or patch==None or version==None:
            if self.pm == None:
                self.pm = PatchManager()
                
            self.version = self.pm.getVersion(season, patch, version)
        else:
            self.version = "{}.{}.{}".format(season,patch,version)
            
        
    def load(self, file):
        
        data = requests.get(self.BASE_URL + self.version + "/data/" + self.language +"/" + file.value).json()
        
        if file == ddragonFiles.champions:
            self.championById = {}
            self.championByName = {}
            
            for c in data["data"]:
                champion = Champion(data["data"][c])
                champion.setImageUrl(self.BASE_URL+ self.version + "/image/")
                
                self.championById[int(data["data"][c]["key"])] = champion
                self.championByName[data["data"][c]["name"]] = champion
                
        if file == ddragonFiles.items:
            self.itemById = {}
            self.itemByName = {}
            
            for i in data["data"]:
                item = Item(data["data"][i])
                item.setImageUrl(self.BASE_URL+ self.version + "/image/")
                
                self.itemById[int(i)] = item
                self.itemByName[data["data"][i]["name"]] = item
                
    def getChampion(self, champion):
        if isinstance(champion, int) or champion.isdigit():
            return self.championById[int(champion)]
        else:
            return self.championByName[champion]
        
    def getItem(self, item):
        if isinstance(item, int) or item.isdigit():
            return self.itemById[int(item)]
        else:
            return self.itemByName[item]