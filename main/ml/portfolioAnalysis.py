from companyAnalysis import predictor
from dbAccess import dbAccessor


class portfolioPredictor:
    def __init__(self):
        self.companyPredic = predictor()
        self.userId = None
        self.allStocks = None

    def categorizePortfolio(self, stockList):
        companyAnan = []
        companyDict = {}
        for row in stockList:
            prediction = self.companyPredic.getAnalysis(row[1])  # row[1] contains company symbol
            companyAnan.append([prediction, row[7]])
        # print companyAnan
        for row in companyAnan:
            if companyDict.get(row[1]):
                if row[0] == 'BUY':
                    companyDict[row[1]] += 1
                elif row[0] == 'SELL':
                    companyDict[row[1]] -= 1
            else:
                if row[0] == 'BUY':
                    companyDict[row[1]] = 1
                elif row[0] == 'SELL':
                    companyDict[row[1]] = -1
                else:
                    companyDict[row[1]] = 0
        return companyDict

    def getPortfolioAnalysis(self, userId):
        self.userId = userId
        db = dbAccessor()
        self.allStocks = db.getInvestments(self.userId)
        return self.categorizePortfolio(self.allStocks)

    def getTopPerformers(self, category='all', top=True):
        db = dbAccessor()
        companiesReturn = []
        companyList = db.companiesOfType(category)
        for row in companyList:
            companiesReturn.append((row[1], self.companyPredic.getMonthlyReturns(row[2])))
        return sorted(companiesReturn, reverse=top, key=lambda x: x[1])
