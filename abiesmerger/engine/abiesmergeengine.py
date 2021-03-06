from abiesmerger.engine.abiesutils import sameValues, getMaxAttribute, getAbiesCode
import xml.etree.ElementTree as etree
import os, errno, re

class AbiesMergeEngine():

    PREFIX_SEPARATOR = "-"
    original = secondary = None

    def __init__(self, original):
        self.original = etree.fromstring(original)

    def setSecondaryFile(self, secondary, prefix=None):
        self.secondary = etree.fromstring(secondary)
        self.prefix = prefix

    def addPrefixToValue(self, sectionName, attrName):
        if (not self.prefix):
            return

        sectionSecondary = self.secondary.find(sectionName)

        for child in sectionSecondary.getchildren():
            attrValue =  self.prefix.upper() + self.PREFIX_SEPARATOR + child.get(attrName)
            child.set(attrName, attrValue)

    def getLastEjemplarCodeNumber(self):
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

        sectionOriginal = self.original.find(sectionName)
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
        sectionOriginal = self.original.find(sectionName)
        lastId = getMaxAttribute(idName, sectionOriginal.getchildren())

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
            if (editorialOld is not None):
                fondo.set('Editorial', self.editorialesIds[editorialOld])
            idAutorOld = fondo.get('IdAutor')
            if (idAutorOld is not None):
                fondo.set('IdAutor', self.autoresIds[idAutorOld])
            ejemplares = fondo.find('Ejemplares')
            for ejemplar in [] if (ejemplares is None) else ejemplares.getchildren():
                lastEjemplarCodeNumber += 1
                newAbiesCode = getAbiesCode(lastEjemplarCodeNumber)
                ejemplar.set('CodigoEjemplar', newAbiesCode)
                idTipoEjemplarOld = ejemplar.get('IdTiposEjemplar')
                if (idTipoEjemplarOld is not None):
                    ejemplar.set('IdTiposEjemplar', self.tiposEjemplarIds[idTipoEjemplarOld])
                idUbicacionOld = ejemplar.get('Ubicacion')
                if (idUbicacionOld is not None):
                    ejemplar.set('Ubicacion', self.ubicacionesIds[idUbicacionOld])
            funcionesAutor = fondo.find('FuncionesAutor')
            for funcionAutor in [] if (funcionesAutor is None) else funcionesAutor.getchildren():
                idFuncionAutorOld = funcionAutor.get('IdAutor')
                if (idFuncionAutorOld is not None):
                    funcionAutor.set('IdAutor', self.autoresIds[idFuncionAutorOld])
            fondoAplicaciones = fondo.find('FondoAplicaciones')
            for fondoAplicacion in [] if (fondoAplicaciones is None) else fondoAplicaciones.getchildren():
                idAplicacionOld = fondoAplicacion.get('IdAplicacion')
                if (idAplicacionOld is not None):
                    fondoAplicacion.set('IdAplicacion', self.aplicacionesIds[idAplicacionOld])
            descriptores = fondo.find('FondoDescriptores')
            for descriptor in [] if (descriptores is None) else descriptores.getchildren():
                idDescriptorOld = descriptor.get('IdDescriptor')
                if (idDescriptorOld is not None):
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
        self.addPrefixToValue('Ubicaciones', 'Ubicacion')
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
