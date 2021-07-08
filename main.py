from mesa import Agent, Model
from mesa.time import RandomActivation
from numpy import random

items = ["red", "blue", "green", "orange"]
prices = {"red": 10, "blue": 5, "green": 7, "orange": 12}
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
        self.desires = getList(int(random.triangular(1, 3, 5)))
        self.inventory = []
        self.MSRPs = []
        for x in range(len(self.desires)):
            self.MSRPs.append(prices[self.desires[x]])

        self.orders = []
        self.patience = 0

    def evaluateItems(self):
        provisionalOrder = []
        MaxPercent = 5
        MaxPercentPrice = 0
        MaxPercentInd = 0
        MaxPercentItem = None
        CheapFirstPrice = 100
        CheapFirstSeller = 0

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

                if self.desires[0] in listing[y][0]:
                    ind = listing[y][0].index(self.desires[0])
                    price = listing[y][1][ind]
                    if price < CheapFirstPrice:
                        CheapFirstPrice = price
                        CheapFirstSeller = listing[y][2]

        MaxPercentResult = orderSheet(self.unique_id, MaxPercentInd, MaxPercentPrice, MaxPercentItem)
        FirstListedItem = orderSheet(self.unique_id, CheapFirstSeller, CheapFirstPrice, self.desires[0])

        tempIndicator = random.randint(0, 1)

        if tempIndicator == 0:
            return MaxPercentResult
        elif tempIndicator == 1:
            return FirstListedItem
        return provisionalOrder

    def makePurchase(self):
        order = self.evaluateItems()
        if order == None:
            pass
        if self.wealth > order.price:
            self.wealth -= order.price
            order.ExpectedArrivalDate, order.SaleDate = Test.epoch + 5, Test.epoch
            orders.append(order)
            '''NEEDS BETTER CALCULATION BASED ON PARAMETERS'''
            #dueDate = Test.epoch + 5
            #incomingOrder = orderTrack(self.unique_id, order.SellerID, Test.epoch, dueDate)
            #self.orders.append(incomingOrder)
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

    def evaluateOrders(self):
        for i in range(len(orders)):
            if orders[i].BuyerID == self.unique_id:
                if Test.epoch == orders[i].ActualArrivalDate:
                    if orders[i].ActualArrivalDate > orders[i].ExpectedArrivalDate:
                        Test.feedback[orders[i].SellerID].append(False)
                    elif orders[i].ActualArrivalDate <= orders[i].ExpectedArrivalDate:
                        Test.feedback[orders[i].SellerID].append(True)

    def leaveFeedback(self):
        pass

    def newItems(self):
        if self.desires == []:
            self.desires.append(getItem())

    def makeMoney(self):
        earnings = int(random.triangular(2, 3, 4))
        self.wealth += earnings

    def step(self):
        self.makePurchase()
        self.evaluateOrders()
        self.newItems()
        self.makeMoney()
        print(f"BuyerID: {self.unique_id}, Desires: {self.desires}, Inventory: {self.inventory}, Wealth: {self.wealth}")

class Seller(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.inventory = getList(int(random.triangular(2, 3, 4)))
        self.prices = []
        self.pendingOrders = []
        self.accuracy = int(random.triangular(1, 35, 50))
        self.speed = int(random.triangular(2, 5, 8))
        '''Assigns Sellers with varied prices'''
        for x in range(len(self.inventory)):
            temp = prices[self.inventory[x]]
            temp = int(random.triangular(temp-2, temp, temp+2))
            self.prices.append(temp)

        listing.append([self.inventory, self.prices, self.unique_id])

    def generateDeliveryTime(self, date):
        test_digit = random.randint(0, self.accuracy)
        if test_digit < 3:
            return (date + self.speed + 5)
        else:
            return (date + self.speed)

    def orderCheck(self):
        for y in range(len(orders)):
            if orders[y] == None:
                continue
            if orders[y].SellerID == self.unique_id and orders[y].ActualArrivalDate == None :
                deliveryDate = self.generateDeliveryTime(orders[y].SaleDate)
                orders[y].ActualArrivalDate = deliveryDate

        for i in range(len(self.pendingOrders)):
            print(self.pendingOrders[i])


    def step(self):
        self.orderCheck()


class Market(Model):
    def __init__(self, B = 10, S = 5):
        self.numOfBuyers = B
        self.numOfSellers = S
        self.schedule = RandomActivation(self)
        self.epoch = 0
        self.feedback = []
        for x in range(300):
            self.feedback.append([])

        for i in range(1, self.numOfSellers * 2, 2):
            a = Seller(i)
            self.schedule.add(a)

        for i in range(0, self.numOfBuyers * 2, 2):
            a = Buyer(i)
            self.schedule.add(a)

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

                print(f"Seller No: {i}, Positive: {pos}, Negative: {neg}")

    def step(self):
        self.schedule.step()
        self.epoch += 1
        print(listing)

        print(self.epoch)
        self.calculateSellerTrust()

Test = Market()

while True:
    input("Continue?")
    Test.step()





