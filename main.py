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
        if list[x][0] == True:
            pos += 1
        elif list[x][0] == False:
            neg += 1
        else:
            pass
    chance = (pos + 1) / (neg + pos + 2)
    return chance

def sellerDishonestyValueAdjusted(list):
    pos = 0
    neg = 0
    for x in range(len(list)):
        if list[x][0] == True:
            pos += list[x][1]
        elif list[x][0] == False:
            neg += list[x][1]
    try:
        return (pos + 1) / (neg + pos + 2)
    except:
        return 0.4


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
        DealFound = False

        if len(self.desires) > 0:
            for q in range(len(listing)):
                if self.desires[0] in listing[q][0]:
                    sellerRep = sellerDishonestyBinary(Sim.feedback[listing[q][2]])
                    #sellerRep = sellerDishonestyValueAdjusted(Sim.feedback[listing[q][2]])
                    if sellerRep > self.riskAversion:
                        ind = listing[q][0].index(self.desires[0])
                        sellerPrice = listing[q][1][ind]
                        riskAdjustedPrice = sellerPrice / sellerRep
                        if riskAdjustedPrice < bestPrice:
                            bestPrice = riskAdjustedPrice
                            bestPriceID = listing[q][2]
                            truePrice = sellerPrice
                            DealFound = True

        if DealFound:
            RiskAdjustedResult = orderSheet(self.unique_id, bestPriceID, truePrice, self.desires[0])
            return RiskAdjustedResult
        else:
            return None

    def makePurchase(self):
        if Sim.epoch < 100:
            order = self.evaluateItems()
        else:
            order = self.evaluateItemsBinary()

        if order != None:
            if order.price < 1:
                pass
            if self.wealth > order.price:
                self.wealth -= order.price
                order.ExpectedArrivalDate = Sim.epoch + 5 + self.patience
                order.SaleDate = Sim.epoch
                newKey = list(Sim.orderDict)[-1] + 1
                Sim.orderDict[newKey] = order
                Sim.orderTrack[self.unique_id].append(newKey)
                Sim.orderTrack[order.SellerID].append(newKey)
                self.orderCount += 1
                temp_index = self.desires.index(order.item)
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
        for i in range(len(Sim.orderTrack[self.unique_id])-1, -1, -1):
            orderKey = Sim.orderTrack[self.unique_id][i]
            seller_ID = Sim.orderDict[orderKey].SellerID
            if Sim.epoch == Sim.orderDict[orderKey].ExpectedArrivalDate:
                if Sim.orderDict[orderKey].ActualArrivalDate > Sim.orderDict[orderKey].ExpectedArrivalDate:
                    Sim.feedback[Sim.orderDict[orderKey].SellerID].append([False, Sim.orderDict[orderKey].price, Sim.orderDict[orderKey].SaleDate])
                    self.negativeInteractions += 1
                    del(Sim.orderTrack[self.unique_id][i])
                    Sim.orderTrack[seller_ID].remove(orderKey)
                    del(Sim.orderDict[orderKey])

                elif Sim.orderDict[orderKey].ActualArrivalDate <= Sim.orderDict[orderKey].ExpectedArrivalDate:
                    Sim.feedback[Sim.orderDict[orderKey].SellerID].append([True, Sim.orderDict[orderKey].price, Sim.orderDict[orderKey].SaleDate])
                    self.positiveInteractions += 1
                    self.inventory.append(Sim.orderDict[orderKey].item)
                    del(Sim.orderTrack[self.unique_id][i])
                    Sim.orderTrack[seller_ID].remove(orderKey)
                    del (Sim.orderDict[orderKey])


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
            self.tracking.append([0, 0, 0])
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
        for y in range(len(Sim.orderTrack[self.unique_id])):
            orderKey = Sim.orderTrack[self.unique_id][y]
            if Sim.orderDict[orderKey].ActualArrivalDate == None :
                self.ordersReceived += 1
                deliveryDate = self.generateDeliveryTime(Sim.orderDict[orderKey].SaleDate)
                Sim.orderDict[orderKey].ActualArrivalDate = deliveryDate
                if Sim.orderDict[orderKey].ActualArrivalDate > Sim.orderDict[orderKey].ExpectedArrivalDate:
                    self.ordersIncorrect += 1
                elif Sim.orderDict[orderKey].ActualArrivalDate <= Sim.orderDict[orderKey].ExpectedArrivalDate:
                    self.ordersCorrect += 1

                try:
                    x = self.inventory.index(Sim.orderDict[orderKey].item)
                    self.tracking[x][0] += 1
                    self.tracking[x][1] = 0
                except:
                    pass

    def updatePrices(self):
        saleLimit = 50
        reductionLimit = 25
        removeLimit = 3
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
                self.tracking[i] = [0, 0, 0]
                #Setting new prices for regenerated items
                newPrice = int(random.triangular(prices[newitem]-2, prices[newitem], prices[newitem]+2))
                self.prices[i] = newPrice
                index_loc = math.floor((self.unique_id / 2))
                listing[index_loc][0], listing[index_loc][1] = self.inventory, self.prices

            if self.tracking[i][1] > reductionLimit:
                self.prices[i] -= 1
                self.tracking[i][1] = 0
                self.tracking[i][2] += 1

            if self.tracking[i][2] > removeLimit:
                while True:
                    newitem = getItem()
                    if newitem in self.inventory:
                        continue
                    else:
                        break
                self.inventory[i] = newitem
                self.tracking[i] = [0, 0, 0]
                #Setting new prices for regenerated items
                newPrice = int(random.triangular(prices[newitem]-2, prices[newitem], prices[newitem]+2))
                self.prices[i] = newPrice
                index_loc = math.floor((self.unique_id / 2))
                listing[index_loc][0], listing[index_loc][1] = self.inventory, self.prices

    def __str__(self):
        return f"Inventory: {self.inventory}, Prices: {self.prices}, Tracking: {self.tracking}"

    def step(self):
        self.orderCheck()
        self.updatePrices()


