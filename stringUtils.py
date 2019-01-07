import json

# Dato un txt in ingresso, lo legge e crea un dizionario che ha come chiavi il nome della pagina con il numero di
# colonna (0 o 1), e come valore un array di interi ordinato con il testo che indica la quantita' di parole per ogni
# riga

def getWordsCounterDict(lines):

    columnsLengthDict = dict()

    for i in range(len(lines)):

        # Trovo nel txt le righe speciali di inizio paragrafo, saranno chiave nel dizionario
        if lines[i][0] == "_":
            columnsLengthDict[lines[i][:-2]] = []

            # Per ogni riga adesso conto quante parole ci sono e me lo salvo
            j = i + 1
            while j < len(lines) and lines[j][0] is not "_":
                columnsLengthDict[lines[i][:-2]].append(wordCounter(lines[j]))
                j += 1

            # per risparmiare cicli adesso riparto dal nuovo paragrafo
            i = j

    return columnsLengthDict


def wordCounter(line):

    words = 0

    for letter in line:
        if letter is " " or letter is "=":
            words += 1

    return words

# Leggo il ground truth e me lo salvo in un file come dizionario json, per non stare a rileggerlo ad ogni esecuzione

groundTruth = open("genesis1-20.txt", "r")
lines = groundTruth.readlines()

dictionary = getWordsCounterDict(lines)

with open('groundTruthDictionary.json', 'w') as fp:
    json.dump(dictionary, fp)