from mesa import Agent, Model
from mesa.time import RandomActivation
import random

items = ["red", "blue", "green", "orange"]
prices = {"red": 10, "blue": 5, "green": 7, "orange": 12}

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

    def

    def step(self):
        #print(f"Buyer id: {self.unique_id}, Buyer List: {self.desires}, Buyer Wealth: {self.wealth}")



class Seller(Agent):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.inventory = getList()
        self.prices = [prices[self.inventory[0]], prices[self.inventory[1]] ]

    def step(self):
        #print(f"Seller id: {self.unique_id}, Seller Inventory: {self.inventory} {self.prices}")


class Market(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        for i in range(0, self.num_agents, 2):
            a = Buyer(i)
            self.schedule.add(a)
        for i in range(1, self.num_agents, 2):
            a = Seller(i)
            self.schedule.add(a)


    def step(self):
        self.schedule.step()



Test = Market(10)
while True:
    input("Continue?")
    Test.step()