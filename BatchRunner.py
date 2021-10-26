import main

testValues = [0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94,
              0.95, 0.96, 0.97, 0.98,  0.99]
testItems = ["blue", "green", "sapphire", "turqoise", "yellow", "mauve", "lilac", "violet", "zomp"]
#testTriggers = [125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475]
testTriggers = [250, 500, 750, 1000, 1250, 1500, 1750]
testValues2 = [0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.72, 0.75, 0.77,0.78,0.79, 0.8, 0.81, 0.82, 0.83, 0.84,
               0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.995, 0.999]
endPoints = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#endPoints = [0.4, 0.42, 0.45, 0.47, 0.5, 0.52, 0.55, 0.57, 0.6, 0.62, 0.65, 0.67, 0.7, 0.75, 0.8, 0.85, 0.87, 0.9, 0.91]

dataOutput = []
'''for i in range(len(endPoints)):
    overall = []
    for turn in range(150):
        print(f"{i} {turn}")
        result = endPoints[i]
        overall.append(main.run(result))
        main.listing = []
        main.Sim.reset()
        main.Attack.reset()
    dataOutput.append(overall)
main.exportData(dataOutput, "Final/R3/Simple_Endpoint2")'''

for turn in range(150):
    print(f"{turn}")
    dataOutput.append(main.run())
    main.listing = []
    main.Sim.reset()
    main.Attack.reset()
main.exportData(dataOutput, "Final/Discussion/Agents150_150")

'''for i in range(len(testTriggers)):
    overall = []
    for turn in range(100):
        print(f"{i} {turn}")
        result = testTriggers[i]
        overall.append(main.run(result))
        main.listing = []
        main.Sim.reset()
        main.Attack.reset()
    dataOutput.append(overall)
main.exportData(dataOutput, "Periodic/Simple_1")'''

