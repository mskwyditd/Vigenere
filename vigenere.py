from statistics import mean


twoletters = [ 'cz', 'ch', 'dz', 'rz', 'sz', 'ci', 'ni', 'zi', 'si' ]

threeletters = ['dzi']


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

# dodane prawdopodobieństwa z polskich znaków
# polishLetterPossibilities = { 'A':9.9, 'B':1.47, 'C':3.96, 'D':3.25, 'E':8.77, 'F':0.3, 'G':1.42,
# 'H':1.08, 'I':8.21, 'J':2.28, 'K':3.51, 'L':3.92, 'M':2.8, 'N':5.72, 'O':8.6, 'P':3.13, 'Q':0.14,
# 'R':4.69, 'S':4.98, 'T':3.98, 'U':2.5, 'V':0.04, 'W':4.65, 'X':0.02, 'Y':3.76, 'Z':6.53,  ' ':5. }

polishLetterPossibilities = { 'A':8.91, 'B':1.47, 'C':3.96, 'D':3.25, 'E':7.66, 'F':0.3, 'G':1.42,
'H':1.08, 'I':8.21, 'J':2.28, 'K':3.51, 'L':2.1, 'M':2.8, 'N':5.52, 'O':7.75, 'P':3.13, 'Q':0.14,
'R':4.69, 'S':4.32, 'T':3.98, 'U':2.5, 'V':0.04, 'W':4.65, 'X':0.02, 'Y':3.76, 'Z':5.64,  ' ':4.0 }

letter_to_nr = dict(zip(ALPHABET, range(len(ALPHABET))))
nr_to_letter = dict(zip(range(len(ALPHABET)), ALPHABET))


def encrypt(key, message):
    ciphertext = ''
    for i in range(len(message)):
        try:
            ciphertext += nr_to_letter[( letter_to_nr[message[i]] + letter_to_nr[key[i % len(key)]] ) % len(ALPHABET)]
        except KeyError:
            print('Letter not int dictionary!')
    return ciphertext

def decrypt(key, ciphertext):
    message = ''
    for i in range(len(ciphertext)):
        try:
            message += nr_to_letter[ (  letter_to_nr[ciphertext[i]] - letter_to_nr[key[i % len(key)]] ) % len(ALPHABET) ]
        except KeyError:
            print('Letter not in dictionary!')
    return message

def findTextProbability(text):
    letters_to_amount = dict(zip(ALPHABET, [0 for i in range(len(ALPHABET))]))
    letters_to_probability = dict(zip(ALPHABET, [0. for i in range(len(ALPHABET))]))
    total = 0
    for letter in text:
        if letter in ALPHABET:
            letters_to_amount[letter] += 1
            total += 1
    for letter in ALPHABET:
        letters_to_probability[letter] += letters_to_amount[letter]/total
    return letters_to_probability

def isAllDictType(dictionary, typeOfValue = int):
    for value in dictionary.values():
        if not isinstance(value, typeOfValue):
            return 0
    return 1

# multiplicating values of 2 dictionaries with each other and summing them up
def dictValuesMultiply(dictA, dictB, offset = 0):
    if len(dictA) != len(dictB):
        return -1
    if not isAllDictType(dictA, float) or not isAllDictType(dictB, float):
        return -2

    offset %= len(ALPHABET)
    alphabetTmp = ALPHABET[:]
    alphabetTmp += ALPHABET[:offset]
    alphabetTmp = alphabetTmp[offset:]
    multiplicationValue = 0
    for i in range(len(ALPHABET)):
        multiplicationValue += dictA[ALPHABET[i]] * dictB[alphabetTmp[i]]
    return multiplicationValue

# make a list of numbers of similar letters within a string and its shifted(shift changes) copy
def findSimilarityTable(ciphertext):
    similarity = []
    for i in range(1, len(ciphertext)):
        tmpSimilarity = 0
        for j in range(len(ciphertext) - i):
            if ciphertext[i+j] == ciphertext[j]:
                tmpSimilarity += 1
        similarity.append(tmpSimilarity)
    return similarity

# finding the size of gaps between "high numbers" from a list
def findInterval(similarity, maxValue):
    tmpGap = 0
    intervals = []
    for i in range(len(similarity)):
        if i == 0 and similarity[i] >= maxValue:
            tmpGap = 1
            continue
        if similarity[i] >= maxValue:
            intervals.append(tmpGap)
            tmpGap = 1
        else:
            tmpGap += 1
    return intervals