class Attacker():
    def __init__(self):
        self.profit = 0
        self.dispatchTime = 4
        self.crossoverPoint = 0.85
        self.AttackItem = "zomp"

    def reset(self):
        self.profit = 0
        self.dispatchTime = 4
        self.crossoverPoint = 0.85

    def createListing(self):
        fake_listing = [["mint", "peach"], [3, 3], 0]
        listing.append(fake_listing)

    def orderCheck(self):
        for y in range(len(Sim.orderTrack[0])):
            orderKey = Sim.orderTrack[0][y]
            if Sim.orderDict[orderKey].ActualArrivalDate == None:
                if Sim.orderDict[orderKey].item != self.AttackItem:
                    Sim.orderDict[orderKey].ActualArrivalDate = self.dispatchTime + Sim.epoch
                    #self.profit += Sim.orderDict[orderKey].price

                elif Sim.orderDict[orderKey].item == self.AttackItem:
                    Sim.orderDict[orderKey].ActualArrivalDate = self.dispatchTime + Sim.epoch + 500
                    self.profit += Sim.orderDict[orderKey].price

    def valueImbalance(self):
        lowPrice = 100
        for x in range(len(listing)):
            if self.AttackItem in listing[x][0]:
                z_index = listing[x][0].index(self.AttackItem)
                z_price = listing[x][1][z_index]
                if z_price < lowPrice:
                    lowPrice = z_price
        newPrice = lowPrice - 1
        new_listing = [[self.AttackItem], [newPrice], 0]
        listing[-1] = new_listing


    def regularTrading(self):
        new_listing = [["mint", "peach"], [4, 4], 0]
        listing[-1] = new_listing

    def act(self):
        if Sim.epoch == 100:
            self.createListing()
        elif Sim.epoch > 100:
            if sellerDishonestyBinary(Sim.feedback[0]) < self.crossoverPoint:
                self.regularTrading()
            elif sellerDishonestyBinary(Sim.feedback[0]) >= self.crossoverPoint:
                self.valueImbalance()
        self.orderCheck()


