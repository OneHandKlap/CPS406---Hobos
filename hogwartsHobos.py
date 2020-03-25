import math as math
import matplotlib.pyplot as plt
import random
e=math.e


class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

def poisson(k, l):
    exp = math.pow(e,-l)
    lambdaPower = math.pow(l,k)
    num = exp*lambdaPower
    denom = math.factorial(k)
    return num/denom


def poissonValues(mean):
    
    trainChance=my_dictionary()
    for i in range(100):
        if poisson(i,mean)*100 >=.5:
            trainChance.add(i,round(poisson(i,mean)*100))
    keys=[x for x in trainChance.keys()]
    for i in range(1,len(trainChance.keys())):
        trainChance[keys[i]]=trainChance[keys[i]]+trainChance[keys[i]-1]
    return trainChance

class Hobo:

    def __init__(self):
        self.hp=20
        self.position=0
        self.info=[[],[]] #List of lists, first represents the trainState of tracks this second, second list for next second
        self.runningResults=[[]]
        self.runningL0=[] #time between trains
        self.runningL1=[] #time of train on track
        self.positionHistory=[0]

    
    def getSuggestion(self,listOfTrackVals):
        self.info[1]=listOfTrackVals

    def act(self):
        
        #based on my calculations i should jump to:
        trackSafeness = self.doMaths()

        #if my calculations say I have a better than 60% chance of being safe, ignore paper plane
        if trackSafeness and (max(trackSafeness)>60):
            self.position = trackSafeness.index(max(trackSafeness))
            self.positionHistory.append(self.position)
            print("DID MATH JUMPING TO: "+str(self.position))
        #basic logic
        #find an empty track, jump to it
        elif self.info[1]==[]:
            for i in range(len(self.info[0])):
                if self.info[0][i]==0:
                    self.position = i
                    print("FOUND EMPTY TRACK, JUMPING TO: "+str(i))
                    self.positionHistory.append(self.position)
                    break
        
        #still basic, but now gjumps based on paperplane info
        else: 
            for i in range(len(self.info[1])):
                if self.info[1][i]==0:
                    self.position = i
                    print("FOUND EMPTY TRACK (VIA AIRPLANE), JUMPING TO: "+str(i))
                    self.positionHistory.append(self.position)
                    break


        #complex logic
        #decide which track to jump to
        #determine validity of suggestion




    def updateResults(self):
        try:
            for i in range(len(self.info[0])):

                if self.runningResults[i][0]==self.info[0][i]:
                    self.runningResults[i].append(self.info[0][i])
                else:
                    if self.info[0][i]==1:
                        self.runningL0.append(len(self.runningResults[i]))
                        self.runningResults[i]=[]
                        self.runningResults[i].append(self.info[0][i])

                    if self.info[0][i]==0:
                        self.runningL1.append(len(self.runningResults[i]))
                        self.runningResults[i]=[]
                        self.runningResults[i].append(self.info[0][i])
        except(IndexError):
            for i in range(len(self.info[0])):
                self.runningResults[i].append(self.info[0][i])

    def doMaths(self):

        #look at all tracks
        #if a track is empty calculate poisson using L0 and length of recent history of that track + 1
        #vice versa if the track has a train on it
        #convert to "Safeness Score"
        #this will result in a list of tracks of varying safeness
        #jump to the safest track
        
        if self.runningL0 and self.runningL1:
            print("DOING MATH")
            trackSafeness=[]
            runningMeanL0=sum(self.runningL0)/(len(self.runningL0))
            runningMeanL1=sum(self.runningL1)/(len(self.runningL1))

            for x in self.runningResults:
                if x[0]== 0: #track is empty
                    #calculate poisson
                    trackSafeness.append(100*poisson(len(x)+1,runningMeanL0))

                if x[0]==1: #track has train

                    trackSafeness.append(100-(100*poisson(len(x)+1,runningMeanL1)))

            print("TRACK SAFENESS: "+str(trackSafeness))
            return (trackSafeness)




    # def updateMeans(self):
    #     #DO CALCULATION ONLY ON STATE CHANGE

    #     for i in range(len(self.info[0])):



    #     L0=[5,2]
    #     L1=[3,5]
    #     track1results=[1,1,1,1,1,0,0,0,1,1,0,0,0,0,0]
    #     track 1 =[1,1,1,1,1]
    #     L0.append(count track 1)
    #     track 1 =[1]



    def lookAtTracks(self,num,listOfTrackResults):
        self.info[0]= [x[num] for x in listOfTrackResults]

