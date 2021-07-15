import pickle
import matplotlib.pyplot as plt

def importData(filename):
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    return new_dict

def BuyerWealthAnalysis(data):
    graph_data = []
    for x in range(len(data)):
        total = data[x].sum().sum()
        graph_data.append(total)
    fig = plt.figure()
    ax = plt.axes()
    plt.plot(graph_data)
    plt.show()


def main():
    data = importData("TestOutput")
    BuyerWealthAnalysis(data)
main()
