# finding all Songs in a directory
import os
import re

class Songs():
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path
    
class SongList(list):
    def __init__(self, directory):
        super().__init__()

        for folders , subFolders , files in os.walk(directory):
            for file in files:
                if re.findall('.mp3$' , file.lower()):
                    self.append(Songs(file, os.path.join(folders , file)))