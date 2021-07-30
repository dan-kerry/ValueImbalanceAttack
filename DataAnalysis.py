import pickle
import matplotlib.pyplot as plt
import pandas


class orderSheet:
    def __str__(self):
        return f"BuyerID: {self.BuyerID}, SellerID: {self.SellerID}, Price: {self.price}, Item: {self.item}, Due: {self.ExpectedArrivalDate}, Sale: {self.SaleDate}, Actual: {self.ActualArrivalDate}"


def importData(filename):
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    return new_dict

def BuyerWealthAnalysis(data):
    graph_data = []
    for x in range(len(data[0])):
        total = data[0][x].sum().sum()
        graph_data.append(total)
    fig = plt.figure()
    ax = plt.axes()
    plt.xlabel('Epoch')
    plt.ylabel('Wealth')
    plt.plot(graph_data)
    plt.show()

def NoOfPurchases(data):
    #Returns a histogram displaying number of purchases made by buyers, ideally normally distributed
    graph_data = data[0][-1]['purchases']
    ax = graph_data.hist(bins = 8)
    plt.show()

def TrustScoreAnalysis(data):
    graph_data = data[1][-1]['feedback']
    ax = graph_data.hist(bins=30)
    plt.show()

def DataVomit(data):
    for i in range(len(data)):
        print(f"Sale: {i} - {data[i]}")

def FeedbackVsSpeed(data):
    graph_data = data[1][-1]
    graph_data.plot.scatter(x="speed", y="feedback")
    plt.show()

def RiskVsNegativeInteractions(data):
    graph_data = data[0][-1]
    '''for x in range(len(graph_data)):
        print(graph_data.loc[x])'''
    graph_data['ScamRate'] = (graph_data['negInteractions'] + 1) / ((graph_data['negInteractions'] + graph_data['posInteractions']) + 2)
    graph_data.plot.scatter(x="riskAversion", y="ScamRate")
    #plt.hexbin(graph_data["riskAversion"], graph_data["negInteractions"])
    plt.show()
    #print(graph_data)

def SalesVsRating(data):
    graph_data = data[1][-1]
    graph_data.plot.scatter(x="feedback", y="ordersRec")
    plt.show()

def ValueImbalanceAnalysis(data):
    wealth = []
    rep = []
    for x in range(len(data[2])):
        rep.append(data[2][x][0])
        wealth.append(data[2][x][1])
    print((wealth))
    fig, ax = plt.subplots()
    ax.plot(rep, color="red")
    ax.plot([[0.9]*len(rep)], color="black")
    ax.hlines(y=0.7, xmin=0, xmax=len(rep), linewidth=1, color='black')
    ax2 = ax.twinx()
    ax2.plot(wealth, color="blue")
    ax.set_xlabel("Epoch", fontsize=10)
    ax.set_ylabel("Attacker Reputation", color="red", fontsize=10)
    ax2.set_ylabel("Attacker Wealth", color="blue", fontsize=10)
    plt.show()

def newDataTest(data):
    wealth = []
    rep = []
    for x in range(len(data)):
        rep.append(data[x][0])
        wealth.append(data[x][1])
    fig, ax = plt.subplots()
    ax.plot(rep, color="red")
    ax.hlines(y=0.8, xmin=0, xmax=len(rep), linewidth=1, color='black')
    ax2 = ax.twinx()
    ax2.plot(wealth, color="blue")
    ax.set_xlabel("Epoch", fontsize=10)
    ax.set_ylabel("Attacker Reputation", color="red", fontsize=10)
    ax2.set_ylabel("Attacker Wealth", color="blue", fontsize=10)
    plt.show()

def DictionaryComprehension(data):
    pass

def batch_analysis(data):
    output_list = []
    output_list2 = []
    for y in range(len(data[0])):
        totalRep = 0
        totalWealth = 0
        for x in range(len(data)):
            totalRep += data[x][y][0]
            totalWealth += data[x][y][1]
        totalRep /= len(data)
        totalWealth /= len(data)

        output_list.append(totalRep)
        output_list2.append(totalWealth)
    fig, ax = plt.subplots()
    ax.plot(output_list, color="red")
    ax2 = ax.twinx()
    ax2.plot(output_list2, color="blue")
    ax.set_ylabel("Attacker Reputation", color="red", fontsize=10)
    ax2.set_ylabel("Attacker Wealth", color="blue", fontsize=10)
    ax.set_xlabel("Epoch", fontsize=10)
    plt.show()

def dataTest(data):
    print(len(data[3]))

def averageFinalValue(data):
    total = 0
    for x in range(len(data)):
        total += data[x][-1][1]
    return total / len(data)

def optimal():
    o5 = averageFinalValue(importData("Results/Simple_05_HighValue"))
    o7 = averageFinalValue(importData("Results/Simple_07_HighValue"))
    o75 = averageFinalValue(importData("Results/Simple_075_HighValue"))
    o8 = averageFinalValue(importData("Results/Simple_08_HighValue"))
    o825 = averageFinalValue(importData("Results/Simple_0825_HighValue"))
    o85 = averageFinalValue(importData("Results/Simple_085_HighValue"))
    o9 = averageFinalValue(importData("Results/Simple_09_HighValue"))
    o95 = averageFinalValue(importData("Results/Simple_095_HighValue"))
    o99 = averageFinalValue(importData("Results/Simple_099_HighValue"))

    y_axis = [o5, o7, o75, o8, o825, o85, o9, o95, o99]
    x_axis = [0.5, 0.7, 0.75, 0.8, 0.825, 0.85, 0.9, 0.95, 0.99]
    plt.plot(x_axis, y_axis)
    plt.show()

def main():
    data = importData("Results/Simple_0825_HighValue")
    #BuyerWealthAnalysis(data)
    #NoOfPurchases(data)
    #TrustScoreAnalysis(data)
    #DataVomit(data)
    #FeedbackVsSpeed(data)
    #RiskVsNegativeInteractions(data) #BuyerActivity3
    #SalesVsRating(data)
    #ValueImbalanceAnalysis(data) #AttackDataTest
    #newDataTest(data)
    #batch_analysis(data)
    #dataTest(data)
    optimal()


main()