def findKeyLength_Friedman(ciphertext, maxValueMultiplicator = 0.8):
    similarity = findSimilarityTable(ciphertext)

    # for the second half of the list, the numbers will be much lower, so I'm not gonna use them
    halfLength = len(similarity)//2
    del similarity[halfLength:]
    
    # getting the highest values from the list
    maxValue = max(similarity)
    maxValue = maxValue * maxValueMultiplicator

    # the sizes of gaps between highest values may be key length's
    possibleKeys = findInterval(similarity, maxValue)
    if not possibleKeys:    
        possibleKeys.append(len(ciphertext))

    return round(mean(possibleKeys))

#finding letter with statistic analysis
def findLetterOfTheKey(ciphertext, langLetterPossibilities):
    letters_to_probability = findTextProbability(ciphertext)
    bestTmpOffset = -1
    bestTmpProbability = -1
    for offset in range(len(ALPHABET)):
        tmpProbability = dictValuesMultiply(langLetterPossibilities, letters_to_probability, offset)
        if tmpProbability > bestTmpProbability:
            bestTmpProbability = tmpProbability
            bestTmpOffset = offset
    return nr_to_letter[bestTmpOffset]


def findKey(keyLength, ciphertext, langLetterPossibilities):
    key = ''
    tmpCiphertext = ''
    for position in range(keyLength):
        for i in range(position, len(ciphertext), keyLength):
            tmpCiphertext += ciphertext[i]
        key += findLetterOfTheKey(tmpCiphertext, langLetterPossibilities)

    return key


def readFile(fileName = 'Vigenere.txt'):
    inFile = open(fileName, 'rt')
    text = ''.join(inFile.readlines())
    inFile.close()
    return text


def avgDistance(ciphertext, word):
    length = len(word)
    positions = []
    for i in range(len(ciphertext) - length + 1):
        if ciphertext[i:i+length] == word:
            positions.append(i)

    gaps = []
    for i in range(len(positions) - 1):
        gaps.append( positions[i+1] - positions[i] )
    if len(positions) <= 1:
        return -1
    positions.clear()
    return sum(gaps)/len(gaps)


def findKeyLength_Kasiski(ciphertext, langLetterPossibilities):
    double = {}
    tripple = {}
    for i in range(len(ciphertext) - 2):
        if ciphertext[i:i+2] in double:
            double[ciphertext[i:i+2]] += 1
        else:
            double[ciphertext[i:i+2]] = 1
        if ciphertext[i:i+3] in tripple:
            tripple[ciphertext[i:i+3]] += 1
        else:
            tripple[ciphertext[i:i+3]] = 1
    reversedDouble = [[value, key] for (key, value) in double.items()]
    reversedTripple = [[value, key] for (key, value) in tripple.items()]
    reversedDouble.sort(reverse=True)
    reversedTripple.sort(reverse=True)
    del reversedDouble[6:]
    del reversedTripple[3:]
    possibleKeys = []
    for i in reversedDouble:
        possibleKeys.append( avgDistance(ciphertext, i[1]) )
    for i in reversedTripple:
        possibleKeys.append( avgDistance(ciphertext, i[1]) )
    return possibleKeys


def isPolish(text):
    notPolish = 'XQV'
    for letter in text:
        if letter in notPolish:
            return False
    return True




def bruteForceCaesar(ciphertext):
    for i in range(len(ALPHABET)):
        decrypted = decrypt(ALPHABET[i], ciphertext)
        if isPolish(decrypted):
            print(i, ": ", decrypted[:10])
    writing = int(input("Który tekst najbardziej przypomina wiadomość w języku polskim: "))
    return ALPHABET[writing]


if __name__ == '__main__':
    print('Czytanie pliku...')
    ciphertext = readFile()
    print('Deszyfrowanie...')

    # keyLength = findKeyLength_Friedman(ciphertext, 0.9 )
    # print('Odzyskana długość klucza: ', keyLength)
    # key = findKey(keyLength, ciphertext, polishLetterPossibilities)
    # print('Odzyskany klucz: ', key)
    # message = decrypt(key, ciphertext)
    # print('Odszyfrowana wiadomość: ', message)
    


    print("Możliwe, że długość klucza jest równa NWD większości z tych liczb:")
    print(findKeyLength_Kasiski(ciphertext, polishLetterPossibilities))
    

    possibleKeyLength = int(input("Jaki długi jest według Ciebie klucz: "))

    possibleKey = ''
    ciphertexts = ['' for i in range(possibleKeyLength)]
    for i in range(len(ciphertext)):
        ciphertexts[i%possibleKeyLength] += ciphertext[i]
        
    for text in ciphertexts:
        possibleKey += bruteForceCaesar(text)
    
    print("Możliwy klucz: ", possibleKey)
    mostPossibleKey = input("Wprowadź klucz: ").upper()

    print('Szyfrogram:')
    print(decrypt(mostPossibleKey, ciphertext))

    


    # out = open('resultsOfVigenere.txt', 'wt')
    # out.write(message)
    # out.close()
















