'''This file contains classes used for users' bank accounts'''

class Account:
    def __init__(self, id, DatabaseObject):
        #Attributes
        self.db = DatabaseObject
        self.ID = id
        # self.__db_cursor =  self.__db.cursor() #creating local cursor
        self.__FirstName = None #Setting new method to None allows to define attributes later
        self.__SecondName = None

    def setAttributes(self):#the method tht sets "empty" atributes
        self.__db_cursor =  self.db.cursor() #creating local cursor
        self.__db_cursor.execute('''SELECT * FROM Accounts WHERE ID == ?''', (self.ID,)) #the app requires only ID because users can have two idenical pins, but not two idenical IDs
        self.__accountInfo = self.__db_cursor.fetchone() #a tulp with all account information

        self.__FirstName = self.__accountInfo[1]
        self.__SecondName = self.__accountInfo[2]

    #Getters methods
    def getFirstName(self):
        return self.__FirstName

    def getSecondName(self):
        return self.__SecondName

class CheckingAccount(Account):
    def __init__(self, id, DatabaseObject):
        Account.__init__(self, id, DatabaseObject)
        #New Attributes
        self.__balance = None

    def setAttributes(self):
        self.__db_cursor =  self.db.cursor() #creating local cursor
        self.__db_cursor.execute('''SELECT * FROM Accounts WHERE ID == ?''', (self.ID,)) #the app requires only ID because users can have two idenical pins, but not two idenical IDs
        self.__accountInfo = self.__db_cursor.fetchone() #a tulp with all account information

        self.__AccountID = self.__accountInfo[0]
        self.__FirstName = self.__accountInfo[1]
        self.__SecondName = self.__accountInfo[2]

        self.__db_cursor.execute('''SELECT * FROM Bank WHERE AccountID == ?''', (self.__AccountID,)) #getting the info on account with same account id
        self.__balanceInfo = self.__db_cursor.fetchone() #a tulp with balance information
        self.__balance = self.__balanceInfo[1]

    #Mutators for new attribute
    def withdraw(self, amount):
        if self.__balance < amount: #if there is less funds on checking account then asked amount
            return 1 #indicator of insuficent funds
        else:
            self.__balance = self.__balance - amount #subtracting from the local variable
            self.__db_cursor.execute('''UPDATE Bank SET CheckingBalance == ? WHERE AccountID == ?''', (self.__balance, self.__AccountID))
            self.db.commit() #writing down changes into the db
            return 0 #indicator that operation went thru

    def deposit(self, amount):
        self.__balance = self.__balance + amount #adding to the local variable
        self.__db_cursor.execute('''UPDATE Bank SET CheckingBalance == ? WHERE AccountID == ?''', (self.__balance, self.__AccountID))
        self.db.commit() #writing down changes into the db
    
    #Accesor for the new attribute
    def getBalance(self):
        return self.__balance

class SavingAccount(Account):
    def __init__(self, id, DatabaseObject):
        Account.__init__(self, id, DatabaseObject)
        #New Attributes
        self.__balance = None
        self.__withdrawLimit = None #limit to woh many times money can be windrawn
    
    def setAttributes(self):
        self.__db_cursor =  self.db.cursor() #creating local cursor
        self.__db_cursor.execute('''SELECT * FROM Accounts WHERE ID == ?''', (self.ID,)) #the app requires only ID because users can have two idenical pins, but not two idenical IDs
        self.__accountInfo = self.__db_cursor.fetchone() #a tulp with all account information

        self.__AccountID = self.__accountInfo[0]
        self.__FirstName = self.__accountInfo[1]
        self.__SecondName = self.__accountInfo[2]

        self.__db_cursor.execute('''SELECT * FROM Bank WHERE AccountID == ?''', (self.__AccountID,)) #getting the info on account with same account id
        self.__balanceInfo = self.__db_cursor.fetchone() #a tulp with balance information
        self.__balance = self.__balanceInfo[2] #mutated attribute so it shows saving account
        self.__withdrawLimit = self.__balanceInfo[3] #limit to woh many times money can be windrawn

    def withdraw(self, amount):
        if self.__balance < amount: #if there is less funds on checking account then asked amount
            return 1 #indicator of insuficent funds
        elif self.__withdrawLimit == 0:
            return 2 #indicator that user can't withdraw money from savings
        else:
            self.__balance = self.__balance - amount #subtracting from the local variable
            self.__withdrawLimit = self.__withdrawLimit - 1
            self.__db_cursor.execute('''UPDATE Bank SET SavingBalance == ? WHERE AccountID == ?''', (self.__balance, self.__AccountID)) #dividing command in two to make things less complicated
            self.__db_cursor.execute('''UPDATE Bank SET SavingWithdrawLimit == ? WHERE AccountID == ?''', (self.__withdrawLimit, self.__AccountID))
            self.db.commit() #writing down changes into the db
            return 0 #indicator that operation went thru

    def deposit(self, amount):
        self.__balance = self.__balance + amount #adding to the local variable
        self.__db_cursor.execute('''UPDATE Bank SET SavingBalance == ? WHERE AccountID == ?''', (self.__balance, self.__AccountID))
        self.db.commit() #writing down changes into the db

    def getWithdrawLimit(self):
        return self.__withdrawLimit

    def getBalance(self):
        return self.__balance


'''Main'''
if __name__ == "__main__":
    pass
