import math as math
import matplotlib.pyplot as plt
from matplotlib import cm
import poisson
from statistics import mean
import random
from hobo import Hobo
from traintrack  import TrainTrack
import numpy as np
from mpl_toolkits import mplot3d

def simulateTrains(L0,L1,numTrains,duration):
    tracks = [TrainTrack(L0,L1) for x in range(numTrains)]
    results=[x.simulate(duration) for x in tracks]
    # print(results)
    fig,ax = plt.subplots(numTrains)
    fig.suptitle("Presence of Trains on Tracks every second")
    for i in range(len(results)):
        
        ax[i].plot([x for x in range (duration)],results[i])
        ax[i].set_title("Track "+str(i))
        
    plt.show()

def simulateGame(L0,L1,numTrains,lengthOfGame,hoboSmartness,trackResults=[]):

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
    if trackResults==[]:
        trackResults = [x.simulate(lengthOfGame) for x in tracks]

    # print("TRACKRESULTS: "+str(trackResults))
   
    dumbledore= Hobo()
    dumbledore.runningResults=[[0]for x in range(numTrains)]
    score=lengthOfGame
    for i in range(lengthOfGame):

        #print("SECOND: "+str(i))
        # print("DUMBLEDORE POSITION: "+str(dumbledore.position))
        
        

        #DID HE GET HIT?
        if trackResults[dumbledore.position][i]==1:
            dumbledore.hp-=1
            # print("DUMBLEDORE GOT HIT")
            #O SHIT, HE DED END THE GAME
            if dumbledore.hp==0:
                score=i
                #showGraphs()
                return score

        #GET PAPER PLANE
        paperPlane=[]
        if (random.randint(1,100)<=90) and i<lengthOfGame-1:
            
            for y in range(numTrains):
                paperPlane.append(trackResults[y][i+1])
            #print("THIS PLANE IS TRUE: "+str(paperPlane))
            #print()
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
        # print("RUNNING L0: "+str(dumbledore.runningL0))
        # print("RUNNING L1: "+str(dumbledore.runningL1))
        
        

        #JUMP
        dumbledore.act(hoboSmartness)
        # print("POSITION HISTORY : "+str(dumbledore.positionHistory))
        # print("DUMBLEDORE POSITION: "+str(dumbledore.position))

    
    #showGraphs()
    return score
    #return dumbledore.positionHistory
    #return "GAME OVER! SCORE: " +str(score) + " L0: "+str(sum(dumbledore.runningL0)/(len(dumbledore.runningL0)))+" L1: "+str(sum(dumbledore.runningL1)/(len(dumbledore.runningL1)))


# results=[]
# for j in range(100):
#     if results!= None:
#         results.append(simulateGame(1,3,2,400,1))
#     else:
#         results=[simulateGame(1,3,2,400,1)]
# print(results)
# print(mean(results))
#print(simulateGame(5,4,2,400,3))


#BEGINNING OF TESTS


results=[[] for x in range(4)]
for i in range(4):
    print("CALCULATING AVERAGE OF SMARTNESS : "+str(i+1))
    for j in range(10):

        if results[i]!= None:
            results[i].append(simulateGame(5,3,2,100,i+1))
        else:
            results[i]=[simulateGame(5,3,2,100,i+1)]
    print(results[i])

print("SMARTNESS 1 AVG: "+str(mean(results[0])) +"\nSMARTNESS 2 AVG: "+str(mean(results[1]))+"\nSMARTNESS 3 AVG: "+str(mean(results[2]))+"\nSMARTNESS 4 AVG: "+str(mean(results[3])))


# fig = plt.figure(figsize = plt.figaspect(0.5))

# for numTrains in range(1,8):

#     results=[]
#     L0axis=[]
#     L1axis=[]
#     for L0 in range(1,15):
#         for L1 in range(1,15):
#             #print("CALCULATING AVERAGE OF SMARTNESS : "+str(i+1))
#             for j in range(10):

#                 if results!= None:
#                     results.append(simulateGame(L0,L1,numTrains,100,3))
#                 else:
#                     results=[simulateGame(L0,L1,numTrains,100,3)]
#                 L0axis.append(L0)
#                 L1axis.append(L1)

    
#     ax = fig.add_subplot(4,2,numTrains, projection = '3d')
#     L0axis=np.array(L0axis)
#     L1axis=np.array(L1axis)

#     results=np.array(results)

#     ax.plot_trisurf(L0axis,L1axis,results,linewidth=0, antialiased=False)
#     title="Hobo 3 Trains: " +str(numTrains) +".png"
#     plt.title("Score Hobo Level 3 - #Trains: "+str(numTrains))
#     plt.xlabel("L0 mean")
#     plt.ylabel("L1 mean")

# plt.show()




#print(simulateGame(5,3,2,100,1))