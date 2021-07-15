from mesa import Agent, Model
from mesa.time import RandomActivation
from numpy import random
import pandas as pd
import pickle
import math

'''Is mesa.DataCollector a usable solution?'''

items = ["red", "blue", "green", "orange", "purple", "yellow"]
prices = {"red": 10, "blue": 5, "green": 7, "orange": 12, "purple": 3, "yellow": 20}
listing = []
orders = []
deliveries = []

def getItem():
    return items[random.randint(0, len(items))]

def getList(quantity):
    desires = []
    while len(desires) < quantity:
        item = getItem()
        if item not in desires:
            desires.append(item)
    return desires

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

class orderTrack():
    def __init__(self, BuyerID, SellerID, SaleDate, ExpectedArrivalDate, ActualArrivalDate = None):
        self.BuyerID = BuyerID
        self.SellerID = SellerID
        self.SaleDate = SaleDate
        self.ExpectedArrivalDate = ExpectedArrivalDate
        self.ActualArrivalDate = ActualArrivalDate

    def __str__(self):
        return f"BuyerID: {self.BuyerID}, SellerID: {self.SellerID}, Due: {self.ExpectedArrivalDate}, Sale: {self.SaleDate}, Actual: {self.ActualArrivalDate}"

class Buyer(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.wealth = int(random.triangular(5, 10, 15))
        self.desires = getList(int(random.triangular(0, 1, 2)))
        self.inventory = []
        self.MSRPs = []
        self.orders = []
        self.patience = int(random.triangular(1, 3, 5))

    #TODO: BUY THE CHEAPEST ABOVE A THRESHOLD (I.E. THEIR RISK TOLERANCE)
    def evaluateItems(self):
        '''Returns a single item in the market (or sometimes none), that the buyer should buy'''
        provisionalOrder = []
        MaxPercent = 5
        MaxPercentPrice = 0
        MaxPercentInd = 0
        MaxPercentItem = None
        CheapFirstPrice = 100
        CheapFirstSeller = 0
        HighScore = 0
        HighScoreInd = 0
        HighScorePrice = 0

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
                        elif discount == MaxPercent:
                            if sellerPrice > MaxPercentPrice:
                                MaxPercent = discount
                                MaxPercentPrice = sellerPrice
                                MaxPercentInd = listing[y][2]
                                MaxPercentItem = self.desires[x]

                    #Buys first item in desires at cheapest price
                    if self.desires[0] in listing[y][0]:
                        ind = listing[y][0].index(self.desires[0])
                        price = listing[y][1][ind]
                        if price < CheapFirstPrice:
                            CheapFirstPrice = price
                            CheapFirstSeller = listing[y][2]

                    #Buys First item from highest reputation seller
                    if self.desires[0] in listing[y][0]:
                        ind_feedback = Test.feedback[listing[y][2]]
                        positive = 0
                        negative = 0
                        for q in range(len(ind_feedback)):
                            if ind_feedback[q] == True:
                                positive += 1
                            elif ind_feedback[q] == False:
                                negative += 1
                        try:
                            score = positive / (positive + negative)
                        except ZeroDivisionError:
                            score = 0
                        if score > HighScore:
                            HighScore = score
                            HighScoreInd = listing[y][2]
                            ind = listing[y][0].index(self.desires[0])
                            HighScorePrice = listing[y][1][ind]

            MaxPercentResult = orderSheet(self.unique_id, MaxPercentInd, MaxPercentPrice, MaxPercentItem)
            FirstListedItem = orderSheet(self.unique_id, CheapFirstSeller, CheapFirstPrice, self.desires[0])
            BestFeedback = orderSheet(self.unique_id, HighScoreInd, HighScorePrice, self.desires[0])

            tempIndicator = random.randint(1, 2)
            #tempIndicator = 2

            '''if tempIndicator == 0:
                return MaxPercentResult
            elif tempIndicator == 1:
                return FirstListedItem'''
            #TODO: Make buyer decision making more atomic (functions?)
            while Test.epoch < 25:
                tempIndicator = random.randint(1, 2)
                # tempIndicator = 2
                if tempIndicator == 0:
                    return MaxPercentResult
                elif tempIndicator == 1:
                    return FirstListedItem
            while Test.epoch >= 25:
                return BestFeedback

        else:
            provisionalOrder = None
            return provisionalOrder

    def makePurchase(self):
        '''Acts on the recommendation of the self.evaluateItems function'''
        order = self.evaluateItems()
        if order != None:
            if self.wealth > order.price:
                self.wealth -= order.price
                order.ExpectedArrivalDate, order.SaleDate = Test.epoch + 5 + self.patience, Test.epoch
                orders.append(order)
                self.desires[self.desires.index(order.item)] = None

            delList = []
            for z in range(len(self.desires)):
                if self.desires[z] == None:
                    delList.append(z)
            if len(delList) < 2:
                for a in range(len(delList)):
                    del(self.desires[delList[a]])
            else:
                self.desires = []
        else:
            pass

    def evaluateOrders(self):
        '''Checks all active orders to see if items have arrived or not'''
        for i in range(len(orders)):
            if orders[i].BuyerID == self.unique_id:
                if Test.epoch == orders[i].ActualArrivalDate:
                    if orders[i].ActualArrivalDate > orders[i].ExpectedArrivalDate:
                        Test.feedback[orders[i].SellerID].append(False)

                    elif orders[i].ActualArrivalDate <= orders[i].ExpectedArrivalDate:
                        Test.feedback[orders[i].SellerID].append(True)
                        self.inventory.append(orders[i].item)

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
            self.tracking.append([0,0])
        self.accuracy = int(random.triangular(1, 35, 50))
        self.speed = int(random.triangular(2, 4, 6))

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
            if orders[y] == None:
                continue
            if orders[y].SellerID == self.unique_id and orders[y].ActualArrivalDate == None :
                deliveryDate = self.generateDeliveryTime(orders[y].SaleDate)
                orders[y].ActualArrivalDate = deliveryDate
                x = self.inventory.index(orders[y].item)
                self.tracking[x][0] += 1
                self.tracking[x][1] = 0

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
                listing[index_loc][0], listing[index_loc][1]  = self.inventory, self.prices
            if self.tracking[i][1] > reductionLimit:
                self.prices[i] -= 1
                self.tracking[i][1] = 0

    def __str__(self):
        return f"Inventory: {self.inventory}, Prices: {self.prices}, Tracking: {self.tracking}"

    def step(self):
        self.orderCheck()
        self.updatePrices()

class Attacker():
    def __init__(self, wealth = 0):
        self.wealth = wealth
        self.inventory = ["yellow"]

    def createListing(self):
        fake_listing = [["blue"], [2], 0]
        listing.append(fake_listing)

    def step(self):
        self.createListing()

class Market(Model):
    def __init__(self, B = 100, S = 35):
        self.numOfBuyers = B
        self.numOfSellers = S
        self.schedule = RandomActivation(self)
        self.epoch = 0
        self.feedback = []
        self.dataReturn = []

        for x in range(1000):
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
        cols = ["wealth"]
        BuyerDF = pd.DataFrame(columns=cols, index=range(self.numOfBuyers))
        SellerDF = pd.DataFrame()
        pos = 0
        for agent in Test.schedule.agents:
            if agent.unique_id % 2 == 0:
                BuyerDF.loc[pos].wealth = agent.wealth
                pos += 1
        self.dataReturn.append(BuyerDF)

    def step(self):
        self.schedule.step()
        self.epoch += 1
        #print(listing)
        print(self.epoch)
        self.calculateSellerTrust()
        self.storeData()

def exportData(dataSet, fileName):
    pickle.dump(dataSet, open(fileName, "wb"))


Test = Market()
Attack = Attacker()


steps = int(input("No. of Epochs?"))
for x in range(steps):
    Test.step()
    Attack.step()
#exportData(Test.dataReturn, "TestOutput")
