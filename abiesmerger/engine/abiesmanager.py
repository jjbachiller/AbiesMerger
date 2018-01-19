from abiesmerger.engine.abiesfile import AbiesFile
from abiesmerger.engine.abiesmergeengine import AbiesMergeEngine


class AbiesManager():

    def __init__(self, baseZip, secondariesZip, suffixes):
        self.base = AbiesFile(baseZip)
        self.secondaries = self.suffixes = []
        for secondaryZip, suffix in zip(secondariesZip, suffixes):
            self.secondaries.append(AbiesFile(secondaryZip))
            self.suffixes.append(suffix)

    def merge(self):
        abiesMerger = AbiesMergeEngine(self.base.getAbiesData)
        for secondary, suffix in zip(self.secondaries, self.suffixes):
            abiesMerger.setSecondaryFile(secondary, suffix)
            abiesMerger.mergeAbiesBackup()
        #Saving changes
        abiesMerger.saveMerge('/tmp')
