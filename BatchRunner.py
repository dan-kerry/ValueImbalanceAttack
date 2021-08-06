import main

testValues = [0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]
dataOutput = []

for i in range(len(testValues)):
    overall = []

    for turn in range(250):
        main.Sim.reset()
        main.Attack.reset()
        print(f"{i} {turn}")
        overall.append(main.run(testValues[i]))
        main.listing = []
    total = 0
    for x in range(len(overall)):
        total += overall[x][-1][1]
    turnResult = total / len(overall)
    dataOutput.append([testValues[i], turnResult])
main.exportData(dataOutput, "AdvancedTRS_LowerRA")


'''for turn in range(100):
    main.Sim.reset()
    main.Attack.reset()
    print(f"{turn}")
    dataOutput.append(main.run())
    main.listing = []
main.exportData(dataOutput, "ThresholdAnalysis/VariableThresholdAnalysis/Variable_Value_098_200_085")'''