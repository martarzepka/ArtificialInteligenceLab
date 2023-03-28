import time
from ex1 import *
from test import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dijkstraGraph, aStarGraph = loadData()

    test(dijkstraGraph, aStarGraph, 100)

    # print("Dijkstra:")
    #
    # start = time.time()
    # print(dijkstra('PL. GRUNWALDZKI', 'Rysia', '15:10:00', dijkstraGraph)[0])
    # end = time.time()
    # print(f"Czas obliczeń = {end - start} sekund")
    #
    # print("\nA* (t):")
    #
    # start = time.time()
    # print(aStar('PL. GRUNWALDZKI', 'Rysia', 't', '15:10:00', aStarGraph, "man")[0])
    # end = time.time()
    # print(f"Czas obliczeń = {end - start} sekund")
    #
    # print("\nA* (p):")
    #
    # start = time.time()
    # print(aStar('PL. GRUNWALDZKI', 'Rysia', 'p', '15:10:00', aStarGraph, "man")[0])
    # end = time.time()
    # print(f"Czas obliczeń = {end - start} sekund")

    # start = time.time()
    # print(aStar('PL. GRUNWALDZKI', 'Rysia', 'p', '15:10:00', aStarGraph, "man")[0])
    # end = time.time()
    # print(f"Czas obliczeń = {end - start} sekund")

    # print("\nA* (modyfikacja):")
    #
    # start = time.time()
    # print(aStarMod('PL. GRUNWALDZKI', 'Rysia', '15:10:00', aStarGraph, "man")[0])
    # end = time.time()
    # print(f"Czas obliczeń = {end - start} sekund")

    # start = time.time()
    # print(aStarMod('PL. GRUNWALDZKI', 'Rysia', '15:10:00', aStarGraph, "euc")[0])
    # end = time.time()
    # print(f"Czas obliczeń = {end - start} sekund")

