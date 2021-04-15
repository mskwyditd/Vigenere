from statistics import mean

# ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZęóąśłżźćńĘÓĄŚŁŻŹĆŃ '
# ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
# ALPHABET = 'abcdefghijklmnopqrstuvwxyz '
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

# CONVERTION = { 'ą':'a', 'ę''e' , 'ó':'o', 'ś':'s', 'ł':'l', 'ż':'z', 'ź':'z', 'ć':'c', 'ń':'n',
# 'Ą':'A', 'Ę''E' , 'Ó':'O', 'Ś':'S', 'Ł':'L', 'Ż':'Z', 'Ź':'Z', 'Ć':'C', 'Ń':'N' }

# CONVERTION = { 'ą':'a', 'ę''e' , 'ó':'o', 'ś':'s', 'ł':'l', 'ż':'z', 'ź':'z', 'ć':'c', 'ń':'n',
# 'Ą':'a', 'Ę''e' , 'Ó':'o', 'Ś':'s', 'Ł':'l', 'Ż':'z', 'Ź':'z', 'Ć':'c', 'Ń':'n' }

# polishLetterPossibilities = { 'a':8.91, 'ą':0.99, 'b':1.47, 'c':3.96, 'ć':0.4, 'd':3.25, 'e':7.66, 'ę':1.11, 'f':0.3, 'g':1.42,
# 'h':1.08, 'i':8.21, 'j':2.28, 'k':3.51, 'l':2.1, 'ł':1.82, 'm':2.8, 'n':5.52, 'ń':0.2, 'o':7.75, 'ó':0.85, 'p':3.13, 'q':0.14,
# 'r':4.69, 's':4.32, 'ś':0.66, 't':3.98, 'u':2.5, 'v':0.04, 'w':4.65, 'x':0.02, 'y':3.76, 'z':5.64, 'ź':0.06, 'ż':0.83, ' ':3.0 }

# polishLetterPossibilities = { 'a':8.91, 'b':1.47, 'c':3.96, 'd':3.25, 'e':7.66, 'f':0.3, 'g':1.42,
# 'h':1.08, 'i':8.21, 'j':2.28, 'k':3.51, 'l':2.1, 'm':2.8, 'n':5.52, 'o':7.75, 'p':3.13, 'q':0.14,
# 'r':4.69, 's':4.32, 't':3.98, 'u':2.5, 'v':0.04, 'w':4.65, 'x':0.02, 'y':3.76, 'z':5.64,  ' ':4.0 }

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
    newKey = ''
    alphabetLen = len(ALPHABET)
    for i in key:
        try:
            newKey += nr_to_letter[ alphabetLen - letter_to_nr[i] -1 ]
        except KeyError:
            print('Letter not in dictionary!')
    return encrypt(newKey, ciphertext)

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


if __name__ == '__main__':
    print('Czytanie pliku: ')
    ciphertext = readFile()
    print('Deszyfrowanie...')
    keyLength = findKeyLength_Friedman(ciphertext, 0.9 )
    print('Odzyskana długość klucza: ', keyLength)
    key = findKey(keyLength, ciphertext, polishLetterPossibilities)
    print('Odzyskany klucz: ', key)
    message = decrypt(key, ciphertext)
    print('Odszyfrowana wiadomość: ', message)

    # out = open('resultsOfVigenere.txt', 'wt')
    # out.write(message)
    # out.close()
















