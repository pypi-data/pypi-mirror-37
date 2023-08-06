# -*- coding: utf-8 -*-
"""
paff.data - manages the hash storage
"""

import shelve
import os
from xdg import XDG_DATA_HOME


# TODO: how to create a nice singleton object with python
class HashData(object):
    def __init__(self):
        paffConfigDir = os.path.join(XDG_DATA_HOME, "paff")
        if not os.path.exists(paffConfigDir):
            os.makedirs(paffConfigDir)
        self.data = shelve.open(os.path.join(paffConfigDir, ".paff"))
        # ToDo: Convert to Sqlite Database for increased performance

    def addHash(self, path, hash):
        self.data[path] = hash

    def getHash(self, path):
        return self.data[path]

    def removeHash(self, path):
        del self.data[path]

    def pathExists(self, path):
        return path in self.data

    def getPaths(self):
        return self.data.keys()

    def removePaths(self):
        pass


hashData = HashData()
