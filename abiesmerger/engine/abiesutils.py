def getMaxAttribute(attribute, recordList):
    maxAttribute = 0
    for record in recordList:
        currentAttribute = int(record.get(attribute))
        if ( currentAttribute > maxAttribute):
            maxAttribute = currentAttribute
    return maxAttribute

def sameValues(value1, value2):
    return value1.lower().strip() == value2.lower().strip()

def getAbiesLetter(number):
    # Secuencia de letras asignadas por Abies, sin sentido alguno
    letterSequence = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']
    return letterSequence[number % len(letterSequence)]

def getAbiesCode(number):
    numberWithZeros = str(number).zfill(6)
    return numberWithZeros + getAbiesLetter(number)
