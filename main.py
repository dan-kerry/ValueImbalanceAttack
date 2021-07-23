from mesa import Agent, Model
from mesa.time import RandomActivation
from numpy import random
import pandas as pd
import pickle
import math
import os

import time
import matplotlib.pyplot as plt


items = ["red", "blue", "green", "orange", "purple", "yellow", "amber", "brown", "pink", "cyan", "lilac", "magenta",
         "mauve", "mint", "peach", "violet", "sapphire", "sepia", "tan", "turqoise", "vanilla", "zomp"]

prices = {"red": 10, "blue": 5, "green": 7, "orange": 12, "purple": 4, "yellow": 20, "amber": 25, "brown": 11,
          "pink": 6, "cyan": 9, "lilac": 32, "magenta": 5, "mauve": 25, "mint": 13, "peach": 8, "violet": 30,
          "sapphire": 12, "sepia": 5, "tan": 4, "turqoise": 18, "vanilla": 10, "zomp": 50}

listing = []
orders = []
deliveries = []
oldestInteraction = 0

def clear():
    os.system('clear')

def getItem():
    return items[random.randint(0, len(items))]

def getList(quantity):
    desires = []
    while len(desires) < quantity:
        item = getItem()
        if item not in desires:
            desires.append(item)
    return desires

def sellerDishonestyBinary(list):
    pos = 0
    neg = 0
    for x in range(len(list)):
        if list[x] == True:
            pos += 1
        elif list[x] == False:
            neg += 1
        else:
            pass
    chance = (pos + 1) / (neg + pos + 2)
    return chance

class orderSheet():
    def __init__(self, BuyerID, SellerID, price, item, SaleDate = None, ExpectedArrivalDate = None, ActualArrivalDate = None):
        self.BuyerID = BuyerID
        self.SellerID = SellerID
        self.price = price
        self.item = item
        self.SaleDate = SaleDate
        self.ExpectedArrivalDate = ExpectedArrivalDate
        self.ActualArrivalDate = ActualArrivalDate

    def __str__(self):
        return f"BuyerID: {self.BuyerID}, SellerID: {self.SellerID}, Price: {self.price}, Item: {self.item}, Due: {self.ExpectedArrivalDate}, Sale: {self.SaleDate}, Actual: {self.ActualArrivalDate}"

