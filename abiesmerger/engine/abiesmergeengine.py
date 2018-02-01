from abiesmerger.engine.abiesutils import sameValues, getMaxAttribute, getAbiesCode
import xml.etree.ElementTree as etree
import os, errno, re

class AbiesMergeEngine():

    RESULT_XML_NAME = "ExportAbies2-Catalogo.xml"
    SUFIX_SEPARATOR = " "
    original = secondary = None

    def __init__(self, original):
        self.original = etree.fromstring(original)

    def setSecondaryFile(self, secondary, suffix=None):
        self.secondary = etree.fromstring(secondary)
        self.suffix = suffix

    def addSufixToValue(self, sectionName, attrName):
        if (not self.suffix):
            return

        # rootSecondary = self.secondary.getroot()
        # sectionSecondary = rootSecondary.find(sectionName)
        sectionSecondary = self.secondary.find(sectionName)

        for child in sectionSecondary.getchildren():
            attrValue = child.get(attrName) + self.SUFIX_SEPARATOR + self.suffix
            child.set(attrName, attrValue)

    def getLastEjemplarCodeNumber(self):
        # root = self.original.getroot()
        # fondos = root.find('Fondos')
        fondos = self.original.find('Fondos')
        lastCodeNumber = 0;
        for fondo in fondos.getchildren():
            ejemplares = fondo.find('Ejemplares')
            for ejemplar in ejemplares.getchildren():
                ejemplarCode = ejemplar.get('CodigoEjemplar')
                reEjemplarCode = re.compile(r'^(\d+)([A-Z])$')
                if not reEjemplarCode.match(ejemplarCode):
                    continue
                codeChunks = reEjemplarCode.search(ejemplarCode).groups()
                codeNumber = int(codeChunks[0])
                if (codeNumber > lastCodeNumber):
                    lastCodeNumber = codeNumber
        return lastCodeNumber


    def removeSameValues(self, sectionName, attrName, idName):
        repeatedIdDictionary = {}

        # rootOriginal = self.original.getroot()
        # sectionOriginal = rootOriginal.find(sectionName)
        sectionOriginal = self.original.find(sectionName)

        # rootSecondary = self.secondary.getroot()
        # sectionSecondary = rootSecondary.find(sectionName)
        sectionSecondary = self.secondary.find(sectionName)

        for secondaryChild in sectionSecondary.getchildren():
            secondaryName = secondaryChild.get(attrName)
            for originalChild in sectionOriginal.getchildren():
                originalName = originalChild.get(attrName)
                # If same names: Delete the row & save the ids to switch them in the 'fondos'
                if (sameValues(secondaryName, originalName)):
                    secondaryId = secondaryChild.get(idName)
                    originalId = originalChild.get(idName)
                    repeatedIdDictionary[secondaryId] = originalId
                    sectionSecondary.remove(secondaryChild)
                    break
        return repeatedIdDictionary

    """
    Copy the values of a section from the secondary file to the same section
    in the original file, changing the id to the correspondent id in the
    original file.

    Return: A dictionary with the correlation of the ids in the secondary file
    and the new id in the original file.
    """
    def copySectionValues(self, sectionName, idName):
        # oldIds --> newIds correlation dictionary
        newIdDictionary = {}

        # Get last Id in the original file
        # rootOriginal = self.original.getroot()
        # sectionOriginal = rootOriginal.find(sectionName)
        sectionOriginal = self.original.find(sectionName)
        lastId = getMaxAttribute(idName, sectionOriginal.getchildren())

        # rootSecondary = self.secondary.getroot()
        # sectionSecondary = rootSecondary.find(sectionName)
        sectionSecondary = self.secondary.find(sectionName)

        for child in sectionSecondary.getchildren():
            lastId += 1
            oldId = child.get(idName)
            # Save the new id correlation with the old id
            newIdDictionary[oldId] = str(lastId)
            child.set(idName, str(lastId))
            # Append the new child with the modifications
            sectionOriginal.append(child)
        return newIdDictionary.copy()

    """
    Merge the 'Fondos' section mantaining the correct id reference. It requires
    that the rest of the sections are filled in the object.

    Return:
    """
    def mergeAbiesFondos(self):
        lastEjemplarCodeNumber = self.getLastEjemplarCodeNumber()
        fondosOriginal = self.original.find('Fondos')
        fondosSecondary = self.secondary.find('Fondos')

        for fondo in fondosSecondary.getchildren():
            editorialOld = fondo.get('Editorial')
            fondo.set('Editorial', self.editorialesIds[editorialOld])
            idAutorOld = fondo.get('IdAutor')
            fondo.set('IdAutor', self.autoresIds[idAutorOld])
            ejemplares = fondo.find('Ejemplares')
            for ejemplar in [] if (ejemplares is None) else ejemplares.getchildren():
                lastEjemplarCodeNumber += 1
                newAbiesCode = getAbiesCode(lastEjemplarCodeNumber)
                ejemplar.set('CodigoEjemplar', newAbiesCode)
                idTipoEjemplarOld = ejemplar.get('IdTiposEjemplar')
                ejemplar.set('IdTiposEjemplar', self.tiposEjemplarIds[idTipoEjemplarOld])
            funcionesAutor = fondo.find('FuncionesAutor')
            for funcionAutor in [] if (funcionesAutor is None) else funcionesAutor.getchildren():
                idFuncionAutorOld = funcionAutor.get('IdAutor')
                funcionAutor.set('IdAutor', self.autoresIds[idFuncionAutorOld])
            fondoAplicaciones = fondo.find('FondoAplicaciones')
            for fondoAplicacion in [] if (fondoAplicaciones is None) else fondoAplicaciones.getchildren():
                idAplicacionOld = fondoAplicacion.get('IdAplicacion')
                fondoAplicacion.set('IdAplicacion', self.aplicacionesIds[idAplicacionOld])
            descriptores = fondo.find('FondoDescriptores')
            for descriptor in [] if (descriptores is None) else descriptores.getchildren():
                idDescriptorOld = descriptor.get('IdDescriptor')
                descriptor.set('IdDescriptor', self.descriptoresIds[idDescriptorOld])

            fondosOriginal.append(fondo)

    """
    Copy the values of all the sections from the secondary file to the same section
    in the original file.

    Return: the xml merge content as string
    """
    def mergeAbiesFiles(self):
        #Mezclando TipoEjemplar
        duplicatesTiposEjemplarIds = self.removeSameValues('TiposEjemplar', 'TipoEjemplar', 'IdTipoEjemplar')
        self.tiposEjemplarIds = self.copySectionValues('TiposEjemplar', 'IdTipoEjemplar')
        self.tiposEjemplarIds.update(duplicatesTiposEjemplarIds)
        #Mezclando ubicaciones
        self.addSufixToValue('Ubicaciones', 'Ubicacion')
        self.ubicacionesIds = self.copySectionValues('Ubicaciones', 'IdUbicacion')
        #Mezclando autores
        self.autoresIds = self.copySectionValues('Autores', 'IdAutor')
        #Mezclando Aplicaciones
        self.aplicacionesIds = self.copySectionValues('Aplicaciones', 'IdAplicacion')
        #Mezclando Descriptores
        self.descriptoresIds = self.copySectionValues('Descriptores', 'IdDescriptor')
        #Mezclando editoriales
        self.editorialesIds = self.copySectionValues('Editoriales', 'IdEditorial')
        #Mezclando fondos
        self.mergeAbiesFondos()

        return self.original

    def getXMLString(self):
        # return etree.tostring(self.original, encoding='unicode', method='xml')
        return etree.tostring(self.original)
