import random as r
from ex1 import *
import numpy
import time as t
import matplotlib.pyplot as plt


def drawNumber(a, b):
    x = r.randint(a, b)
    x = str(x)
    if len(x) == 1:
        x = '0' + x
    return x


def test(dijkstraGraph, aStarGraph, iterations):
    dij = [[], [], [], []]
    atm = [[], [], [], []]
    ate = [[], [], [], []]
    apm = [[], [], [], []]
    ape = [[], [], [], []]
    amm = [[], [], [], []]
    ame = [[], [], [], []]

    for x in range(iterations):
        # print(x, " start")
        result = "Brak"
        while result == "Brak":
            start = r.choice(list(aStarGraph.keys()))
            while True:
                end = r.choice(list(aStarGraph.keys()))
                if end != start:
                    break
            time = f"{drawNumber(0,23)}:{drawNumber(0,59)}:00"
            # print("start: ", start)
            # print("end: ", end)
            # print("time: ", time)

            startT = t.time()
            result, a, b, c = dijkstra(start, end, time, dijkstraGraph)
            endT = t.time()
            d = endT-startT
            if result != "Brak":
                dij[0].append(a)
                dij[1].append(b)
                dij[2].append(c)
                dij[3].append(d)

                startT = t.time()
                _, a, b, c = aStar(start, end, 't', time, aStarGraph, "man")
                endT = t.time()
                d = endT - startT
                atm[0].append(a)
                atm[1].append(b)
                atm[2].append(c)
                atm[3].append(d)

                startT = t.time()
                _, a, b, c = aStar(start, end, 't', time, aStarGraph, "euc")
                endT = t.time()
                d = endT - startT
                ate[0].append(a)
                ate[1].append(b)
                ate[2].append(c)
                ate[3].append(d)

                startT = t.time()
                _, a, b, c = aStar(start, end, 'p', time, aStarGraph, "man")
                endT = t.time()
                d = endT - startT
                apm[0].append(a)
                apm[1].append(b)
                apm[2].append(c)
                apm[3].append(d)

                startT = t.time()
                _, a, b, c = aStar(start, end, 'p', time, aStarGraph, "euc")
                endT = t.time()
                d = endT - startT
                ape[0].append(a)
                ape[1].append(b)
                ape[2].append(c)
                ape[3].append(d)

                startT = t.time()
                _, a, b, c = aStarMod(start, end, time, aStarGraph, "man")
                endT = t.time()
                d = endT - startT
                amm[0].append(a)
                amm[1].append(b)
                amm[2].append(c)
                amm[3].append(d)

                startT = t.time()
                _, a, b, c = aStarMod(start, end, time, aStarGraph, "euc")
                endT = t.time()
                d = endT - startT
                ame[0].append(a)
                ame[1].append(b)
                ame[2].append(c)
                ame[3].append(d)

    avgTravelTime = [numpy.mean(dij[0]), numpy.mean(atm[0]), numpy.mean(ate[0]), numpy.mean(apm[0]), numpy.mean(ape[0]), numpy.mean(amm[0]), numpy.mean(ame[0])]
    avgChangesNumber = [numpy.mean(dij[1]), numpy.mean(atm[1]), numpy.mean(ate[1]), numpy.mean(apm[1]), numpy.mean(ape[1]), numpy.mean(amm[1]), numpy.mean(ame[1])]
    avgProcessedStops = [numpy.mean(dij[2]), numpy.mean(atm[2]), numpy.mean(ate[2]), numpy.mean(apm[2]), numpy.mean(ape[2]), numpy.mean(amm[2]), numpy.mean(ame[2])]
    avgCountingTime = [numpy.mean(dij[3]), numpy.mean(atm[3]), numpy.mean(ate[3]), numpy.mean(apm[3]), numpy.mean(ape[3]), numpy.mean(amm[3]), numpy.mean(ame[3])]

    for i in range(len(avgTravelTime)):
        avgTravelTime[i] = round(avgTravelTime[i], 0)

    for i in range(len(avgChangesNumber)):
        avgChangesNumber[i] = round(avgChangesNumber[i], 0)

    for i in range(len(avgProcessedStops)):
        avgProcessedStops[i] = round(avgProcessedStops[i], 0)

    for i in range(len(avgCountingTime)):
        avgCountingTime[i] = round(avgCountingTime[i], 2)

    print(avgTravelTime)
    print(avgChangesNumber)
    print(avgProcessedStops)
    print(avgCountingTime)

    labels = ["dij", "atm", "ate", "apm", 'ape', "amm", 'ame']

    fig1, ax = plt.subplots()
    plt.bar(labels, avgTravelTime)
    plt.title("Średni czas podróży względem użytego algorytmu")
    plt.xlabel("Algorytm")
    plt.ylabel("Średni czas podróży w minutach")
    for i, v in enumerate(avgTravelTime):
        ax.text(i, v + 0.1, str(v), ha='center')

    fig2, ax = plt.subplots()
    plt.bar(labels, avgChangesNumber)
    plt.title("Średna liczba przesiadek względem użytego algorytmu")
    plt.xlabel("Algorytm")
    plt.ylabel("Średna liczba przesiadek")
    for i, v in enumerate(avgChangesNumber):
        ax.text(i, v + 0.1, str(v), ha='center')

    fig3, ax = plt.subplots()
    plt.bar(labels, avgProcessedStops)
    plt.title("Średnia liczba przetworzonych węzłów względem użytego algorytmu")
    plt.xlabel("Algorytm")
    plt.ylabel("Średnia liczba przetworzonych węzłów")
    for i, v in enumerate(avgProcessedStops):
        ax.text(i, v + 0.1, str(v), ha='center')

    fig4, ax = plt.subplots()
    plt.bar(labels, avgCountingTime)
    plt.title("Średni czas obliczeń względem użytego algorytmu")
    plt.xlabel("Algorytm")
    plt.ylabel("Średni czas obliczeń w sekundach")
    for i, v in enumerate(avgCountingTime):
        ax.text(i, v + 0.1, str(v), ha='center')

    plt.show()
