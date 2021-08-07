import pickle
import matplotlib.pyplot as plt
import pandas
import statistics as stat


class orderSheet:
    def __str__(self):
        return f"BuyerID: {self.BuyerID}, SellerID: {self.SellerID}, Price: {self.price}, Item: {self.item}, Due: {self.ExpectedArrivalDate}, Sale: {self.SaleDate}, Actual: {self.ActualArrivalDate}"

def quartiles(data):
    data.sort()
    half_list = int(len(data) // 2)
    upper_quartile = stat.median(data[-half_list])
    lower_quartile = stat.median(data[:half_list])
    return [upper_quartile, lower_quartile]


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

def SingleRunAnalysis(data):
    wealth = []
    rep = []
    for x in range(len(data)):
        rep.append(data[x][0])
        wealth.append(data[x][1])
    fig, ax = plt.subplots()
    ax.plot(rep, color="red")
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

def ErrorTest2(data):
    output_list = []
    for y in range(len(data[0])):
        totalWealth = 0
        for x in range(len(data)):
            totalWealth += data[x][y][1]
        totalWealth /= len(data)
        output_list.append(totalWealth)


    for j in range(len(data)):
        newLine = []
        for k in range(len(data[j])):
            newLine.append(data[j][k][1])
        plt.plot(newLine, alpha=0.1, color='black')
    plt.plot(output_list, color='red')
    plt.show()

def dataTest(data):
    print(len(data[3]))

def averageFinalValue(data):
    total = 0
    for x in range(len(data)):
        total += data[x][-1][1]
    return total / len(data)

def optimal():
    o4 = averageFinalValue(importData("Results/Simple_04_HighValue"))
    o5 = averageFinalValue(importData("Results/Simple_05_HighValue"))
    o7 = averageFinalValue(importData("Results/Simple_07_HighValue"))
    o75 = averageFinalValue(importData("Results/Simple_075_HighValue"))
    o8 = averageFinalValue(importData("Results/Simple_08_HighValue"))
    o825 = averageFinalValue(importData("Results/Simple_0825_HighValue"))
    o85 = averageFinalValue(importData("Results/Simple_085_HighValue"))
    o9 = averageFinalValue(importData("Results/Simple_09_HighValue"))
    o95 = averageFinalValue(importData("Results/Simple_095_HighValue"))
    o99 = averageFinalValue(importData("Results/Simple_099_HighValue"))

    y_axis = [o4, o5, o7, o75, o8, o825, o85, o9, o95, o99]
    #x_axis = [0.4, 0.5, 0.7, 0.75, 0.8, 0.825, 0.85, 0.9, 0.95, 0.99]
    x_axis = [0.4, 0.5, 0.6, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]
    plt.plot(x_axis, y_axis)
    plt.show()

def StaticThreshold():
    data1 = importData("ThresholdAnalysis/ConstantThresholdAnalysis/BaseTRS_LowerRA")
    data2 = importData("ThresholdAnalysis/ConstantThresholdAnalysis/BaseTRS_HigherRA")
    data3 = importData("ThresholdAnalysis/ConstantThresholdAnalysis/AdvancedTRS_HigherRA")
    data4 = importData("ThresholdAnalysis/ConstantThresholdAnalysis/AdvancedTRS_LowerRA")

    x_axis1 = []
    y_axis1 = []
    for x in range(len(data1)):
        x_axis1.append(data1[x][0])
        y_axis1.append(data1[x][1])
    plt.plot(x_axis1, y_axis1, label='Lower Risk Aversion')

    x_axis2 = []
    y_axis2 = []
    for x in range(len(data2)):
        x_axis2.append(data2[x][0])
        y_axis2.append(data2[x][1])
    plt.plot(x_axis2, y_axis2, label='Higher Risk Aversion')

    x_axis3 = []
    y_axis3 = []
    for x in range(len(data3)):
        x_axis3.append(data3[x][0])
        y_axis3.append(data3[x][1])
    plt.plot(x_axis3, y_axis3, label='Higher RA w/ Value-Based TRS')

    x_axis4 = []
    y_axis4 = []
    for x in range(len(data4)):
        x_axis4.append(data4[x][0])
        y_axis4.append(data4[x][1])
    plt.plot(x_axis4, y_axis4, label='Lower RA w/ Value-Based TRS')
    plt.ylabel("Profit", fontsize=10)
    plt.xlabel("Attack Threshold", fontsize=10)
    plt.title('Analysis of Attack Threshold variation')

    plt.legend()
    plt.show()

def errorTest():
    data1 = importData("ValueDifferentiation/LowValueAttack_ValueBased")

    output_list = []
    UpperQuart = []
    LowerQuart = []

    for y in range(len(data1[0])):
        totalWealth = 0
        quart = []
        for x in range(len(data1)):
            totalWealth += data1[x][y][1]
            quart.append(data1[x][y][1])
        newQuart = sorted(quart)
        half = int(len(newQuart) // 2)
        UpperQuart.append(newQuart[half + (half // 2)])
        LowerQuart.append(newQuart[half - (half // 2)])
        totalWealth /= len(data1)
        output_list.append(totalWealth)

    plt.plot(output_list, label='Lower Risk Aversion')
    plt.plot(UpperQuart)
    plt.plot(LowerQuart)

    plt.ylabel("Profit", fontsize=10)
    plt.xlabel("Attack Threshold", fontsize=10)
    plt.title('Analysis of Attack Threshold variation')

    plt.legend()
    plt.show()



def ValueDiff():
    data1 = importData("ValueDifferentiation/LowValueAttack_ValueBased")
    data2 = importData("ValueDifferentiation/MidValueAttack_ValueBased")
    data3 = importData("ValueDifferentiation/HighValueAttack_ValueBased")

    output_list = []
    for y in range(len(data1[0])):
        totalWealth = 0
        for x in range(len(data1)):
            totalWealth += data1[x][y][1]
        totalWealth /= len(data1)
        output_list.append(totalWealth)

    output_list2 = []
    for y in range(len(data2[0])):
        totalWealth = 0
        for x in range(len(data2)):
            totalWealth += data2[x][y][1]
        totalWealth /= len(data2)
        output_list2.append(totalWealth)

    output_list3 = []
    for y in range(len(data3[0])):
        totalWealth = 0
        for x in range(len(data3)):
            totalWealth += data3[x][y][1]
        totalWealth /= len(data3)
        output_list3.append(totalWealth)

    fig, ax = plt.subplots()
    ax.plot(output_list, color="red", label='Low Value Attack')
    ax.plot(output_list2, color="blue", label='Medium Value Attack')
    ax.plot(output_list3, color="black", label='High Value Attack')
    plt.ylabel("Profit", fontsize=10)
    plt.xlabel("Epoch", fontsize=10)
    plt.title('Analysis of Profit with a Value-Based TRS')
    plt.legend()
    plt.show()

def ValueDiffSimple():
    data1 = importData("ValueDifferentiation/LowValueAttack_Regular")
    data2 = importData("ValueDifferentiation/MidValueAttack_Regular")
    data3 = importData("ValueDifferentiation/HighValueAttack_Regular")

    output_list = []
    for y in range(len(data1[0])):
        totalWealth = 0
        for x in range(len(data1)):
            totalWealth += data1[x][y][1]
        totalWealth /= len(data1)
        output_list.append(totalWealth)

    output_list2 = []
    for y in range(len(data2[0])):
        totalWealth = 0
        for x in range(len(data2)):
            totalWealth += data2[x][y][1]
        totalWealth /= len(data2)
        output_list2.append(totalWealth)

    output_list3 = []
    for y in range(len(data3[0])):
        totalWealth = 0
        for x in range(len(data3)):
            totalWealth += data3[x][y][1]
        totalWealth /= len(data3)
        output_list3.append(totalWealth)

    fig, ax = plt.subplots()
    ax.plot(output_list, color="red", label='Low Value Attack')
    ax.plot(output_list2, color="blue", label='Medium Value Attack')
    ax.plot(output_list3, color="black", label='High Value Attack')
    plt.ylabel("Profit", fontsize=10)
    plt.xlabel("Epoch", fontsize=10)
    plt.title('Analysis of Profit with a Simple TRS')
    plt.legend()
    plt.show()

def VariableValueAnalysis():
    data1 = importData("ThresholdAnalysis/VariableThresholdAnalysis/Constant085_Value")
    data2 = importData("ThresholdAnalysis/VariableThresholdAnalysis/Variable_Value_300_0_85")
    data3 = importData("ThresholdAnalysis/VariableThresholdAnalysis/Variable_Value_300_085_500_075")
    data4 = importData("ThresholdAnalysis/VariableThresholdAnalysis/Variable_Value_SemiRandom")
    data5 = importData("ThresholdAnalysis/VariableThresholdAnalysis/Variable_Value_098_200_085")


    output_list = []
    for y in range(len(data1[0])):
        totalWealth = 0
        for x in range(len(data1)):
            totalWealth += data1[x][y][1]
        totalWealth /= len(data1)
        output_list.append(totalWealth)

    output_list2 = []
    for y in range(len(data2[0])):
        totalWealth = 0
        for x in range(len(data2)):
            totalWealth += data2[x][y][1]
        totalWealth /= len(data2)
        output_list2.append(totalWealth)

    output_list3 = []
    for y in range(len(data3[0])):
        totalWealth = 0
        for x in range(len(data3)):
            totalWealth += data3[x][y][1]
        totalWealth /= len(data3)
        output_list3.append(totalWealth)

    output_list4 = []
    for y in range(len(data4[0])):
        totalWealth = 0
        for x in range(len(data4)):
            totalWealth += data4[x][y][1]
        totalWealth /= len(data4)
        output_list4.append(totalWealth)

    output_list5 = []
    for y in range(len(data5[0])):
        totalWealth = 0
        for x in range(len(data5)):
            totalWealth += data5[x][y][1]
        totalWealth /= len(data5)
        output_list5.append(totalWealth)

    fig, ax = plt.subplots()
    ax.plot(output_list, color="red", label='Constant Threshold')
    ax.plot(output_list2, color="blue", label='0.95 Initial, Dropping to 0.85')
    ax.plot(output_list3, color="black", label='0.95 Initial, 0.85, 0.75')
    ax.plot(output_list4, color="green", label='Semi-Random')
    ax.plot(output_list5, color="yellow", label='0.98, dropping to 0.85')
    plt.ylabel("Profit", fontsize=10)
    plt.xlabel("Epoch", fontsize=10)
    plt.title('Analysis of Profit when using Variable Threshold')
    plt.legend()
    plt.show()

def main():
    data = importData("ThresholdAnalysis/VariableThresholdAnalysis/Variable_Value_SemiRandom")
    #BuyerWealthAnalysis(data)
    #NoOfPurchases(data)
    #TrustScoreAnalysis(data)
    #DataVomit(data)
    #FeedbackVsSpeed(data)
    #RiskVsNegativeInteractions(data) #BuyerActivity3
    #SalesVsRating(data)
    #ValueImbalanceAnalysis(data) #AttackDataTest
    #SingleRunAnalysis(data)
    #batch_analysis(data)
    #dataTest(data)
    #optimal()
    #StaticThreshold()
    #ValueDiffSimple()
    #VariableValueAnalysis()
    #errorTest()
    ErrorTest2(data)



main()
