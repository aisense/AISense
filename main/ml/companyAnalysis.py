import json
import os


class predictor:
    profitMax = 1.2
    lossMax = 0.8
    volumeDifference = 0.2
    historicGain = 1.03

    def __init__(self):
        self.symbol = None
        self.returnStatus = None
        self.message = None
        self.holding = None
        pass

    def getData(self, companySymbol):
        with open(os.path.dirname(__file__) + '\\data\\' + companySymbol + '.json') as data_file:
            data = json.load(data_file)
        return data['query']['results']['quote']

    def getDetails(self, data, howMany=250):
        High, Low, Close, Volume, count = 0, 0, 0, 0, 0
        for row in data:
            count += 1
            High += float(row['High'])
            Low += float(row['Low'])
            Close += float(row['Close'])
            Volume += float(row['Volume'])
            if count > howMany:
                break
        High = High / count
        Low = Low / count
        Close = Close / count
        Volume = Volume / count
        return (High, Low, Close, Volume)

    def getOneDayDetails(self, data, whichDay):
        whichDay = -1 * whichDay
        nextDay = whichDay + 1
        return data[whichDay:nextDay]

    def limitAnalysis(self, closeData):
        from dbAccess import dbAccessor
        db = dbAccessor()
        userHoldings = db.getCompanyInvestement(self.symbol)
        buyPrice = userHoldings[3]
        buyToCurrentRation = buyPrice / float(closeData['Close'])
        if buyToCurrentRation > predictor.profitMax:
            self.returnStatus = "SELL"
            self.message = 'It would be best to book profits and sell.'
            return self.returnStatus
        elif buyToCurrentRation < predictor.lossMax:
            self.returnStatus = "SELL"
            self.message = 'Cut your losses and sell the stock'
            return self.returnStatus

    def historyBasedAnalysis(self, data):
        details30 = self.getDetails(data, 30)
        detailsAll = self.getDetails(data, len(data))
        if details30[2] / detailsAll[2] > predictor.historicGain:
            if self.holding:
                self.returnStatus = "HOLD"
                self.message = 'The company has been in an upward trend.'
                return self.returnStatus
            else:
                self.returnStatus = "BUY"
                self.message = 'The company has been in an upward trend.'
                return self.returnStatus
        else:
            if self.holding:
                self.returnStatus = "SELL"
                self.message = 'The company has been in a downward trend.'
                return self.returnStatus
            else:
                self.returnStatus = "IGNORE"
                self.message = 'The company has been in a downward trend.'
                return self.returnStatus

    def getAnalysis(self, companySymbol, holding=False):
        self.symbol = companySymbol
        self.holding = holding
        data = self.getData(companySymbol)
        if self.holding:
            limits = self.limitAnalysis(data[len(data) - 1])
            if limits:
                return self.returnStatus
        return self.historyBasedAnalysis(data)

    def getMonthlyReturns(self, companySymbol):
        data = self.getData(companySymbol)
        data30 = self.getDetails(data, 30)
        dataOne = self.getOneDayDetails(data, 30)
        return float(dataOne[0]['Close']) / data30[2]
