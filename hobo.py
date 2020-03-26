import poisson
import random

class Hobo:
    
    def __init__(self):
        self.hp=20
        self.position=0
        self.info=[[],[]] #List of lists, first represents the trainState of tracks this second, second list for next second
        self.runningResults=[[]] #memory of tracks that havent changed yet
        self.runningL0=[] #time between trains
        self.runningL1=[] #time of train on track
        self.positionHistory=[0]

    
    def getSuggestion(self,listOfTrackVals):
        self.info[1]=listOfTrackVals

    def act(self,smartness):
        
        if smartness == 1:
            #THIS SMARTNESS LEVEL IS CHARACTERIZED BY MERELY JUMPING TO THE FIRST TRACK THAT IS EMPTY RIGHT NOW
            for i in range(len(self.info[0])):
                if self.info[0][i]==0:
                    self.position = i
                    # print("FOUND EMPTY TRACK, JUMPING TO: "+str(i))
                    self.positionHistory.append(self.position)
                    return
            # print("NO POINT MOVING")
            self.positionHistory.append(self.position)
        
        elif smartness == 2:
            #THIS SMARTNESS LEVEL JUMPS TO THE FIRST EMPTY TRACK OUTLINED BY THE PAPER PLANE (WHICH PURPORTS TO KNOW WHAT THE STATE WILL BE NEXT SECOND)
            for i in range(len(self.info[1])):
                if self.info[1][i]==0:
                    self.position = i
                    # print("FOUND EMPTY TRACK (VIA AIRPLANE), JUMPING TO: "+str(i))
                    self.positionHistory.append(self.position)
                    return
            self.positionHistory.append(self.position)
        elif smartness == 3:
            #USES RUNNING MEANS TO DETERMINE THE LIKELIHOOD THAT A TRACK STATE WILL CHANGE, AND BECOME SAFE NEXT SECOND, IF >90% JUMP, ELSE JUMP TO FIRST EMPTY THIS TURN
            trackSafeness = self.doMaths()
            # print(trackSafeness)
            #if my calculations say I have a better than 90% chance of being safe, go to the best odds
            if trackSafeness and (max(trackSafeness)>60) and (1 not in self.info[0]):
                # print("TRUSTING MY HEAD")
                self.position = trackSafeness.index(max(trackSafeness))
                self.positionHistory.append(self.position)
                # print("DID MATH JUMPING TO: "+str(self.position))
            else:
                # print("TRUSTING MY GUT")
                for i in range(len(self.info[0])):
                    if self.info[0][i]==0:
                        self.position = i
                        # print("FOUND EMPTY TRACK, JUMPING TO: "+str(i))
                        self.positionHistory.append(self.position)
                        return
                self.positionHistory.append(self.position)
        else:
            #USES RUNNING MEANS TO DETERMINE THE LIKELIHOOD THAT A TRACK STATE WILL CHANGE, AND BECOME SAFE NEXT SECOND, IF >90% JUMP, ELSE JUMP TO FIRST FROM PAPER PLANE
            #based on my calculations i should jump to:
            trackSafeness = self.doMaths()
            # print(trackSafeness)
            #if my calculations say I have a better than 60% chance of being safe, ignore paper plane
            if trackSafeness and (max(trackSafeness)>80):
                # print("TRUSTING MY HEAD")
                self.position = trackSafeness.index(max(trackSafeness))
                self.positionHistory.append(self.position)

            else: 
                # print("TRUSTING MY BUDDY")
                
                for i in range(len(self.info[1])):
                    if self.info[1][i]==0:
                        self.position = i
                        # print("FOUND EMPTY TRACK (VIA AIRPLANE), JUMPING TO: "+str(i))
                        self.positionHistory.append(self.position)
                        return
                self.positionHistory.append(self.position)
        

    def updateResults(self):

        #update the running memory of HOBO
        #the idea is that state changes are important, they are what feed the runningmean values for L0 and L1
        # print("THIS TRACK: "+str(self.info[0]))
        # print("HOBO MEMORY: "+str(self.runningResults))
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
        # except(IndexError):
        #     return (self.info[0])
        #     for i in range(len(self.info[0])):
        #         self.runningResults[i].append(self.info[0][i])

    def doMaths(self):

        #look at all tracks
        #if a track is empty calculate poisson using L0 and length of recent history of that track + 1
        #vice versa if the track has a train on it
        #convert to "Safeness Score"
        #this will result in a list of tracks of varying safeness
        #RETURN
        
        try: 
            if self.runningL0 and self.runningL1:
                # print("DOING MATH")
                trackSafeness=[]
                runningMeanL0=sum(self.runningL0)/(len(self.runningL0))
                runningMeanL1=sum(self.runningL1)/(len(self.runningL1))

                for x in self.runningResults:
                    if x[0]== 0: #track is empty
                        #calculate poisson
                        getValues = poisson.poissonValues(runningMeanL0)
                        #print(getValues)
                        #find key which is len(x)+1
                        key=len(x)+1
                        if key in getValues.keys():
                            trackSafeness.append(100-getValues[key])
                        else:
                            trackSafeness.append(100)
                        #trackSafeness.append(100*poisson.poisson(len(x)+1,runningMeanL0))

                    if x[0]==1: #track has train
                        
                        getValues = poisson.poissonValues(runningMeanL1)
                        #print(getValues)
                        #find key which is len(x)+1
                        key=len(x)+1
                        if key in getValues.keys():
                            trackSafeness.append(100-getValues[key])
                        else:
                            trackSafeness.append(100)
                        # trackSafeness.append(100*poisson.poisson(len(x)+1,runningMeanL1))

                # print("TRACK SAFENESS: "+str(trackSafeness))
                return (trackSafeness)
        except(OverflowError):
            print("OVERFLOW ERROR: L0 = "+str(runningMeanL0)+" L1 = "+str(runningMeanL1)+" ")

    def lookAtTracks(self,num,listOfTrackResults):
        self.info[0]= [x[num] for x in listOfTrackResults]