class TrainTrack:
    def __init__(self,L0,L1):
        self.L0=poissonValues(L0)
        self.L1=poissonValues(L1)
        self.hasTrain=False
        self.isWaiting=False
        self.trackOccupancy=[0]
    def getTimeBetweenTrains(self):
        r=random.randint(1,100)
        for key, val in self.L0.items():
            if r<= val:
                return key
        return list(self.L0.keys())[len(self.L0.keys())-1]
    def getHowLong(self):
        r=random.randint(1,100)
        for key, val in self.L1.items():
            if r<= val:
                return key
        return list(self.L1.keys())[len(self.L1.keys())-1]
    def simulate(self):
        waitFor=0
        thisTrain=0
        if(random.randint(1,100)>50):
            self.isWaiting=True
            waitFor=self.getHowLong()
        for i in range (1,60):
            print("SECOND : "+str(i))
            if self.isWaiting==True and i >= waitFor:
                self.isWaiting=False
            if self.hasTrain and i >=thisTrain:
                self.hasTrain = False
            if self.hasTrain == False and self.isWaiting==False:
                self.hasTrain=True
                self.isWaiting=True
                thisTrain = i + self.getHowLong()
                waitFor = waitFor + self.getTimeBetweenTrains()
            if self.hasTrain == True:
                self.trackOccupancy.append(0)
            else:
                self.trackOccupancy.append(1)
        return self.trackOccupancy




def simulateTrains(L0,L1,numTrains):
    tracks = [TrainTrack(L0,L1) for x in range(numTrains)]
    results=[x.simulate() for x in tracks]
    print(results)
    fig,ax = plt.subplots(numTrains)
    fig.suptitle("Presence of Trains on Tracks every second")
    for i in range(len(results)):
        
        ax[i].plot([x for x in range (60)],results[i])
        ax[i].set_title("Track "+str(i))
        
    plt.show()

def simulateGame(L0,L1,numTrains,hobo=0):
    #for each 60second window generate TrainTrack results
    tracks = [TrainTrack(L0,L1) for x in range(numTrains)]
    trackResults = [x.simulate() for x in tracks]
    print("TRACKRESULTS: "+str(trackResults))
    if hobo:
        dumbledore= hobo
    else:
        dumbledore= Hobo()
    dumbledore.runningResults=[[]for x in range(numTrains)]
    score=10000000000
    for i in range(60):
        print("DUMBLEDORE POSITION: "+str(dumbledore.position))
        
        

        #DID HE GET HIT?
        if trackResults[dumbledore.position][i]==1:
            dumbledore.hp-=1
            if dumbledore.hp==0:
                score=i
                break

        #GET PAPER PLANE
        paperPlane=[]
        if (random.randint(1,100)<=60):
            for y in range(numTrains):
                paperPlane.append(trackResults[y][i])
        else:
            for y in range(numTrains):
                paperPlane.append(random.randint(0,1))
        dumbledore.getSuggestion(paperPlane)
        print("PAPER PLANE INFO: "+str(paperPlane))

        #LOOKS AROUND AT TRAINS
        dumbledore.lookAtTracks(i,trackResults)
        print("CURRENT STATE OF TRAINS: "+str(dumbledore.info[0]))
        print("DUMBLEDORE HP: "+str(dumbledore.hp))

        #STORES WHAT HE SEES
        dumbledore.updateResults()
        print("DUMBLEDORE'S MEMORY: "+str(dumbledore.runningResults))
        print("RUNNING L0: "+str(dumbledore.runningL0))
        print("RUNNING L1: "+str(dumbledore.runningL1))
        
        #DO MATHS
        
        #look at all tracks
        #if a track is empty calculate poisson using L0 and length of recent history of that track + 1
        #vice versa if the track has a train on it
        #convert to "Safeness Score"
        #this will result in a list of tracks of varying safeness
        #jump to the safest track

        #JUMP
        dumbledore.act()


    fig,ax = plt.subplots(numTrains)
    fig.suptitle("Presence of Trains on Tracks every second")
    
    for i in range(len(trackResults)):
        hoboHistoryOnThisTrack=[]
        deathTrack=0
        for j in range(len (dumbledore.positionHistory)):
            if dumbledore.positionHistory[j]==i:
                hoboHistoryOnThisTrack.append(.5)
                if j == score:
                    deathTrack = i
            else:
                hoboHistoryOnThisTrack.append(None)
        ax[i].plot([x for x in range (60)],trackResults[i],hoboHistoryOnThisTrack,'ro')
        ax[i].set_title("Track "+str(i))
    ax[deathTrack].text(score,.5, "HOBO DIED")
    plt.show()


    return "GAME OVER! SCORE: " +str(score) + " L0: "+str(sum(dumbledore.runningL0)/(len(dumbledore.runningL0)))+" L1: "+str(sum(dumbledore.runningL1)/(len(dumbledore.runningL1)))
        #Hobo action every second
# track = TrainTrack(5,3)
# track,simulateTrains(5,3,2)
print(simulateGame(5,3,4))



#TO DO: GRAPHICAL REPRESENTATION OF HOBO MOVEMENT, IMPLEMENT 60% VERACITY PAPER PLANE, IMPLEMENT 3 DECISION CASES

#player profile # case 1: just jump to an empty track - hypothesis lowest survivability rate, based on number of tracks and his health
#player profile # case 2: using paper planes - hypothesis surivability slightly increased, based on tracks,health, and % veracity of paper plane
#player profile # case 3: using his memory and running average calculation - hypothesis survivability greatly increased but only towards the end,
#player profile # case 4: blend of 2 and 3
#player profile # case 5: genetic learning.