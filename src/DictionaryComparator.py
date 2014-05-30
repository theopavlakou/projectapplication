
class DictionaryComparator:
    """ Given two dictionaries with words as keys and ranks as values,
    this class is used to make various comparisons between them."""

    def __init__(self, dictionaryOld, dictionaryCurrent):
        self.dictOld = dictionaryOld
        self.dictCurrent = dictionaryCurrent
        self.wordsOld = set(self.dictOld.keys())
        self.wordsCurrent = set(self.dictCurrent.keys())
        self.wordsDifferentOld = set()
        self.wordsDifferentCurrent = set()

    def getOldWordsNotInCurrent(self):
        if not self.wordsDifferentOld:
            self.wordsDifferentOld = self.wordsOld.difference(self.wordsCurrent)
        return self.wordsDifferentOld

    def getCurrentWordsNotInOld(self):
        if not self.wordsDifferentCurrent:
            self.wordsDifferentCurrent = self.wordsCurrent.difference(self.wordsOld)
        return self.wordsDifferentCurrent

    def getCommonWords(self):
        return self.wordsCurrent.intersection(self.wordsOld)

    def getIndexChangesFromOldToCurrent(self):
        commonWords = self.getCommonWords()
        indexChanges = {}
        for commonWord in commonWords:
            indexChanges[self.dictOld[commonWord]] = self.dictCurrent[commonWord]
        return indexChanges

    def getIndexOfWordsNotInCurrent(self):
        indexNotInCurrent = set()
        for word in self.getOldWordsNotInCurrent():
            indexNotInCurrent.add(self.dictOld[word])
        return indexNotInCurrent

    def getIndexOfWordsNotInOld(self):
        indexNotInOld = set()
        for word in self.getCurrentWordsNotInOld():
            indexNotInOld.add(self.dictCurrent[word])
        return indexNotInOld