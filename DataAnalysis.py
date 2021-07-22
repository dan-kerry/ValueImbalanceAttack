import pickle
import matplotlib.pyplot as plt
import pandas

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
    print(data)

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



def main():
    data = importData("DataOutputs/BuyerActivity3")
    #BuyerWealthAnalysis(data)
    #NoOfPurchases(data)
    #TrustScoreAnalysis(data)
    #DataVomit(data)
    #FeedbackVsSpeed(data)
    RiskVsNegativeInteractions(data)
    #SalesVsRating(data)


main()
