from datetime import datetime
from math import *

import pandas as pd


def loadData():
    connectionGraph = pd.read_csv('connection_graph.csv', low_memory=False)

    dijkstraGraph = {}
    aStarGraph = {}

    for index, row in connectionGraph.iterrows():
        line = row["line"]
        departureTime = row["departure_time"]
        arrivalTime = row["arrival_time"]
        startStop = row["start_stop"]
        endStop = row["end_stop"]
        startStopLat = row["start_stop_lat"]
        startStopLon = row["start_stop_lon"]
        endStopLat = row["end_stop_lat"]
        endStopLon = row["end_stop_lon"]

        dijkstraGraph.setdefault(startStop, StopDijkstra(startStop, startStopLat, startStopLon))
        dijkstraGraph.setdefault(endStop, StopDijkstra(endStop, endStopLat, endStopLon))
        dijkstraGraph[startStop].addToSchedule(line, dijkstraGraph[startStop], departureTime, dijkstraGraph[endStop],
                                               arrivalTime)

        aStarGraph.setdefault(startStop, StopAStar(startStop, startStopLat, startStopLon))
        aStarGraph.setdefault(endStop, StopAStar(endStop, endStopLat, endStopLon))
        aStarGraph[startStop].addToSchedule(line, aStarGraph[startStop], departureTime, aStarGraph[endStop],
                                            arrivalTime)

    return dijkstraGraph, aStarGraph


def timeToSeconds(time):
    hour = int(time[:2])
    minute = int(time[3:5])
    second = int(time[6:])
    return 60 * 60 * hour + 60 * minute + second


def secondsToTime(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time = "{:02d}h {:02d}m {:02d}s ".format(hours, minutes, seconds)
    return time


def calculateTimeDifference(startTime, endTime):
    if startTime <= endTime:
        return timeToSeconds(endTime) - timeToSeconds(startTime)
    return 24 * 60 * 60 + timeToSeconds(endTime) - timeToSeconds(startTime)


class Stop:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

        self.schedule = []

    def __str__(self):
        result = f"{self.name} \nSchedule:\n"

        for entry in self.schedule:
            result += str(entry) + "\n"

        return result

    def addToSchedule(self, line, departureStop, departureTime, arrivalStop, arrivalTime):
        self.schedule.append(ScheduleEntry(line, departureStop, departureTime, arrivalStop, arrivalTime))


class ScheduleEntry:
    def __init__(self, line, departureStop, departureTime, arrivalStop, arrivalTime):
        self.line = line
        self.departureStop = departureStop
        self.departureTime = departureTime
        self.arrivalStop = arrivalStop
        self.arrivalTime = arrivalTime
        self.timeDifference = calculateTimeDifference(departureTime, arrivalTime)

    def __str__(self):
        return f"{self.line} {self.departureStop.name} : {self.departureTime} -> {self.arrivalStop.name} : {self.arrivalTime}"


class StopDijkstra(Stop):
    def __init__(self, name, latitude, longitude):
        super().__init__(name, latitude, longitude)
        self.previous = None
        self.cost = None

    def initialize(self):
        self.cost = inf
        self.previous = None

    def __lt__(self, other):
        return self.cost < other.cost


class StopAStar(Stop):
    def __init__(self, name, latitude, longitude):
        super().__init__(name, latitude, longitude)
        self.previous = None
        self.cost = None

    def initialize(self):
        self.cost = inf
        self.previous = None

    def initializeMod(self):
        self.cost = inf
        self.previous = None
        self.schedule.sort(key=lambda x: x.departureTime)

    def hMan(self, endStop):
        return abs(self.latitude-endStop.latitude) + abs(self.longitude-endStop.longitude)

    def hEuc(self, endStop):
        return sqrt((self.latitude-endStop.latitude)**2 + (self.longitude-endStop.longitude)**2)

    def __lt__(self, other):
        return self.cost < other.cost