class Market(Model):
    def __init__(self, B = 200, S = 50):
        self.numOfBuyers = B
        self.numOfSellers = S
        self.schedule = RandomActivation(self)
        self.epoch = 0
        self.feedback = []
        self.orderDict = {0: None}
        self.orderTrack = []
        for x in range(self.numOfBuyers*2):
            self.orderTrack.append([])
        for x in range(self.numOfSellers * 2):
            self.feedback.append([])
        #dataReturn is structured as [[Seller Data], [Buyer Data], [Attack Data]]
        self.dataReturn = [[], [], []]
        self.newDataReturn = []
        for i in range(2, self.numOfBuyers * 2, 2):
            a = Buyer(i)
            self.schedule.add(a)

        for i in range(1, self.numOfSellers * 2, 2):
            b = Seller(i)
            self.schedule.add(b)


    def reset(self):
        self.numOfBuyers = self.numOfBuyers
        self.numOfSellers = self.numOfSellers
        self.schedule = RandomActivation(self)
        self.epoch = 0
        self.feedback = []
        self.orderDict = {0: None}
        self.orderTrack = []
        for x in range(self.numOfBuyers * 2):
            self.orderTrack.append([])
        for x in range(self.numOfSellers * 2):
            self.feedback.append([])
        # dataReturn is structured as [[Seller Data], [Buyer Data], [Attack Data]]
        self.dataReturn = [[], [], []]
        self.newDataReturn = []
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
        pos2 = 0

        for agent in Sim.schedule.agents:
            if agent.unique_id % 2 == 0:
                BuyerDF.loc[pos].wealth = agent.wealth
                BuyerDF.loc[pos].purchases = agent.orderCount
                BuyerDF.loc[pos].riskAversion = agent.riskAversion
                BuyerDF.loc[pos].posInteractions = agent.positiveInteractions
                BuyerDF.loc[pos].negInteractions = agent.negativeInteractions
                BuyerDF.loc[pos].patience = agent.patience
                pos += 1
            if agent.unique_id % 2 != 0:
                SellerDF.loc[pos2].speed = agent.speed
                SellerDF.loc[pos2].ordersRec = agent.ordersReceived
                pos2 += 1

        #Seller Data Tracking
        pos3 = 0
        for j in range(1, self.numOfSellers * 2, 2):
            individualFeeback = sellerDishonestyBinary(self.feedback[j])
            SellerDF.loc[pos3].feedback = individualFeeback
            pos3 += 1

        #Attacker Data Tracking
        AttackerRep = sellerDishonestyBinary(Sim.feedback[0])
        AttackTurn = [AttackerRep, Attack.profit]
        self.dataReturn[0].append(BuyerDF)
        self.dataReturn[1].append(SellerDF)
        self.dataReturn[2].append(AttackTurn)

    def displayProgress(self):
        #clear()
        print(f"Epoch: {self.epoch} \n"
              f"Buyers: {self.numOfBuyers} \n"
              f"Sellers: {self.numOfSellers} \n")

    def newDataStore(self):
        AttackerRep = sellerDishonestyBinary(Sim.feedback[0])
        AttackTurn = [AttackerRep, Attack.profit]
        self.newDataReturn.append(AttackTurn)


    def step(self):
        self.schedule.step()
        self.epoch += 1
        #self.storeData()
        self.newDataStore()
        self.displayProgress()

def exportData(dataSet, fileName):
    pickle.dump(dataSet, open(fileName, "wb"))

Sim = Market()
Attack = Attacker()

def run(var):
    steps = 500
    for x in range(steps):
        Attack.crossoverPoint = var
        Attack.act()
        Sim.step()
    #return Sim.newDataReturn
    exportData(Sim.newDataReturn, "7AugTest")

run(0.85)



