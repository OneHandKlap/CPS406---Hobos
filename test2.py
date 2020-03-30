import math as math
import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib import cm
import poisson
from statistics import mean
import random
from hobo import Hobo
from traintrack  import TrainTrack
import numpy as np
from mpl_toolkits import mplot3d

def simulateGame(L0,L1,numTrains,lengthOfGame,hoboSmartness):

    def showGraphs():
        fig,ax = plt.subplots(numTrains)
        fig.suptitle("Presence of Trains on Tracks every second")
        deathTrack=0
        for i in range(len(trackResults)):
            hoboHistoryOnThisTrack=[]
            for j in range(len (dumbledore.positionHistory)):
                if dumbledore.positionHistory[j]==i:
                    hoboHistoryOnThisTrack.append(.5)
                    if j==score:
                        deathTrack = i
                else:
                    hoboHistoryOnThisTrack.append(None)
            ax[i].plot([x for x in range (lengthOfGame)],trackResults[i],hoboHistoryOnThisTrack,'ro')
            ax[i].set_title("Track "+str(i))
        ax[deathTrack].text(score,.5, "HOBO DIED",bbox=dict(facecolor='red', alpha=0.5))
        plt.show()


    #for each time period generate a trainTrack simulation
    tracks = [TrainTrack(L0,L1) for x in range(numTrains)]
    trackResults = [x.simulate(lengthOfGame) for x in tracks]

    #initialize our hobo object
    dumbledore= Hobo()
    dumbledore.runningResults=[[0]for x in range(numTrains)]
    score=lengthOfGame

    #MAIN GAME LOOP, each i represents a game slice or a second of the whole window
    for i in range(lengthOfGame):
        #DID HE GET HIT? Does the track he is on have a 1 at the given index? If so, decrement HP
        if trackResults[dumbledore.position][i]==1:
            dumbledore.hp-=1
            #O SHIT, HE DIED END THE GAME
            if dumbledore.hp==0:
                score=i
                return score

        #GET PAPER PLANE
        paperPlane=[]
        if (random.randint(1,100)<=99) and i<lengthOfGame-1:
            
            for y in range(numTrains):
                paperPlane.append(trackResults[y][i+1])

        else:
            for y in range(numTrains):
                paperPlane.append(random.randint(0,1))
            dumbledore.getSuggestion(paperPlane)
