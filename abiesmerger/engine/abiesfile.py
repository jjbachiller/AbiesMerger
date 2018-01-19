import zipfile
import os
import pathlib

class AbiesFile():

    def __init__(self, zipSource, parentFolder=''):
        self.zip = zipfile.ZipFile(zipSource, 'r')
        self.parentFolder = parentFolder

    def __del__(self):
        self.zip.close()

    def getAbiesData(self, libraryFileName):
        return self.zip.open(libraryFileName)
        # zipTarget = os.path.join(workingDirectory, self.parentFolder)
        #pathlib.Path(zipTarget).mkdir(parents=True, exist_ok=True)
        # self.zip.extractall(zipTarget)
        # self.zip.close()
