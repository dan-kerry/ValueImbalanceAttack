import pickle
import matplotlib.pyplot as plt
import numpy as np

def stylize_axes(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


class orderSheet:
    def __str__(self):
        return f"BuyerID: {self.BuyerID}, SellerID: {self.SellerID}, Price: {self.price}, Item: {self.item}, Due: {self.ExpectedArrivalDate}, Sale: {self.SaleDate}, Actual: {self.ActualArrivalDate}"

def quartiles(data):
    data.sort()
    half_list = int(len(data) // 2)
    iqr = half_list // 2
    median = data[half_list]
    upper_quartile = data[half_list + iqr]
    lower_quartile = data[half_list - iqr]
    return [upper_quartile, median, lower_quartile]


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
    ax2.set_ylabel("Attacker Profit", color="blue", fontsize=10)
    stylize_axes(ax)
    plt.show()
    #fig.savefig("Figures/Figure11a.pdf", bbox_inches='tight')

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
    stylize_axes(ax)

    plt.show()
    #fig.savefig("Figures/Figure4a.pdf", bbox_inches='tight')
def ErrorTest2(data):
    print(len(data))
    output_list = []
    for y in range(len(data[0])):
        totalWealth = 0
        for x in range(len(data)):
            totalWealth += data[x][y][1]
        totalWealth /= len(data)
        output_list.append(totalWealth)

    fig, ax = plt.subplots()
    for j in range(len(data)):
        newLine = []
        for k in range(len(data[j])):
            newLine.append(data[j][k][1])
        plt.plot(newLine, alpha=0.1, color='black')
    plt.plot(output_list, color='red', label='7-turn Rolling Average')
    plt.xlabel('Epoch')
    plt.ylabel('Damage (Cost to Buyers)')
    stylize_axes(ax)
    plt.legend()
    plt.show()
    #fig.savefig("Figures/Figure10c.pdf", bbox_inches='tight')
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
    data1 = importData("Threshold/SimpleTRS_Zomp")
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
def highestValues(data):
    max_values = []
    for run in range(len(data)):
        highest = 0
        for turn in range(len(data[run])):
            if data[run][turn][1] > highest:
                highest = data[run][turn][1]
        max_values.append(highest)
    return max_values
def newStaticPointBatch():
    testValues = [0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94,
                    0.95, 0.96, 0.97, 0.98,  0.99]
    data1 = importData("Threshold/SimpleTRS_ZompII")
    data1_Value = []
    data1_Error = []
    for value in range(len(data1)):
        data1_Value.append(np.median(highestValues(data1[value])))
        data1_Error.append(quartiles(highestValues(data1[value])))

    data1_Value = []
    data1_upper = []
    data1_lower = []
    for x in range(len(data1_Error)):
        data1_Value.append(data1_Error[x][1])
        data1_lower.append(data1_Error[x][0])
        data1_upper.append(data1_Error[x][2])

    fig, (ax1) = plt.subplots(1, 1)
    #ax1.errorbar(testValues, data2_Value, yerr=data2_Error)
    ax1.fill_between(testValues, data1_upper, data1_lower, color='black', alpha=0.3)
    ax1.plot(testValues, data1_Value, marker='x', markeredgecolor='black')
    plt.show()
def ValueAnalysis(data):
    prices = [8, 12, 18, 20, 25, 32, 40, 50]
    #prices = [8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 25, 32, 40, 50]
    max_value = 50
    x_axis = []
    data_Value = []
    data_Errors = []
    upper = []
    lower = []
    for x in prices:
        x_axis.append(((x - 4) / 4) * 100)
    for value in range(1, len(data)):
        newData = sorted(highestValues(data[value]))
        data_Value.append(quartiles(highestValues(data[value]))[1])
        upper.append( quartiles(newData)[0] )
        lower.append( quartiles(newData)[2] )
    fig, (ax1) = plt.subplots()
    plt.xlim(0, 1200)
    '''for x in range(len(upper)):
        plt.vlines(x_axis[x], lower[x], upper[x])'''
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax1.fill_between(x_axis, lower, upper, color='black', alpha=0.3)
    ax1.plot(x_axis, data_Value, marker='x', markeredgecolor='black')
    plt.xlabel('Value of Attack Item (% of Honest Sale Item)')
    plt.ylabel('Damage (Cost to Buyers)')
    stylize_axes(ax1)
    plt.show()
    #fig.savefig("Figures/Figure9.pdf", bbox_inches='tight')
def ValueAnalysisScatter(data):
    prices = [8, 12, 18, 20, 25, 32, 40, 50]
    max_value = 50
    x_axis = []
    xx = [0, 8000]
    data_Value = []
    data_Errors = []
    upper = []
    lower = []
    for x in prices:
        x_axis.append((x / max_value) * 100)
    for value in range(1, len(data)):
        newData = sorted(highestValues(data[value]))
        data_Value.append(quartiles(highestValues(data[value]))[1])
        upper.append(quartiles(newData)[0])
        lower.append(quartiles(newData)[2])
    fig, (ax1) = plt.subplots(1, 1)
    x = prices
    y = data_Value
    plt.scatter(x, y, color='black', label='Original Data Points')
    plt.xlim([0, 110])
    plt.ylim([0, 9100])

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(xx, p(xx), "r--")

    black_data = importData("ValueAnalysis/Black2")
    blackData = quartiles(highestValues(black_data))[1]
    bd1 = quartiles(highestValues(black_data))[0]
    bd2 = quartiles(highestValues(black_data)[75:125])[2]
    plt.vlines(80, bd1, bd2, label='IQR of result set')
    plt.scatter(80, blackData, marker='+', label='New Data Point')

    plt.xlabel('Value of Attack Item (True Value)')
    plt.ylabel('Damage (Cost to Buyers)')
    stylize_axes(ax1)
    plt.legend()
    plt.show()
    fig.savefig("Figures/Figure8.pdf", bbox_inches='tight')
def DualValueAnalysis():
    OriginData = importData("ValueAnalysis/VB_ReRun")
    ProofData = importData("ValueAnalysis/VB_Proof_ReRun")
    data7 = importData("AdditionalDataPointsF9/7")

    prices = [5, 7, 12, 18, 20, 25, 32, 40, 50]
    max_value = 50
    x_axis = []
    data_Value = []
    proof_data = []
    increase = []

    for x in prices:
        x_axis.append((x / max_value) * 100)
    d1 = quartiles(sorted(highestValues(OriginData[0])))
    data_Value.append(d1[1])
    d7 = quartiles(sorted(highestValues(data7)))
    data_Value.append(d7[1])

    for value in range(2, len(OriginData)):
        data_Value.append(quartiles(highestValues(OriginData[value]))[1])
    for x in range(len(ProofData)):
        proof_data.append(quartiles(highestValues(ProofData[x]))[1])
    for y in range(len(data_Value)):
        temp = proof_data[y] - data_Value[y]
        increase.append((temp/data_Value[y]) * 100)
    fig, (ax1) = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x_axis, data_Value, color='black', label='500 Epochs')
    ax1.plot(x_axis, proof_data, color='black',linestyle='dashed', label='1000 Epochs')
    ax2.bar(x_axis, increase, alpha=0.7)
    ax1.set_xlabel('Value of Attack Item (% of Honest Sale Item)')
    ax1.set_ylabel('Damage (Cost to Buyers)', color='black')
    ax2.set_ylabel('Percentage Increase', color='blue')
    ax1.legend()
    plt.show()
    #fig.savefig("Figures/Figure13.pdf", bbox_inches='tight')
def DataParse(data, target):
    output = []
    for x in range(len(data)):
        flag = False
        for y in range(len(data[x])):

            if data[x][y][1] > target:
                flag = True
        if not flag:
            output.append(data[x])
    return output
def TRS():
    data = importData("Results1/SimpleTRS")
    data2 = importData("Results1/VB_TRS")
    output_list = []
    output_list2 = []
    for y in range(len(data[0])):
        totalWealth2 = 0
        totalWealth = 0
        for x in range(len(data)):
            totalWealth += data[x][y][1]
            totalWealth2 += data2[x][y][1]

        totalWealth /= len(data)
        totalWealth2 /= len(data2)


        output_list.append(totalWealth)
        output_list2.append(totalWealth2)

    fig, ax = plt.subplots()
    ax.plot(output_list, color="red", label='Simple TRS')
    ax.plot(output_list2, color="blue", label='Value-Based TRS')

    ax.set_ylabel("Attacker Profit", color="black", fontsize=10)
    ax.set_xlabel("Epoch", fontsize=10)
    plt.xlim([0, 750])
    plt.ylim([0, 7000])
    stylize_axes(ax)
    plt.legend()
    plt.show()
    #fig.savefig("Figures/Figure3.pdf", bbox_inches='tight')
def DataComprehension(data):
    count = 0
    for x in range(len(data)):
        if data[x][-1][1] > 400:
            count += 1
    print(count)
def ValueAnalysis_Additional(data):
    data7 = importData("AdditionalDataPointsF9/7")

    prices = [5, 7, 12, 18, 20, 25, 32, 40, 50]
    #prices = [8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 25, 32, 40, 50]
    max_value = 50
    x_axis = []
    data_Value = []
    upper = []
    lower = []
    for x in prices:
        x_axis.append(((x - 4) / 4) * 100)

    d1 = quartiles(sorted(highestValues(data[0])))
    data_Value.append(d1[1])
    upper.append(d1[0])
    lower.append(d1[2])

    d7 = quartiles(sorted(highestValues(data7)))
    data_Value.append(d7[1])
    upper.append(d7[0])
    lower.append(d7[2])

    for value in range(2, len(data)):
        newData = sorted(highestValues(data[value]))
        data_Value.append(quartiles(highestValues(data[value]))[1])
        upper.append(quartiles(newData)[0])
        lower.append(quartiles(newData)[2])
    fig, (ax1) = plt.subplots()
    plt.xlim(0, 1200)
    '''for x in range(len(upper)):
        plt.vlines(x_axis[x], lower[x], upper[x])'''
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax1.fill_between(x_axis, lower, upper, color='black', alpha=0.3)
    ax1.plot(x_axis, data_Value, marker='x', markeredgecolor='black')
    plt.xlabel('Value of Attack Item (% of Honest Sale Item)')
    plt.ylabel('Damage (Cost to Buyers)')
    stylize_axes(ax1)
    plt.show()
    #fig.savefig("Figures/Figure9.pdf", bbox_inches='tight')
def PeriodAnalysis(data):
    #prices = [125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475]
    prices = [250, 500, 750, 1000, 1250, 1500, 1750]
    max_value = 50
    x_axis = []
    data_Value = []
    data_Errors = []
    upper = []
    lower = []
    for x in range(len(prices)):
        x_axis.append(prices[x])

    for value in range(len(data)):
        data_Value.append(quartiles(highestValues(data[value]))[1])

    fig, (ax1) = plt.subplots()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax1.plot(x_axis, data_Value, marker='x', markeredgecolor='black')
    plt.xlabel('Value of Attack Item (% of Honest Sale Item)')
    plt.ylabel('Damage (Cost to Buyers)')
    stylize_axes(ax1)
    plt.show()
    #fig.savefig("Figures/Figure9.pdf", bbox_inches='tight')
def EndPointAnalysis():
    data = importData("Final/R3/Simple_Endpoint2")
    #endPoints = [0.4, 0.42, 0.45, 0.47, 0.5, 0.52, 0.55, 0.57, 0.6, 0.62, 0.65, 0.67, 0.7, 0.75, 0.8, 0.85, 0.87, 0.9, 0.91]
    endPoints = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    data1_Value = []
    data1_Error = []
    for value in range(len(data)):
        data1_Value.append(np.median(highestValues(data[value])))
        data1_Error.append(quartiles(highestValues(data[value])))
    data1_Value = []
    data1_upper = []
    data1_lower = []
    for x in range(len(data1_Error)):
        data1_Value.append(data1_Error[x][1])
        data1_lower.append(data1_Error[x][0])
        data1_upper.append(data1_Error[x][2])

    fig, (ax1) = plt.subplots(1, 1)
    # ax1.errorbar(testValues, data2_Value, yerr=data2_Error)
    ax1.fill_between(endPoints, data1_upper, data1_lower, color='black', alpha=0.3)
    ax1.plot(endPoints, data1_Value, marker='x', markeredgecolor='black')
    plt.show()
def RatioAnalysis():
    data = importData("Final/R3/VB_Ratio")
    endPoints = [0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.72, 0.75, 0.77,0.78,0.79, 0.8, 0.81, 0.82, 0.83, 0.84,
               0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.995, 0.999]
    data1_Value = []
    data1_Error = []
    for value in range(len(data)):
        data1_Value.append(np.median(highestValues(data[value])))
        data1_Error.append(quartiles(highestValues(data[value])))
    data1_Value = []
    data1_upper = []
    data1_lower = []
    for x in range(len(data1_Error)):
        data1_Value.append(data1_Error[x][1])
        data1_lower.append(data1_Error[x][0])
        data1_upper.append(data1_Error[x][2])

    fig, (ax1) = plt.subplots(1, 1)
    # ax1.errorbar(testValues, data2_Value, yerr=data2_Error)
    ax1.fill_between(endPoints, data1_upper, data1_lower, color='black', alpha=0.3)
    ax1.plot(endPoints, data1_Value, marker='x', markeredgecolor='black')
    plt.show()

def VolumeAnalysis():
    LineData = importData('Final/R2/Simple')
    VolumeData = importData('Final/R2/Simple_Volume')
    prices = [5, 7, 12, 18, 20, 25, 32, 40, 50]
    x_axis = []
    data_Value = []
    data_Errors = []
    upper = []
    lower = []
    volume = []
    for x in prices:
        x_axis.append(((x - 4) / 4) * 100)
    for value in range(len(LineData)):
        newData = sorted(highestValues(LineData[value]))
        data_Value.append(quartiles(highestValues(LineData[value]))[1])
        upper.append(quartiles(newData)[0])
        lower.append(quartiles(newData)[2])

    for y in range(len(VolumeData)):
        total = 0
        for j in range(len(VolumeData[y])):
            batchVol = VolumeData[y][j][-1][2]
            total += batchVol
        volume.append(total/len(VolumeData[y]))

    fig, (ax1) = plt.subplots()
    ax2 = ax1.twinx()
    plt.xlim(0, 1200)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ax1.fill_between(x_axis, lower, upper, color='black', alpha=0.3)
    ax1.plot(x_axis, data_Value, marker='x', markeredgecolor='black', alpha=0.3)
    ax2.bar(x_axis, volume, width=30)
    ax1.set_xlabel('Value of Attack Item (% of Honest Sale Item)')
    ax1.set_ylabel('Damage (Cost to Buyers)')
    ax2.set_ylabel('Average Total Dishonest Sales')
    stylize_axes(ax1)
    plt.show()
    #fig.savefig("Figures/Figure9.pdf", bbox_inches='tight')

def MultiRep():
    data1 = importData("Final/R3/VB_StartPoints")[1]
    data5 = importData("Final/R3/VB_StartPoints")[5]
    data6 = importData("Final/R3/VB_StartPoints")[6]

    output_list1 = []
    output_list5 = []
    output_list6 = []

    for y in range(len(data1[0])):
        totalRep1 = 0
        totalRep5 = 0
        totalRep6 = 0
        for x in range(len(data1)):
            totalRep1 += data1[x][y][1]
            totalRep5 += data5[x][y][1]
            totalRep6 += data6[x][y][1]

        totalRep1 /= len(data1)
        totalRep5 /= len(data5)
        totalRep6 /= len(data6)

        output_list1.append(totalRep1)
        output_list5.append(totalRep5)
        output_list6.append(totalRep6)

    fig, ax = plt.subplots()
    ax.plot(output_list1, color="red", label="0.5")
    ax.plot(output_list5, color="green", label="0.8")
    ax.plot(output_list6, color="blue", label="0.85")

    plt.legend()
    ax.set_xlabel("Epoch", fontsize=10)
    stylize_axes(ax)
    plt.show()
    #fig.savefig("Figures/Figure4a.pdf", bbox_inches='tight')
def main():
    data = importData("Final/R3/VB_EndPoint")[0]
    #BuyerWealthAnalysis(data)
    #NoOfPurchases(data)
    #TrustScoreAnalysis(data)
    #DataVomit(data)
    #FeedbackVsSpeed(data)
    #RiskVsNegativeInteractions(data) #BuyerActivity3
    #SalesVsRating(data)
    #ValueImbalanceAnalysis(data) #AttackDataTest
    #SingleRunAnalysis(data[-1][89])
    batch_analysis(data)
    #dataTest(data)
    #optimal()
    #StaticThreshold()
    #ValueDiffSimple()
    #VariableValueAnalysis()
    #errorTest()
    #ErrorTest2(DataParse(data, 1700))
    #newStaticPointBatch()
    #ValueAnalysis(data)
    #ValueAnalysisScatter(data)
    #DualValueAnalysis()
    #TRS()
    #DataComprehension(data[-4])
    #ValueAnalysis_Additional(data)
    #PeriodAnalysis(data)
    #EndPointAnalysis()
    #VolumeAnalysis()
    #RatioAnalysis()
    #MultiRep()


main()
