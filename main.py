from mesa import Agent, Model
from mesa.time import RandomActivation
import random

items = ["red", "blue", "green", "orange"]
prices = {"red": 10, "blue": 5, "green": 7, "orange": 12}
listing = []

def getList():
    desires = []
    desire_index = []
    while len(desires) < 2:
        item = random.randint(0, len(items)-1)
        if item not in desire_index:
            desire_index.append(item)
            desires.append(items[item])
    return desires

class Buyer(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.wealth = int(random.normalvariate(20, 5))
        self.desires = getList()
        self.inventory = []


    def step(self):
        print(f"Buyer id: {self.unique_id}, Buyer List: {self.desires}, Buyer Wealth: {self.wealth}")
        '''Search listings for items that are in buyer's list'''
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
            print(f"Lowest price: {currentLow}, Seller:{sellerID}")




class Seller(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.inventory = getList()
        self.prices = []
        '''Assigns Sellers with varied prices, can be improved '''
        for x in range(len(self.inventory)):
            temp = prices[self.inventory[x]]
            temp = int(random.normalvariate(temp, 2))
            self.prices.append(temp)
        listing.append([self.inventory, self.prices, self.unique_id])

    def step(self):
        print(f"Seller id: {self.unique_id}, Seller Inventory: {self.inventory} {self.prices}")


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
        #IDs = [agent.inventory for agent in self.schedule.agents]
        print(listing)


Test = Market()
while True:
    input("Continue?")
    Test.step()