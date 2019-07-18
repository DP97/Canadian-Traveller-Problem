from tkinter import *

# graficke rozhranie
root = Tk()
root.title("CTP calc")
root.geometry("400x400+0+0")

heading = Label(
    root, text="Porovnanie efektivity stratégií", font=("arial", 20, "bold"), fg="black"
).pack()

label1 = Label(root, text="Zvolte počet uzlov: ", font=("arial", 15), fg="black").place(
    x=10, y=162
)
label2 = Label(
    root, text="Zvolte % blok. hrán: ", font=("arial", 15), fg="black"
).place(x=10, y=202)
label3 = Label(
    root, text="Zvolte počet iterácií: ", font=("arial", 15), fg="black"
).place(x=10, y=242)

node = IntVar()
block = IntVar()
it = IntVar()
entry_box1 = Entry(root, textvariable=node, width=20, bg="white").place(x=250, y=170)
entry_box2 = Entry(root, textvariable=block, width=20, bg="white").place(x=250, y=210)
entry_box3 = Entry(root, textvariable=it, width=20, bg="white").place(x=250, y=250)

# funkcia ktora spusti test
def start():

    controll = True
    while controll:

        try:
            controll = False
            from graph import graphGen
            from dijkstra import dijkstra
            from greedy import greedyStrategy
            from reposition import repositionStrategy
            from comparison import comparisonStrategy
            from waiting import waitingStrategy
            from recoverygreedy import recoverygreedyStrategy
            import xlsxwriter
            from statistics import median
            import matplotlib as mpl
            import matplotlib.pyplot as plt
            import numpy as np
            import tkinter

            timelist1 = []
            timelist2 = []
            timelist3 = []
            timelist4 = []
            timelist5 = []

            costlist1 = []
            costlist2 = []
            costlist3 = []
            costlist4 = []
            costlist5 = []

            graphGen = graphGen()
            original_graph = graphGen.create(int(node.get()))

            t = dijkstra(original_graph)
            dijk = t.shortest_path(0, (int(node.get()) - 1))
            dijkpath = t.get_path_length(dijk)

            for i in range(int(it.get())):
                # generovanie blok.hran
                blocked_graph = graphGen.generate_blockades(int(block.get()))
                graphGen.save_fig(blocked_graph)

                greedy = greedyStrategy(blocked_graph)
                t1, cost1, route1 = greedy.search(0, (int(node.get()) - 1))
                timelist1.append(t1)
                costlist1.append(cost1)

                reposition = repositionStrategy(blocked_graph)
                t2, cost2, route2 = reposition.search(0, (int(node.get()) - 1))
                timelist2.append(t2)
                costlist2.append(cost2)

                comparison = comparisonStrategy(blocked_graph)
                t3, cost3, route3 = comparison.search(0, (int(node.get()) - 1))
                timelist3.append(t3)
                costlist3.append(cost3)

                waiting = waitingStrategy(blocked_graph)
                t4, cost4, route4 = waiting.search(0, (int(node.get()) - 1))
                timelist4.append(t4)
                costlist4.append(cost4)

                recoverygreedy = recoverygreedyStrategy(blocked_graph)
                t5, cost5, route5 = recoverygreedy.search(0, (int(node.get()) - 1))
                timelist5.append(t5)
                costlist5.append(cost5)

            controll_time = [timelist1, timelist2, timelist3, timelist4, timelist5]

            for i in controll_time:
                if len(i) == 0:
                    i.append(0)

            avgtimes = []

            for times in controll_time:
                avgtimes.append(sum(times) / len(times))

            controll_cost = [costlist1, costlist2, costlist3, costlist4, costlist5]

            for i in controll_cost:
                if len(i) == 0:
                    i.append(0)

            avgcosts = []

            for costs in controll_cost:
                avgcosts.append(sum(costs) / len(costs))

            workbook = xlsxwriter.Workbook("results.xlsx")
            worksheet = workbook.add_worksheet()

            worksheet.set_column("A:A", 20)
            worksheet.set_column("B:B", 15)
            worksheet.set_column("C:C", 15)
            worksheet.set_column("D:D", 15)
            worksheet.set_column("E:E", 15)
            worksheet.set_column("F:F", 15)

            bold = workbook.add_format({"bold": True})

            worksheet.write("A1", "              Strategy", bold)
            worksheet.write("A2", "Greedy")
            worksheet.write("A3", "Reposition")
            worksheet.write("A4", "Comparison")
            worksheet.write("A5", "Waiting")
            worksheet.write("A6", "Recovery Greedy")
            worksheet.write("A7", "Dijkstra algorithm")

            worksheet.write("B1", "    Average Cost", bold)
            worksheet.write("B2", avgcosts[0])
            worksheet.write("B3", avgcosts[1])
            worksheet.write("B4", avgcosts[2])
            worksheet.write("B5", avgcosts[3])
            worksheet.write("B6", avgcosts[4])
            worksheet.write("B7", dijkpath)

            worksheet.write("C1", "  Maximum Cost", bold)
            worksheet.write("C2", max(costlist1))
            worksheet.write("C3", max(costlist2))
            worksheet.write("C4", max(costlist3))
            worksheet.write("C5", max(costlist4))
            worksheet.write("C6", max(costlist5))

            worksheet.write("D1", "  Minimum Cost", bold)
            worksheet.write("D2", min(costlist1))
            worksheet.write("D3", min(costlist2))
            worksheet.write("D4", min(costlist3))
            worksheet.write("D5", min(costlist4))
            worksheet.write("D6", min(costlist5))

            worksheet.write("E1", "          Median", bold)
            worksheet.write("E2", median(costlist1))
            worksheet.write("E3", median(costlist2))
            worksheet.write("E4", median(costlist3))
            worksheet.write("E5", median(costlist4))
            worksheet.write("E6", median(costlist5))

            worksheet.write("F1", "   Average Time", bold)
            worksheet.write("F2", avgtimes[0])
            worksheet.write("F3", avgtimes[1])
            worksheet.write("F4", avgtimes[2])
            worksheet.write("F5", avgtimes[3])
            worksheet.write("F6", avgtimes[4])

            workbook.close()

            fig = plt.figure(figsize=(10, 8))

            data = [costlist1, costlist2, costlist3, costlist4, costlist5]

            fig, ax = plt.subplots()
            ax.set_title("Porovnanie efektivity stratégií")
            ax.boxplot(data)

            bottom, top = plt.ylim()
            plt.ylim(bottom=(median(costlist1) - 20))
            plt.ylim(top=(median(costlist1) + 40))

            fig.savefig("graph.png")
            tkinter.messagebox.showinfo("Oznam", "Výpočet bol úspešne dokončený.")

        except KeyError:
            controll = True


work = Button(
    root, text="Spustiť", width=20, height=3, bg="lightblue", command=start
).place(x=120, y=300)


root.mainloop()
