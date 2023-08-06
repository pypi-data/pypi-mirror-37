import requests
from enum import Enum

from .patch import PatchManager

from .DataStore import Champion, Item, Map, Summoner, Icon, Rune

class ddragonFiles(Enum):
    champions="champion.json"
    championsFull="championFull.json"
    items="item.json"
    maps="map.json"
    summoners="summoner.json"
    icons="profileicon.json"
    runes="runesReforged.json"

class ddragon():
    
    BASE_URL = "http://ddragon.leagueoflegends.com/cdn/"
    
    def __init__(self, load=True, language="en_US", championFull=True):
        self.language = language
        self.championFull = championFull
        
        self.version=None
        self.pm = None
        if load:
            self.setVersion()
            
    def setVersion(self, season=None, patch=None, version=None):
        if season==None or patch==None or version==None:
            if self.pm == None:
                self.pm = PatchManager()
                
            self.version = self.pm.getVersion(season, patch, version)
        else:
            self.version = "{}.{}.{}".format(season,patch,version)
        self.loadAll()
            
    def loadAll(self):
        if self.championFull:
            self.load(ddragonFiles.championsFull)
        else:
            self.load(ddragonFiles.champions)
            
        
        self.load(ddragonFiles.items)
        self.load(ddragonFiles.maps)
        self.load(ddragonFiles.summoners)
        self.load(ddragonFiles.icons)
        self.load(ddragonFiles.runes)
    
    
    def load(self, file):
        
        data = requests.get(self.BASE_URL + self.version + "/data/" + self.language +"/" + file.value).json()
        
        if file == ddragonFiles.champions or file == ddragonFiles.championsFull:
            self.championById = {}
            self.championByName = {}
            
            for c in data["data"]:
                champion = Champion(data["data"][c])
                champion.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.championById[int(data["data"][c]["key"])] = champion
                self.championByName[data["data"][c]["name"]] = champion
                
        if file == ddragonFiles.items:
            self.itemById = {}
            self.itemByName = {}
            
            for i in data["data"]:
                item = Item(data["data"][i])
                item.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.itemById[int(i)] = item
                self.itemByName[data["data"][i]["name"]] = item
                
        if file == ddragonFiles.maps:
            self.mapById = {}
            self.mapByName = {}
            
            for i in data["data"]:
                m = Map(data["data"][i])
                m.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.mapById[int(i)] = m
                self.mapByName[data["data"][i]["MapName"]] = m
                
        if file == ddragonFiles.summoners:
            self.summonersById = {}
            self.summonersByName = {}
            
            for s in data["data"]:
                summ = Summoner(data["data"][s])
                summ.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.summonersById[int(data["data"][s]["key"])] = summ
                self.summonersByName[data["data"][s]["name"]] = summ
                
        if file == ddragonFiles.icons:
            self.iconsById = {}
            
            for i in data["data"]:
                icon = Icon(data["data"][i])
                icon.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.iconsById[int(i)] = icon
        
        if file == ddragonFiles.runes:
            self.runesById = {}
            self.runesByName = {}
            
            for tree in data:
                for slot in tree["slots"]:
                    for r in slot["runes"]:
                        rune = Rune(r)
                        rune.setImageUrl(self.BASE_URL+ "img/")

                        self.runesById[int(r["id"])] = rune
                        self.runesByName[r["name"]] = rune
                
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
        
    def getMap(self, m):
        if isinstance(m, int) or m.isdigit():
            return self.mapById[int(m)]
        else:
            return self.mapByName[m]
        
    def getSummoner(self, s):
        if isinstance(s, int) or s.isdigit():
            return self.summonersById[int(s)]
        else:
            return self.summonersByName[s]
        
    def getIcon(self, icon):
        return self.iconsById[int(icon)]
    
    def getRune(self, r):
        if isinstance(r, int) or r.isdigit():
            return self.runesById[int(r)]
        else:
            return self.runesByName[r]