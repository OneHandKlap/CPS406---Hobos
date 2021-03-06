import math as math
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
import pandas as pd
import csv
from matplotlib import cm
import poisson
from statistics import mean
import random
from hobo import Hobo
from traintrack import TrainTrack
import numpy as np
from mpl_toolkits import mplot3d


def simulateTrains(L0, L1, numTrains, duration):
    tracks = [TrainTrack(L0, L1) for x in range(numTrains)]
    results = [x.simulate(duration) for x in tracks]
    # print(results)
    fig, ax = plt.subplots(numTrains)
    fig.suptitle("Presence of Trains on Tracks every second")
    for i in range(len(results)):
        ax[i].plot([x for x in range(duration)], results[i])
        ax[i].set_title("Track "+str(i))
    plt.show()


def simulateGame(L0, L1, numTrains, lengthOfGame, hoboSmartness, trackResults=[]):
    def showGraphs():
        fig, ax = plt.subplots(numTrains)
        fig.suptitle("Presence of Trains on Tracks every second")
        deathTrack = 0
        for i in range(len(trackResults)):
            hoboHistoryOnThisTrack = []
            for j in range(len(dumbledore.positionHistory)):
                if dumbledore.positionHistory[j] == i:
                    # # print("J: "+str(j))
                    hoboHistoryOnThisTrack.append(.5)
                    if j == score:
                        # print("SCORE: "+str(score))
                        # print("DEATH TRACK: "+str(i))
                        deathTrack = i
                else:
                    hoboHistoryOnThisTrack.append(None)
            ax[i].plot([x for x in range(lengthOfGame)], trackResults[i], hoboHistoryOnThisTrack, 'ro')
            ax[i].set_title("Track " + str(i))
        ax[deathTrack].text(score, .5, "HOBO DIED", bbox=dict(facecolor='red', alpha=0.5))
        plt.show()
    # for each 60second window generate TrainTrack results
    tracks = [TrainTrack(L0, L1) for x in range(numTrains)]
    if trackResults == []:
        trackResults = [x.simulate(lengthOfGame) for x in tracks]
    # print("TRACKRESULTS: "+str(trackResults))
    dumbledore = Hobo()
    dumbledore.runningResults = [[0] for x in range(numTrains)]
    score = lengthOfGame
    for i in range(lengthOfGame):
        # DID HE GET HIT?
        if trackResults[dumbledore.position][i] == 1:
            dumbledore.hp -= 1
            # O SHIT, HE DED END THE GAME
            if dumbledore.hp == 0:
                score = i
                # showGraphs()
                return score
        # GET PAPER PLANE
        paperPlane = []
        if (random.randint(1, 100) <= 75) and i < lengthOfGame - 1:
            for y in range(numTrains):
                paperPlane.append(trackResults[y][i+1])
        else:
            for y in range(numTrains):
                paperPlane.append(random.randint(0, 1))
            dumbledore.getSuggestion(paperPlane)
        # LOOKS AROUND AT TRAINS
        dumbledore.lookAtTracks(i, trackResults)
        # STORES WHAT HE SEES
        dumbledore.updateResults()
        # JUMP
        dumbledore.act(hoboSmartness)
    # showGraphs()
    return score


# DISPLAY METHODS
def overallAverageGraphs():
    for hoboLevel in range(5):
        fig = plt.figure(figsize=plt.figaspect(0.5))
        for numTrains in range(2, 10, 2):
            results = []
            L0axis = []
            L1axis = []
            for L0 in range(1, 17, 2):
                for L1 in range(1, 17, 2):
                    #print("CALCULATING AVERAGE OF SMARTNESS : "+str(i+1))
                    for j in range(10):
                        if results != None:
                            results.append(simulateGame(
                                L0, L1, numTrains, 500, hoboLevel))
                        else:
                            results = [simulateGame(
                                L0, L1, numTrains, 500, hoboLevel)]
                        L0axis.append(L0)
                        L1axis.append(L1)
            ax = fig.add_subplot(2, 2, numTrains/2, projection='3d')
            L0axis = np.array(L0axis)
            L1axis = np.array(L1axis)
            results = np.array(results)
            ax.plot_trisurf(L0axis, L1axis, results, linewidth=0, antialiased=False)
            plt.title("Score Hobo Level" + str(hoboLevel) + " - #Trains: " + str(numTrains))
            plt.xlabel("L0 mean")
            plt.ylabel("L1 mean")
        plt.show()


def hitRateComparisonGraph():
    results0 = []
    results4 = []
    x = []
    for i in range(30, 150, 10):
        x.append(i)
        meanResult0 = []
        meanResult4 = []
        for j in range(25):
            meanResult0.append(simulateGame(7, 7, 5, i, 0))
            meanResult4.append(simulateGame(7, 7, 5, i, 4))
        results0.append(20 / mean(meanResult0))
        results4.append(20 / mean(meanResult4))
    fig, ax = plt.subplots(2)
    fig.suptitle("Comparison of Hit-Rate")
    custom_ylim = (0, 1)
    custom_xlim = (30, 150)
    x = np.array(x)
    ax[0].plot(x, results0, 'ro')
    ax[0].set_title("Hobo Level 0")
    b, m = polyfit(x, results0, 1)
    ax[0].plot(x, b+m*x, '-')
    ax[1].plot(x, results4, 'ro')
    b, m = polyfit(x, results4, 1)
    ax[1].set_title("Hobo level 4")
    ax[1].plot(x, b+m*x, '-')
    plt.setp(ax, ylim=custom_ylim, xlim=custom_xlim)
    plt.show()


def displayOverallAverages():
    for hoboLevel in range(5):
        avgScore = []
        for numTrains in range(2, 10, 2):
            results = []
            for L0 in range(1, 15, 2):
                for L1 in range(1, 15, 2):
                    #print("CALCULATING AVERAGE OF SMARTNESS : "+str(i+1))
                    for j in range(10):
                        if results != None:
                            results.append(simulateGame(
                                L0, L1, numTrains, 500, hoboLevel))
                        else:
                            results = [simulateGame(
                                L0, L1, numTrains, 500, hoboLevel)]
            avgScore.append(mean(results))
        print("Hobo Level: "+str(hoboLevel) + " Overall Average Score: " + str(mean(avgScore)) + "\n")


overallAverageGraphs()
