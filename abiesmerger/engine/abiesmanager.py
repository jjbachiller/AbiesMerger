import random
import string
import os
from shutil import rmtree
from abiesmerger.engine.abiesfile import AbiesFile
from abiesmerger.engine.abiesmergeengine import AbiesMergeEngine
from django.conf import settings

RANDOM_FOLDER_LENGTH = 9

class AbiesManager():

    def __init__(self, baseZip, secondariesZip, suffixes):
        # randomFolder = self.getRandomFolderName()
        # workingFolder = os.path.join(WORKING_FOLDER, randomFolder)
        self.base = AbiesFile(baseZip)
        self.secondaries = []
        self.suffixes = suffixes
        for i, secondaryZip in enumerate(secondariesZip):
            abiesType = 'secondary' + str(i)
            self.secondaries.append(AbiesFile(secondaryZip))

    def merge(self):
        # Borramos los restos de otros mergeos que pudieran quedar
        rmtree(settings.DOWNLOAD_FOLDER, ignore_errors=True)
        # Creamos un MergeEngine con la biblioteca base
        abiesMerger = AbiesMergeEngine(self.base.getAbiesData())
        # Y le anexamos a esta cada biblioteca secundaria con su sufijo
        for secondary, suffix in zip(self.secondaries, self.suffixes):
            abiesMerger.setSecondaryFile(secondary.getAbiesData(), suffix)
            abiesMerger.mergeAbiesFiles()
        # Crear archivo para descarga
        randomFolderName = self.getRandomFolderName()
        downloadFolder = os.path.join(settings.DOWNLOAD_FOLDER, randomFolderName)
        self.downloadableFile = AbiesFile()
        self.downloadableFile.createEmptyFile(downloadFolder)
        # Le añadimos el contenido mergeado
        abiesMergeString = abiesMerger.getXMLString()
        self.downloadableFile.createDataFileFromStream(abiesMergeString)
        # Y el archivo de CDU y Log del archivo base.
        baseLogFile = self.base.getLogFile()
        self.downloadableFile.createLogFileFromStream(baseLogFile)
        baseCduFile = self.base.getCduFile()
        self.downloadableFile.createCduFileFromStream(baseCduFile)
        # Devolvemos el nombre de la carpeta que contiene el archivo zip
        return randomFolderName

    def getRandomFolderName(self):
        randomFolder = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(RANDOM_FOLDER_LENGTH)])
        return randomFolder
