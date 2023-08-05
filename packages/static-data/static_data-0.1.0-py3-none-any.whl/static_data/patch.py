import requests

class Version():
    
    def __init__(self, patch, versionNumber):
        self.patch = patch
        self.versionNumber = int(versionNumber)
        
    def getString(self):
        return "{}.{}".format(self.patch.getString(), self.versionNumber)
        
    def __eq__(self, other):
        if self is other:
            return True

        elif type(self) != type(other):
            return False

        else:
            return self.patch == other.patch and self.versionNumber == other.versionNumber
        
    def __lt__(self, other):
        if self.patch == other.patch:
            return self.versionNumber < other.versionNumber
        else:
            return self.patch < other.patch
        
class Patch():
    
    def __init__(self, season, patchNumber):
        self.season = season
        self.patchNumber = int(patchNumber)
        
        self.versions = {}
        self.lastVersion = None
        
    def addVersion(self, versionNumber):
        versionNumber = int(versionNumber)
        
        if versionNumber in self.versions:
            return self.getVersion(versionNumber)
        
        version = Version(self, versionNumber)
        
        if self.lastVersion == None or version > self.lastVersion:
            self.lastVersion = version
        
        self.versions[versionNumber] = version
        
        return version
        
    def getLastVersion(self):
        return self.lastVersion
        
    def getVersion(self, versionNumber):
        return self.versions[versionNumber]
    
    def getString(self):
        return "{}.{}".format(self.season.getString(), self.patchNumber)
    
        
    def __eq__(self, other):
        if self is other:
            return True

        elif type(self) != type(other):
            return False

        else:
            return self.season == other.season and self.patchNumber == other.patchNumber
        
    def __lt__(self, other):
        if self.season == other.season:
            return self.patchNumber < other.patchNumber
        else:
            return self.season < other.season
    
class Season():
    
    def __init__(self, seasonNumber):
        self.seasonNumber = int(seasonNumber)
        
        self.patches = {}
        self.lastPatch = None
        
    def addPatch(self, patchNumber):
        patchNumber = int(patchNumber)
        
        if patchNumber in self.patches:
            return self.getPatch(patchNumber)
        
        patch = Patch(self, patchNumber)
        
        if self.lastPatch == None or patch > self.lastPatch:
            self.lastPatch = patch
        
        self.patches[patchNumber] = patch
        
        return patch
        
    def getLastPatch(self):
        return self.lastPatch
    
    def getPatch(self, patchNumber):
        return self.patches[patchNumber]
    
    def getLastVersion(self):
        return self.lastPatch.getLastVersion()
        
    def getString(self):
        return "{}".format(self.seasonNumber)
        
        
    def __eq__(self, other):
        if self is other:
            return True

        elif type(self) != type(other):
            return False

        else:
            return self.seasonNumber == other.seasonNumber
        
    def __lt__(self, other):
        return self.seasonNumber < other.seasonNumber
    
    
class PatchManager():
    
    def __init__(self):
        self.seasons = {}
        self.lastSeason = None
        
        self.getVersions()
        
        
    def getVersions(self):
        r = requests.get("http://ddragon.leagueoflegends.com/api/versions.json").json()
        
        for v in r:
            if not v.split(".")[0].isdigit():
                break
            season, patch, version = v.split(".")
            
            self.addSeason(season).addPatch(patch).addVersion(version)
        
    #The only function you need here
    def getLatestVersion(self):
        return self.getLastSeason().getLastVersion().getString()
    
    def getVersionFromGameVersion(self, gameVersion):
        return self.getSeason(int(gameVersion.split(".")[0])).getPatch(int(gameVersion.split(".")[1])).getLastVersion().getString()
    
    def getVersion(self, season=None, patch=None, version=None):
        if season == None:
            s = self.getLastSeason()
        else:
            s = self.getSeason(season)
            
        if patch == None:
            p = s.getLastPatch()
        else:
            p = s.getPatch(patch)
            
        if version == None:
            return p.getLastVersion().getString()
        else:
            return p.getVersion(version).getString()
        
    def addSeason(self, seasonNumber):
        seasonNumber = int(seasonNumber)
        
        if seasonNumber in self.seasons:
            return self.getSeason(seasonNumber)
        
        season = Season(seasonNumber)
        
        if self.lastSeason == None or season > self.lastSeason:
            self.lastSeason = season
        
        self.seasons[seasonNumber] = season
        
        return season
    
    def getLastSeason(self):
        return self.lastSeason
            
    def getSeason(self, seasonNumber):
        return self.seasons[seasonNumber]
                
            
            
            