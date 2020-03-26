import math as math
import matplotlib.pyplot as plt
import poisson
from statistics import mean
import random
from hobo import Hobo
from traintrack  import TrainTrack




def simulateTrains(L0,L1,numTrains):
    tracks = [TrainTrack(L0,L1) for x in range(numTrains)]
    results=[x.simulate() for x in tracks]
    # print(results)
    fig,ax = plt.subplots(numTrains)
    fig.suptitle("Presence of Trains on Tracks every second")
    for i in range(len(results)):
        
        ax[i].plot([x for x in range (60)],results[i])
        ax[i].set_title("Track "+str(i))
        
    plt.show()

def simulateGame(L0,L1,numTrains,lengthOfGame,hoboSmartness,hobo=0):

    def showGraphs():
        fig,ax = plt.subplots(numTrains)
        fig.suptitle("Presence of Trains on Tracks every second")
        deathTrack=0
        for i in range(len(trackResults)):
            hoboHistoryOnThisTrack=[]
            for j in range(len (dumbledore.positionHistory)):
                if dumbledore.positionHistory[j]==i:
                    # # print("J: "+str(j))
                    hoboHistoryOnThisTrack.append(.5)
                    if j == score:
                        
                        # print("SCORE: "+str(score))
                        # print("DEATH TRACK: "+str(i))
                        deathTrack = i
                else:
                    hoboHistoryOnThisTrack.append(None)
            ax[i].plot([x for x in range (lengthOfGame)],trackResults[i],hoboHistoryOnThisTrack,'ro')
            ax[i].set_title("Track "+str(i))
        ax[deathTrack].text(score,.5, "HOBO DIED",bbox=dict(facecolor='red', alpha=0.5))
        plt.show()



    #for each 60second window generate TrainTrack results
    tracks = [TrainTrack(L0,L1) for x in range(numTrains)]
    trackResults = [x.simulate(lengthOfGame) for x in tracks]

    # print("TRACKRESULTS: "+str(trackResults))
    if hobo:
        dumbledore= hobo
    else:
        dumbledore= Hobo()
    dumbledore.runningResults=[[]for x in range(numTrains)]
    score=lengthOfGame
    for i in range(lengthOfGame):
        # print("SECOND: "+str(i))
        # print("DUMBLEDORE POSITION: "+str(dumbledore.position))
        
        

        #DID HE GET HIT?
        if trackResults[dumbledore.position][i]==1:
            dumbledore.hp-=1
            #O SHIT, HE DED END THE GAME
            if dumbledore.hp==0:
                score=i
                #showGraphs()
                return score

        #GET PAPER PLANE
        paperPlane=[]
        if (random.randint(1,100)<=30):
            for y in range(numTrains):
                paperPlane.append(trackResults[y][i])
        else:
            for y in range(numTrains):
                paperPlane.append(random.randint(0,1))
        dumbledore.getSuggestion(paperPlane)
        # print("PAPER PLANE INFO: "+str(paperPlane))

        #LOOKS AROUND AT TRAINS

        dumbledore.lookAtTracks(i,trackResults)
        acc=[]
        for j in range(numTrains):
            acc.append(trackResults[j][i])
        # print("WHAT IS ON THE TRACK NOW: "+str(acc))
        # print("WHAT DUMBLEDORE SEES: "+str(dumbledore.info[0]))
        # # print("DUMBLEDORE HP: "+str(dumbledore.hp))

        #STORES WHAT HE SEES
        dumbledore.updateResults()
        # # print("DUMBLEDORE'S MEMORY: "+str(dumbledore.runningResults))
        # # print("RUNNING L0: "+str(dumbledore.runningL0))
        # # print("RUNNING L1: "+str(dumbledore.runningL1))
        
        

        #JUMP
        dumbledore.act(hoboSmartness)
        # print("POSITION HISTORY : "+str(dumbledore.positionHistory))

    
    #showGraphs()
    return score
    #return "GAME OVER! SCORE: " +str(score) + " L0: "+str(sum(dumbledore.runningL0)/(len(dumbledore.runningL0)))+" L1: "+str(sum(dumbledore.runningL1)/(len(dumbledore.runningL1)))




#print(simulateGame(5,1,2,100,1))


#BEGINNING OF TESTS

results=[[] for x in range(4)]

for i in range(4):

    for j in range(100):
        if results[i]!= None:
            results[i].append(simulateGame(5,3,9,100,i))
        else:
            results[i]=[simulateGame(5,3,2,100,i)]

print("SMARTNESS 1 AVG: "+str(mean(results[0])) +"\nSMARTNESS 2 AVG: "+str(mean(results[1]))+"\nSMARTNESS 3 AVG: "+str(mean(results[2]))+"\nSMARTNESS 4 AVG: "+str(mean(results[3])))


