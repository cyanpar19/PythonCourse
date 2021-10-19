# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 15:03:11 2021

@author: Celal Yanpar - cyanpar19

CSSM 502 - Homework 1
"""
import numpy
class Portfolio():
    def __init__(self): #constructor of Portfolio Class
        self.stocks = [] #list of stocks
        self.mfs = [] #list of mutual funds
        self.cash=0
        self.transaction_record = [] # list of transactions that are used in history functions
        msg = "New Portfolio created"
        self.transaction_record.append(msg)
        print(msg)
    
    def __str__(self): #overriding print function for portfolio printing
        print("\nPORTFOLIO: ")
        print("cash: " + str(self.cash) + "$")
        print("stocks:")
        for i in self.stocks:
            print("       " +str(i["share"]) +" "+i["investment"].symbol)
        print("mutual funds:")
        for k in self.mfs:
            print("       " +str(k["share"]) +" "+k["investment"].symbol)   
        return "\n"
        
    def history(self): #returns list of transaction accroding to creation time, fifo
        print("\nHISTORY: ")
        for i in self.transaction_record:
            print(i + "\n")
        
    def addCash(self, amount): #adds Cash
        self.cash = self.cash + amount
        msg = "Adds cash to new portfolio: " + str(amount)+ "$"
        print(msg)
        self.transaction_record.append(msg)
    
    def withdrawCash(self, amount): #withdraw cash if user has enough money
        if amount <= self.cash:
            self.cash = self.cash - amount
            msg = "Removes: " + str(amount) +"$"
            print(msg)
            self.transaction_record.append(msg)
        else:
            print("You dont have enough money to withdraw")

    def buyStock(self,share,stock): #buy stock if user has enough money
        cost = share * stock.buy_price
        check=False
        if cost <= self.cash:
            self.cash = self.cash - cost
            for i in self.stocks: # check user already has same stock
                if i["investment"].symbol == stock.symbol:
                    i["investment"] = i["investment"] + share #increase the stock share
                    check = True
            if check == False:
                self.stocks.append({"investment": stock, "share": share })
            msg = "Buys " + str(share) + " shares of stock " + stock.symbol
            print(msg)
            self.transaction_record.append(msg)
        else:
            print("You dont have enough money")
            return
        
    def buyMutualFund(self,share,mf):#buy mutual fund if user has enough money
        cost = share * mf.buy_price
        check=False
        if cost <= self.cash:
            self.cash = self.cash - cost
            for i in self.mfs: # check user already has same stock
                if i["investment"].symbol == mf.symbol:
                    i["investment"] = i["investment"] + share #increase the mf share
                    check = True
            if check == False:
                self.mfs.append({"investment": mf, "share": share})
            msg = "Buys " + str(share) + " shares of mutual fund " + mf.symbol
            print(msg)
            self.transaction_record.append(msg)
        else:
            print("You dont have enough money")
            return
        
    def sellStock(self, symbol, share): #sell stock and add revenue into the portfolio as cash
        for i in self.stocks:
            if i["investment"].symbol == symbol:
                if i["share"]>= share:
                    revenue = i["investment"].sell_price * share
                    self.cash = self.cash + revenue
                    i["share"] = i["share"] - share #decrease the stock share
                    msg = "Sells " + str(share) + " of " + symbol
                    print(msg)
                    self.transaction_record.append(msg)
                    if i["share"] == 0:  #remove stock from the portfolio if its share equal to 0
                        self.stocks.remove(i)
                    return    
                else:
                    print("You dont have enough share to sell")
                    return
            else:
               print("You dont have this type of stock")
               return 
        
    def sellMutualFund(self,symbol, share): #sell mf and add revenue into the portfolio as cash
        for i in self.mfs:
            if i["investment"].symbol == symbol:
                if i["share"]>= share:
                    revenue = i["investment"].sell_price * share
                    self.cash = self.cash + revenue
                    i["share"] = i["share"] - share #decrease the mf share
                    msg = "Sells " + str(share) + " of " + symbol
                    print(msg)
                    self.transaction_record.append(msg)
                    if i["share"] == 0:#remove mf from the portfolio if its share equal to 0
                        self.mfs.remove(i)
                    return    
                else:
                    print("You dont have enough share to sell")
                    return
            else:
               print("You dont have this type of mutual fund")
               return 


class Stock(): 
    def __init__(self,buy_price,symbol):# constructor of stock class
        self.buy_price = buy_price
        self.symbol = symbol
        self.sell_price = numpy.random.uniform(0.5*buy_price,1.5*buy_price)
        msg = "Create stock with price " + str(buy_price) + " and symbol " + symbol
        print(msg)


class MutualFund():
    def __init__(self, symbol):  #constructor of stock class   
        self.buy_price = 1
        self.symbol = symbol
        self.sell_price = numpy.random.uniform(0.9,1.2)
        msg = "Create MF with symbol " + symbol
        print(msg)

def test():
    portfolio = Portfolio() 
    portfolio.addCash(300.50) 
    s = Stock(20, "HFH") 
    portfolio.buyStock(5, s)
    mf1 = MutualFund("BRT") 
    mf2 = MutualFund("GHT") 
    portfolio.buyMutualFund(10.3, mf1) 
    portfolio.buyMutualFund(2, mf2) 
    print(portfolio)
    portfolio.sellMutualFund("BRT", 3) 
    portfolio.sellStock("HFH", 1) 
    portfolio.withdrawCash(50) 
    portfolio.history()

if __name__ == '__main__':    
    test()