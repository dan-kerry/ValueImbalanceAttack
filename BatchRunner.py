import main

overall = []
for turn in range(100):
    main.Sim.reset()
    main.Attack.reset()
    print(turn)
    overall.append(main.run())
    main.listing = []

main.exportData(overall, "DataOutputs/ValueImbalanceHigh7")
