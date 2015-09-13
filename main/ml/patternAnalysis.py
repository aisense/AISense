from dbAccess import dbAccessor
import operator


class patternAnalyser:
    maxOffers = 3

    def __init__(self, userId):
        self.db = dbAccessor()
        self.userId = userId
        self.purchases = self.db.getUserPurchases(self.userId)

    def frequentPurchases(self):
        freq = {}
        for row in self.purchases:
            if freq.get(row[3]):
                freq[row[3]] += 1
            else:
                freq[row[3]] = 1
        sortedData = sorted(freq.items(), reverse=True, key=operator.itemgetter(1))
        return sortedData

    def amountPattern(self):
        freq = {}
        for row in self.purchases:
            if freq.get(row[3]):
                freq[row[3]] += row[2]
            else:
                freq[row[3]] = row[2]
        sortedData = sorted(freq.items(), reverse=True, key=operator.itemgetter(1))
        return sortedData

    def locationPattern(self):
        freq = {}
        for row in self.purchases:
            if freq.get(row[5]):
                freq[row[5]] += 1
            else:
                freq[row[5]] = 1
        sortedData = sorted(freq.items(), reverse=True, key=operator.itemgetter(1))
        return sortedData

    def getOfferList(self, method='amount'):
        if method == 'amount':
            offerType = self.amountPattern()
        elif method == 'frequency':
            offerType = self.frequentPurchases()
        else:
            offerType = self.locationPattern()
        count = 0
        offer = []
        for x in offerType:
            count += 1
            if method == 'location':
                temp = self.db.getOffers(False, x[0])
            else:
                temp = self.db.getOffers(x[0])
            offer.append(temp)
            if count > patternAnalyser.maxOffers:
                break
        return offer
