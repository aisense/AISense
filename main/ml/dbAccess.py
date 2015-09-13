import MySQLdb
class dbAccessor:
    def __init__(self):
        db =  MySQLdb.connect("localhost", "root", "root","socgen")
        self.cursor = db.cursor()
        self.error = False

    def getTransactions(self, userId, limit=6, order='DESC'):
        query = "select * from transtable where userid ="+userId
        self.cursor.execute(query)
        if self.cursor.rowcount < 1:
            self.error = "No previous transactions for the user"
            return False
        else:
            return self.cursor.fetchall()

    def getInvestments(self,userId):
        queryString = "select * from investments i, company c where userid="+str(userId)+" and c.symbol = i.symbol"
        self.cursor.execute(queryString)
        if self.cursor.rowcount < 1:
            return False
        else:
            return self.cursor.fetchall()
        pass

    def companiesOfType(self,category='ALL', order = 'DESC'):
        if category == 'ALL':
            queryString = "select * from company"
        else:
            queryString = "select * from company WHERE ctype='"+category+"'"

        self.cursor.execute(queryString)
        return self.cursor.fetchall()

    def getCompanyInvestement(self, companySymbol):
        queryString = "select * from investments where symbol ='"+companySymbol+"'"
        self.cursor.execute(queryString)
        return self.cursor.fetchone()

    '''def userLogin(self, userName, password):
        queryString = "select * from usertable where username="+userName+"and password="+password
        self.cursor.execute(queryString)
        if self.cursor.rowcount != 1:
            self.error = "Sorry, you are not a member of the bank"
            return False
        else:
            return self.cursor.fetchone()
    '''

    def getUserPurchases(self, userId):
        queryString = "select * from usertrans t, users u where u.uid ="+str(userId)+" and u.acno = t.acno"
        self.cursor.execute(queryString)
        return self.cursor.fetchall()

    def getOffers(self, category, location =False):
        if location:
            queryString = "select * from offers where location='"+location+"' order by discount desc limit 1  "
        else:
            queryString = "select * from offers where ptype = '"+category+"' order by discount desc limit 1  "
        self.cursor.execute(queryString)
        return self.cursor.fetchone()

