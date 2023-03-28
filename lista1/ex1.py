from queue import PriorityQueue
from graph import *


def recoverRoute(end):
    current = end
    route = []
    # while current.previous:
    #     route.append(str(current.previous))
    #     current = current.previous.departureStop
    #
    # result = ""
    # for x in route[::-1]:
    #     result += x + '\n'

    while current.previous:
        route.append(current.previous)
        current = current.previous.departureStop

    i = len(route)-1
    changeCount = 0
    result = f"{route[i].line} {route[i].departureStop.name} : {route[i].departureTime} -> "
    line = route[i].line
    i -= 1
    while i > 0:
        if route[i].line != line:
            changeCount += 1
            result += f"{route[i+1].arrivalStop.name} : {route[i+1].arrivalTime}\n"
            result += f"{route[i].line} {route[i].departureStop.name} : {route[i].departureTime} -> "
            line = route[i].line

        i -= 1

    result += f"{route[0].arrivalStop.name} : {route[0].arrivalTime}\n"

    return result, changeCount


def calculateTimeCost(graph, entry, time):
    currentStop = entry.departureStop
    currentTime = graph[currentStop.name].cost

    if currentTime == 0:
        waitTime = calculateTimeDifference(time, entry.departureTime)
    else:
        waitTime = calculateTimeDifference(currentStop.previous.arrivalTime, entry.departureTime)

    tripTime = entry.timeDifference

    return currentTime + waitTime + tripTime


def calculateChangeCost(graph, entry):
    currentStop = entry.departureStop
    currentChange = graph[currentStop.name].cost

    if currentChange == 0:
        change = 1
    elif currentStop.previous.line == entry.line:
        change = 0
    else:
        change = 1

    return currentChange + change


def dijkstra(start, end, time, graph):
    processedCount = 0
    que = PriorityQueue()

    startStop = graph[start]
    endStop = graph[end]

    for stop in graph.values():
        stop.initialize()

    que.put(startStop)
    startStop.cost = 0

    while not que.empty():
        currentStop = que.get()
        processedCount += 1

        if currentStop == endStop:
            break

        for entry in currentStop.schedule:
            if entry.arrivalStop != startStop:
                nextStop = entry.arrivalStop
                newCost = calculateTimeCost(graph, entry, time)
                if newCost < nextStop.cost:
                    nextStop.cost = newCost
                    que.put(nextStop)
                    nextStop.previous = entry

    if endStop.previous:
        result = "\nTrasa z " + start + " do " + end + ":\n"
        route, changes = recoverRoute(endStop)
        result += route + '\n'
        result += "Początek: " + time + '\n'
        result += "Koniec: " + endStop.previous.arrivalTime + '\n'
        result += "Czas podroży: " + secondsToTime(endStop.cost) + '\n'
        result += "Liczba przesiadek: " + str(changes) + '\n\n'
        result += "Przetworzone węzły: " + str(processedCount)
        return result, endStop.cost/60, changes, processedCount
    return "Brak", 0, 0, 0


