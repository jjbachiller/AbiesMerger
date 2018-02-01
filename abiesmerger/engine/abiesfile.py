import zipfile
import os
import pathlib
import errno
from os.path import basename
from django.conf import settings

ABIES_DATA_FILE = "ExportAbies2-Catalogo.xml"
ABIES_LOG_FILE = "ExportAbies2-Catalogo.xml.log"
ABIES_CDU_FILE = "ExportAbies2-CDU.dat"

class AbiesFile():

    def __init__(self, uploadZipFile=None):
        if (uploadZipFile is not None):
            self.zip = zipfile.ZipFile(uploadZipFile, 'r')

    def __del__(self):
        self.zip.close()

    def createEmptyFile(self, path):
        self.path = path
        self.createPath()
        zipLocal = os.path.join(self.path, settings.ABIES_ZIP_FILE)
        self.zip = zipfile.ZipFile(zipLocal, 'w')

    def getAbiesData(self):
        # TODO: Verificar que existe el fichero
        return self.zip.read(ABIES_DATA_FILE)

    def getLogFile(self):
        return self.zip.read(ABIES_LOG_FILE)

    def getCduFile(self):
        return self.zip.read(ABIES_CDU_FILE)

    def createFileFromStream(self, filePath, stream):
        genericFile = open(filePath, "wb")
        genericFile.write(stream)
        genericFile.close()
        return genericFile

    def createDataFileFromStream(self, xmlString):
        dataFilePath = os.path.join(self.path, ABIES_DATA_FILE)
        self.createFileFromStream(dataFilePath, xmlString)
        self.zip.write(dataFilePath, basename(ABIES_DATA_FILE))
        os.remove(dataFilePath)

    def createLogFileFromStream(self, logContent):
        dataLogPath = os.path.join(self.path, ABIES_LOG_FILE)
        self.createFileFromStream(dataLogPath, logContent)
        self.zip.write(dataLogPath, basename(ABIES_LOG_FILE))
        os.remove(dataLogPath)

    def createCduFileFromStream(self, cduContent):
        dataCduPath = os.path.join(self.path, ABIES_CDU_FILE)
        self.createFileFromStream(dataCduPath, cduContent)
        self.zip.write(dataCduPath, basename(ABIES_CDU_FILE))
        os.remove(dataCduPath)

    def createPath(self):
        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
