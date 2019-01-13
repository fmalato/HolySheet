import json
try:
    import Queue as Q
except ImportError:
    import queue as Q

# Dato un txt in ingresso, lo legge e crea un dizionario che ha come chiavi il nome della pagina con il numero di
# colonna (0 o 1), e come valore un array di interi ordinato con il testo che indica la quantita' di parole per ogni
# riga

def getWordsCounterDict(lines):

    columnsLengthDict = dict()

    for i in range(len(lines)):

        # Trovo nel txt le righe speciali di inizio paragrafo, saranno chiave nel dizionario
        if lines[i][0] == "_":
            columnsLengthDict[lines[i][:-1]] = []

            # Per ogni riga adesso conto quante parole ci sono e me lo salvo
            j = i + 1
            while j < len(lines) and lines[j][0] is not "_":
                columnsLengthDict[lines[i][:-1]].append(wordCounter(lines[j]))
                j += 1

            # per risparmiare cicli adesso riparto dal nuovo paragrafo
            i = j

    return columnsLengthDict

'''
def wordCounter(line):

    words = 0

    for letter in line:
        if letter is " " or letter is "=":
            words += 1

    return words
'''

def wordCounter(line):

    words = line.split()

    return len(words)



def histWords(lines):

    histWords = dict()

    for i in range(len(lines)):
        if lines[i][0] == "_":
            continue
        else:
            words = lines[i].split()
            for word in words:
                if word[len(word) - 1] is "=" or word[len(word) - 1] is ".":
                    if word[: len(word) - 2] in histWords:
                        histWords[word[: len(word) - 2]] += 1
                    else:
                        histWords[word[: len(word) - 2]] = 1
                else:
                    if word in histWords:
                        histWords[word] += 1
                    else:
                        histWords[word] = 1

    return histWords


def getNmostFrequentWords(hist, n):

    frequent = []

    for key in hist.keys():
        frequent.append(hist[key])

    frequent.sort(reverse=True)
    print(frequent)

    mostFrequentWords = []
    for i in range(n):
        for key in hist.keys():
            if hist[key] is frequent[i]:
                mostFrequentWords.append(key)

    return mostFrequentWords


def getDictWordPosition(lines, specificWord):

    wordDict = dict()
    page = ""
    nLine = 0

    for i in range(len(lines)):

        # Trovo nel txt le righe speciali di inizio paragrafo, primo elemento della tupla
        if lines[i][0] == "_":
            page = lines[i][:-1]
            nLine = 0

        # Altrimenti trovo una riga vera, splitto le parole e le conto
        else:
            words = lines[i].split()

            for i in range(len(words)):
                if words[i][len(words[i]) - 1] == "=" or words[i][len(words[i]) - 1] == ".":
                    if words[i][: len(words[i]) - 2] == specificWord:
                        wordDict[str((page, nLine, i))] = 1
                elif words[i] == specificWord:
                    wordDict[str((page, nLine, i))] = 1

            nLine += 1

    return wordDict

'''
# Leggo il ground truth e me lo salvo in un file come dizionario json, per non stare a rileggerlo ad ogni esecuzione


groundTruth = open("genesis1-20.txt", "r")
lines = groundTruth.readlines()

dictionary = getWordsCounterDict(lines)

with open('JsonUtils/groundTruthDictionary.json', 'w') as fp:
    json.dump(dictionary, fp)


#hist = histWords(lines)


with open('JsonUtils/10mostFrequentWords.json') as mf:
    mostFrequentWords = json.load(mf)

# Dizionario che ha come chiave la tupla per ritrovare la parola nel testo, pagina e colonna, numero riga e numero di
# parola

# tupla = ('_P0_C0', 20, 3)

for frequentWord in mostFrequentWords:
    with open('JsonUtils/{frequentWord}Positions.json'.format(frequentWord=frequentWord), 'w') as fw:
        json.dump(getDictWordPosition(lines, frequentWord), fw)


print("Finished")



'''