def aStar(start, end, criterion, time, graph, h):
    processedCount = 0
    que = PriorityQueue()

    startStop = graph[start]
    endStop = graph[end]

    for stop in graph.values():
        stop.initialize()

    que.put((0, startStop))
    startStop.cost = 0

    if criterion == 't':
        while not que.empty():
            currentStop = que.get()[1]
            processedCount += 1

            if currentStop == endStop:
                break

            for entry in currentStop.schedule:
                if entry.arrivalStop != startStop:
                    nextStop = entry.arrivalStop
                    newCost = calculateTimeCost(graph, entry, time)
                    if h == "man":
                        heuristic = nextStop.hMan(endStop)
                    else:
                        heuristic = nextStop.hEuc(endStop)
                    if newCost < nextStop.cost:
                        nextStop.cost = newCost
                        que.put((newCost + heuristic, nextStop))
                        nextStop.previous = entry
    else:
        while not que.empty():
            currentStop = que.get()[1]
            processedCount += 1

            if currentStop == endStop:
                break

            for entry in currentStop.schedule:
                if entry.arrivalStop != startStop:
                    nextStop = entry.arrivalStop
                    newCost = calculateChangeCost(graph, entry)
                    if h == "man":
                        heuristic = nextStop.hMan(endStop)
                    else:
                        heuristic = nextStop.hEuc(endStop)
                    if newCost < nextStop.cost:
                        nextStop.cost = newCost
                        que.put((newCost + heuristic, nextStop))
                        nextStop.previous = entry

    if endStop.previous:
        result = "\nTrasa z " + start + " do " + end + ":\n"
        route, changes = recoverRoute(endStop)
        result += route + '\n'
        result += "Początek: " + time + '\n'
        result += "Koniec: " + endStop.previous.arrivalTime + '\n'
        result += "Czas podroży: " + secondsToTime(calculateTimeDifference(time, endStop.previous.arrivalTime)) + '\n'
        result += "Liczba przesiadek: " + str(changes) + '\n\n'
        result += "Przetworzone węzły: " + str(processedCount)
        return result, calculateTimeDifference(time, endStop.previous.arrivalTime)/60, changes, processedCount
    return "Brak", 0, 0, 0


def calculateCostMod(graph, entry, time):
    currentStop = entry.departureStop
    currentCost = graph[currentStop.name].cost

    if currentCost == 0:
        waitTime = calculateTimeDifference(time, entry.departureTime)
        change = 1
    else:
        if currentStop.previous.line == entry.line:
            change = 0
        else:
            change = 1
        waitTime = calculateTimeDifference(currentStop.previous.arrivalTime, entry.departureTime)

    tripTime = entry.timeDifference

    return currentCost + waitTime + tripTime + change * 1000


def binarySearch(array, target):
    left = 0
    right = len(array)
    index = 0

    while left < right:

        index = (left + right) // 2

        if array[index].departureTime == target:
            return index
        else:
            if array[index].departureTime < target:
                left = index + 1
            else:
                right = index

    return index


def aStarMod(start, end, time, graph, h):
    processedCount = 0
    que = PriorityQueue()

    startStop = graph[start]
    endStop = graph[end]

    for stop in graph.values():
        stop.initializeMod()

    que.put((0, startStop))
    startStop.cost = 0

    while not que.empty():
        currentStop = que.get()[1]
        processedCount += 1

        if currentStop == endStop:
            break

        index = binarySearch(currentStop.schedule, currentStop.previous.arrivalTime if currentStop.previous else time)
        for entry in currentStop.schedule[index:]:
            if entry.arrivalStop != startStop:
                nextStop = entry.arrivalStop
                newCost = calculateCostMod(graph, entry, time)
                if h == "man":
                    heuristic = nextStop.hMan(endStop)
                else:
                    heuristic = nextStop.hEuc(endStop)
                if newCost < nextStop.cost:
                    nextStop.cost = newCost
                    que.put((newCost + heuristic, nextStop))
                    nextStop.previous = entry

        for entry in currentStop.schedule[:index]:
            if entry.arrivalStop != startStop:
                nextStop = entry.arrivalStop
                newCost = calculateCostMod(graph, entry, time)
                if h == "man":
                    heuristic = nextStop.hMan(endStop)
                else:
                    heuristic = nextStop.hEuc(endStop)
                if newCost < nextStop.cost:
                    nextStop.cost = newCost
                    que.put((newCost + heuristic, nextStop))
                    nextStop.previous = entry

    if endStop.previous:
        result = "\nTrasa z " + start + " do " + end + ":\n"
        route, changes = recoverRoute(endStop)
        result += route + '\n'
        result += "Początek: " + time + '\n'
        result += "Koniec: " + endStop.previous.arrivalTime + '\n'
        result += "Czas podroży: " + secondsToTime(calculateTimeDifference(time,endStop.previous.arrivalTime)) + '\n'
        result += "Liczba przesiadek: " + str(changes) + '\n\n'
        result += "Przetworzone węzły: " + str(processedCount)
        return result, calculateTimeDifference(time, endStop.previous.arrivalTime)/60, changes, processedCount
    return "Brak", 0, 0, 0