class Buyer(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.wealth = int(random.triangular(5, 10, 15))
        self.desires = getList(int(random.triangular(0, 1, 3)))
        self.inventory = []
        self.MSRPs = []
        self.orders = []
        self.orderCount = 0
        self.patience = int(random.triangular(1, 3, 5))
        self.patience = 3
        self.riskAversion = random.triangular(0.4, 0.85, 0.95)
        self.positiveInteractions = 0
        self.negativeInteractions = 0

    def evaluateItems(self):
        '''Returns a single item in the market (or sometimes none), that the buyer should buy'''
        MaxPercent = 5
        MaxPercentPrice = 0
        MaxPercentInd = 0
        MaxPercentItem = None
        DealFound = False

        self.MSRPs = []
        if len(self.desires) > 0:
            for z in range(len(self.desires)):
                self.MSRPs.append(prices[self.desires[z]])

            for x in range(len(self.desires)):
                for y in range(len(listing)):
                    #Selects item with greatest percentage discount
                    if self.desires[x] in listing[y][0]:
                        ind = listing[y][0].index(self.desires[x])
                        sellerPrice = listing[y][1][ind]
                        discount = sellerPrice / self.MSRPs[x]
                        if discount < MaxPercent:
                            MaxPercent = discount
                            MaxPercentPrice = sellerPrice
                            MaxPercentInd = listing[y][2]
                            MaxPercentItem = self.desires[x]
                            DealFound = True
                        elif discount == MaxPercent:
                            if sellerPrice > MaxPercentPrice:
                                MaxPercent = discount
                                MaxPercentPrice = sellerPrice
                                MaxPercentInd = listing[y][2]
                                MaxPercentItem = self.desires[x]

            MaxPercentResult = orderSheet(self.unique_id, MaxPercentInd, MaxPercentPrice, MaxPercentItem)
            if DealFound:
                return MaxPercentResult

        else:
            return None

    def evaluateItemsBinary(self):
        bestPrice = 1000
        bestPriceID = 0
        truePrice = 0
        if len(self.desires) > 0:
            for x in range(len(listing)):
                if self.desires[0] in listing[x][0]:
                    sellerRep = sellerDishonestyBinary(Test.feedback[listing[x][2]])
                    if sellerRep < self.riskAversion:
                        #print(f"Buyer: {self.unique_id} has a maximum risk of {self.riskAversion}, so would not trade with seller {listing[x][2]}, with a score of {sellerRep}")
                        continue
                    ind = listing[x][0].index(self.desires[0])
                    sellerPrice = listing[x][1][ind]
                    riskAdjustedPrice = sellerPrice / sellerRep
                    if riskAdjustedPrice < bestPrice:
                        bestPrice = riskAdjustedPrice
                        bestPriceID = listing[x][2]
                        truePrice = sellerPrice
            RiskAdjustedResult = orderSheet(self.unique_id, bestPriceID, truePrice, self.desires[0])
            return RiskAdjustedResult
        else:
            return None

    def makePurchase(self):
        '''Acts on the recommendation of the self.evaluateItems function'''
        if Test.epoch < 40:
            order = self.evaluateItems()
        elif Test.epoch >= 40:
            order = self.evaluateItemsBinary()

        if order != None:
            #print(order.item)
            if self.wealth > order.price:
                self.wealth -= order.price
                order.ExpectedArrivalDate, order.SaleDate = Test.epoch + 5 + self.patience, Test.epoch
                orders.append(order)
                self.orderCount += 1
                try:
                    temp_index = self.desires.index(order.item)
                except:
                    print(Test.epoch)
                    print(order)
                    print(self.desires)
                    exit()
                self.desires[temp_index] = None

            delList = []
            for z in range(len(self.desires)):
                if self.desires[z] == None:
                    delList.append(z)
            if len(delList) < 2:
                for a in range(len(delList)):
                    del(self.desires[delList[a]])
            else:
                self.desires = []
            '''for z in range(len(self.desires)):
                if self.desires[z] == None:
                    self.desires.pop(z)'''

        else:
            pass

    def evaluateOrders(self):
        '''Checks all active orders to see if items have arrived or not'''
        for i in range(len(orders)):
            if orders[i].BuyerID == self.unique_id:
                if Test.epoch == orders[i].ExpectedArrivalDate:
                    if orders[i].ActualArrivalDate > orders[i].ExpectedArrivalDate:
                        Test.feedback[orders[i].SellerID].append(False)
                        self.negativeInteractions += 1
                        if Test.epoch > 10:
                            orders.pop(i)
                            break

                    elif orders[i].ActualArrivalDate <= orders[i].ExpectedArrivalDate:
                        Test.feedback[orders[i].SellerID].append(True)
                        self.positiveInteractions += 1
                        self.inventory.append(orders[i].item)
                        if Test.epoch > 10:
                            orders.pop(i)
                            break

    def newItems(self):
        if self.desires == []:
            #TODO: Find a better way to assign new items
            if random.randint(0,2) == 1:
                self.desires.append(getItem())

    def makeMoney(self):
        #TODO: Increase complexity of wealth increase
        earnings = int(random.triangular(2, 3, 4))
        self.wealth += earnings

    def step(self):
        self.makePurchase()
        self.evaluateOrders()
        self.newItems()
        self.makeMoney()

        #print(f"BuyerID: {self.unique_id}, Desires: {self.desires}, Inventory: {self.inventory}, Wealth: {self.wealth}")

class Seller(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.inventory = getList(int(random.triangular(2, 3, 4)))
        self.prices = []
        self.tracking = []
        for i in range(len(self.inventory)):
            self.tracking.append([0, 0])
        self.accuracy = int(random.triangular(1, 35, 50))
        self.speed = int(random.triangular(3, 6, 8))
        self.ordersReceived = 0
        self.ordersCorrect = 0
        self.ordersIncorrect = 0

        for x in range(len(self.inventory)):
            temp = prices[self.inventory[x]]
            temp = int(random.triangular(temp-2, temp, temp+2))
            self.prices.append(temp)
        listing.append([self.inventory, self.prices, self.unique_id])

    def generateDeliveryTime(self, date):
        test_digit = random.randint(0, self.accuracy)
        singleUseSpeed = int(random.triangular(self.speed - 2, self.speed, self.speed + 2))
        #TODO: Make delivery time rely more heavily on parameters
        if test_digit < 3:
            return (date + singleUseSpeed + 5)
        else:
            return (date + singleUseSpeed)

    def orderCheck(self):
        for y in range(len(orders)):
            '''if orders[y] == None:
                continue'''
            if orders[y].SellerID == self.unique_id and orders[y].ActualArrivalDate == None :
                self.ordersReceived += 1
                deliveryDate = self.generateDeliveryTime(orders[y].SaleDate)
                orders[y].ActualArrivalDate = deliveryDate
                if orders[y].ActualArrivalDate > orders[y].ExpectedArrivalDate:
                    self.ordersIncorrect += 1
                elif orders[y].ActualArrivalDate <= orders[y].ExpectedArrivalDate:
                    self.ordersCorrect += 1

                try:
                    x = self.inventory.index(orders[y].item)
                    self.tracking[x][0] += 1
                    self.tracking[x][1] = 0
                except:
                    pass
    #Time

    def updatePrices(self):
        saleLimit = 50
        reductionLimit = 25
        """If Item is sold 50+ times, it is removed from stock and replaced by a new item"""
        """If an item goes 25 iterations without a sale, its price is reduced by 1"""
        for i in range(len(self.tracking)):
            self.tracking[i][1] += 1
            if self.tracking[i][0] > saleLimit:
                while True:
                    newitem = getItem()
                    if newitem in self.inventory:
                        continue
                    else:
                        break
                self.inventory[i] = newitem
                self.tracking[i] = [0, 0]
                #Setting new prices for regenerated items
                newPrice = int(random.triangular(prices[newitem]-2, prices[newitem], prices[newitem]+2))
                self.prices[i] = newPrice
                index_loc = math.floor((self.unique_id / 2))
                listing[index_loc][0], listing[index_loc][1] = self.inventory, self.prices
            if self.tracking[i][1] > reductionLimit:
                self.prices[i] -= 1
                self.tracking[i][1] = 0

    def __str__(self):
        return f"Inventory: {self.inventory}, Prices: {self.prices}, Tracking: {self.tracking}"

    def step(self):
        self.orderCheck()
        self.updatePrices()

class Attacker():
    def __init__(self):
        self.profit = 0
        self.createListing()
        self.dispatchTime = 4
        self.crossoverPoint = 0.7

    def createListing(self):
        fake_listing = [["mint", "peach"], [11, 7], 0]
        listing.append(fake_listing)

    def HonestTrading(self):
        new_listing = [["mint", "peach"], [11, 7], 0]
        listing[0] = new_listing

    def orderCheck(self, Honest):
        if Honest:
            for y in range(len(orders)):
                if orders[y].SellerID == 0 and orders[y].ActualArrivalDate == None :
                    orders[y].ActualArrivalDate = self.dispatchTime + Test.epoch
        else:
            for y in range(len(orders)):
                if orders[y].SellerID == 0 and orders[y].ActualArrivalDate == None :
                    orders[y].ActualArrivalDate = self.dispatchTime + Test.epoch + 500
                    self.profit += orders[y].price

    def valueImbalance(self):
            new_listing = [["zomp"], [45], 0]
            listing[0] = new_listing

    def act(self):
        if sellerDishonestyBinary(Test.feedback[0]) < self.crossoverPoint:
            self.HonestTrading()
            self.orderCheck(True)
        elif sellerDishonestyBinary(Test.feedback[0]) >= self.crossoverPoint:
            self.valueImbalance()
            self.orderCheck(False)

        '''print(listing[0])
        print(sellerDishonestyBinary(Test.feedback[0]))
        print(self.wealth)'''

class Market(Model):
    def __init__(self, B = 100, S = 50):
        self.numOfBuyers = B
        self.numOfSellers = S
        self.schedule = RandomActivation(self)
        self.epoch = 0
        self.feedback = []
        #dataReturn is structured as [[Seller Data], [Buyer Data], [Attack Data]]
        self.dataReturn = [[], [], []]

        for x in range(1050):
            self.feedback.append([])

        for i in range(2, self.numOfBuyers * 2, 2):
            a = Buyer(i)
            self.schedule.add(a)

        for i in range(1, self.numOfSellers * 2, 2):
            b = Seller(i)
            self.schedule.add(b)

    def calculateSellerTrust(self):
        for i in range(len(self.feedback)):
            if self.feedback[i] != []:
                pos = 0
                neg = 0
                for j in range(len(self.feedback[i])):
                    if self.feedback[i][j] == True:
                        pos += 1
                    elif self.feedback[i][j] == False:
                        neg += 1
                print(f"Seller No: {i}, Positive: {pos}, Negative: {neg}, Total: {pos+neg}")

    def storeData(self):
        buyerCols = ["wealth", "purchases", "riskAversion", "posInteractions", "negInteractions", "patience"]
        BuyerDF = pd.DataFrame(columns=buyerCols, index=range(self.numOfBuyers))
        sellerCols = ["feedback", "speed", "ordersRec", "ordersPos", "ordersNeg"]
        SellerDF = pd.DataFrame(columns=sellerCols, index=range(self.numOfSellers))

        #Buyer Data Tracking
        pos = 0
        for agent in Test.schedule.agents:
            if agent.unique_id % 2 == 0:
                BuyerDF.loc[pos].wealth = agent.wealth
                BuyerDF.loc[pos].purchases = agent.orderCount
                BuyerDF.loc[pos].riskAversion = agent.riskAversion
                BuyerDF.loc[pos].posInteractions = agent.positiveInteractions
                BuyerDF.loc[pos].negInteractions = agent.negativeInteractions
                BuyerDF.loc[pos].patience = agent.patience
                pos += 1

        #Seller Data Tracking
        pos2 = 0
        for j in range(1, self.numOfSellers * 2, 2):
            #print(f"Seller: {j}, Feedback: {Buyer.sellerDishonestyBinary(None, self.feedback[j])}")
            individualFeeback = sellerDishonestyBinary(self.feedback[j])
            SellerDF.loc[pos2].feedback = individualFeeback
            pos2 += 1
        pos2 = 0
        for agent in Test.schedule.agents:
            if agent.unique_id % 2 != 0:
                SellerDF.loc[pos2].speed = agent.speed
                SellerDF.loc[pos2].ordersRec = agent.ordersReceived
                pos2 += 1

        #Attacker Data Tracking
        AttackerRep = sellerDishonestyBinary(Test.feedback[0])
        AttackTurn = [AttackerRep, Attack.profit]
        self.dataReturn[0].append(BuyerDF)
        self.dataReturn[1].append(SellerDF)
        self.dataReturn[2].append(AttackTurn)

    def displayProgress(self):
        clear()
        print(f"Epoch: {self.epoch} \n"
              f"Buyers: {self.numOfBuyers} \n"
              f"Sellers: {self.numOfSellers} \n")

    def step(self):
        self.schedule.step()
        self.epoch += 1
        self.storeData()
        self.displayProgress()

def exportData(dataSet, fileName):
    pickle.dump(dataSet, open(fileName, "wb"))

def main():
    time_list = []
    steps = int(input("No. of Epochs?"))
    for x in range(steps):
        Attack.act()
        start = time.time()
        Test.step()
        end = time.time()
        result = end - start
        time_list.append(result)
    fig, ax = plt.subplots()
    ax.plot(time_list, color="red")
    plt.show()
    #exportData(Test.dataReturn, "DataOutputs/AttackDataTest4")

Attack = Attacker()
Test = Market()
main()
