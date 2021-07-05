from mesa import Agent, Model
from mesa.time import RandomActivation
from numpy import random

items = ["red", "blue", "green", "orange"]
prices = {"red": 10, "blue": 5, "green": 7, "orange": 12}
listing = []
orders = []

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
    def __init__(self, BuyerID, SellerID, price, item):
        self.BuyerID = BuyerID
        self.SellerID = SellerID
        self.price = price
        self.item = item

    def __str__(self):
        return f"BuyerID: {self.BuyerID}, SellerID: {self.SellerID}, Price: {self.price}, Item: {self.item}"

class Buyer(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.wealth = int(random.triangular(5, 10, 15))
        self.desires = getList(int(random.triangular(1, 3, 5)))
        self.inventory = []
        self.MSRPs = []
        for x in range(len(self.desires)):
            self.MSRPs.append(prices[self.desires[x]])
        self.memory = []

    def priceEvaluation(self):
        pass

    def evaluateItems(self):
        provisionalOrder = None

        for x in range(len(self.desires)):
            for y in range(len(listing)):
                biggestPercent = 5
                if self.desires[x] in listing[y][0]:
                    ind = listing[y][0].index(self.desires[x])
                    sellerPrice = listing[y][1][ind]
                    discount = sellerPrice / self.MSRPs[x]
                    if discount < biggestPercent:





        return provisionalOrder

    def makePurchase(self):
        order = self.evaluateItems()
        if order == None:
            pass

    def evaluateOrders(self):
        pass

    def leaveFeedback(self):
        pass

    def step(self):
        '''Search listings for items that are in buyer's list'''
        self.evaluateItems()
        for x in range(len(self.desires)):
            currentLow = 100
            sellerID = 0
            for y in range(len(listing)):
                if self.desires[x] in listing[y][0]:
                    ind = listing[y][0].index(self.desires[x])
                    price = listing[y][1][ind]
                    if price < currentLow:
                        currentLow = price
                        sellerID = listing[y][2]
            '''If the Buyer can afford the item, they buy it'''
            if self.wealth > currentLow:
                self.wealth -= currentLow
                newOrder = orderSheet(self.unique_id, sellerID, currentLow, self.desires[x])
                orders.append(newOrder)

                self.inventory.append(self.desires[x])
                self.desires[x] = None

        delList = []
        for z in range(len(self.desires)):
            if self.desires[z] == None:
                delList.append(z)
        if len(delList) < 2:
            for a in range(len(delList)):
                del(self.desires[delList[a]])
        else:
            self.desires = []

        print(f"BuyerID: {self.unique_id}, Desires: {self.desires}, Inventory: {self.inventory}, Wealth: {self.wealth}")

class Seller(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.inventory = getList(int(random.triangular(2, 3, 4)))
        self.prices = []
        self.pendingOrders = []
        self.accuracy = 1
        self.speed = 1
        '''Assigns Sellers with varied prices'''
        for x in range(len(self.inventory)):
            temp = prices[self.inventory[x]]
            temp = int(random.triangular(temp-2, temp, temp+2))
            self.prices.append(temp)
        listing.append([self.inventory, self.prices, self.unique_id])

    def orderCheck(self):
        for y in range(len(orders)):
            if orders[y] == None:
                continue
            if orders[y].SellerID == self.unique_id:
                self.pendingOrders.append(orders[y])
                orders[y] = None

    def step(self):
        self.orderCheck()

class Market(Model):
    def __init__(self, B = 10, S = 5):
        self.numOfBuyers = B
        self.numOfSellers = S
        self.schedule = RandomActivation(self)

        for i in range(1, self.numOfSellers * 2, 2):
            a = Seller(i)
            self.schedule.add(a)

        for i in range(0, self.numOfBuyers * 2, 2):
            a = Buyer(i)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()
        print(listing)


Test = Market()
while True:
    input("Continue?")
    Test.step()
