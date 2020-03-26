import poisson
import random
class TrainTrack:
    def __init__(self,L0,L1):
        self.L0=poisson.poissonValues(L0)
        self.L1=poisson.poissonValues(L1)
        self.hasTrain=False
        self.isWaiting=False
        self.trackOccupancy=[0]
    def getTimeBetweenTrains(self):
        r=random.randint(0,100)
        for key, val in self.L0.items():
            if r<= val:
                return key
        return list(self.L0.keys())[len(self.L0.keys())-1]
    def getHowLong(self):
        r=random.randint(0,100)
        for key, val in self.L1.items():
            if r<= val:
                return key
        return list(self.L1.keys())[len(self.L1.keys())-1]
    def simulate(self,duration):
        waitFor=0
        thisTrain=0
        if(random.randint(1,100)>50):
            self.isWaiting=True
            waitFor=self.getTimeBetweenTrains()
        for i in range (1,duration):
            # print("SECOND : "+str(i))
            if self.isWaiting==True and i >= waitFor:
                self.isWaiting=False
            if self.hasTrain and i >=thisTrain:
                self.hasTrain = False
            if self.hasTrain == False and self.isWaiting==False:
                self.hasTrain=True
                self.isWaiting=True
                thisTrain = i + self.getHowLong()
                waitFor = thisTrain + self.getTimeBetweenTrains()
            if self.hasTrain == True:
                self.trackOccupancy.append(1)
            else:
                self.trackOccupancy.append(0)
        return self.trackOccupancy
