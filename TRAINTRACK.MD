# TrainTrack Class
## Brief overview of TrainTracks

TrainTracks are datastructures that take in two numbers representing the average time between trains, and the average length of a train. They then model the pseudo-random behaviour of a train track based on the poisson distribution that is generated from the inputs.

Instance Variables:

- self.L0: stores a dictionary that is used for generating weighted random values for the duration between trains
- self.L1: stores a dictionary that is used for generating weighted random values for the duration of the train on the track
- self.hasTrain (BOOLEAN): self-explanatory
- self.isWaiting (BOOLEAN): the inverse of the above
- self.trackOccupancy: a list of numbers either 0 or 1 that depicts the behaviour of the train track. The index corresponds to the game second, and 1 means there is a train on it, 0 means there isnt.

 ## API

 ### getTimeBetweenTrains(self):
method for determining a weighted random number to be used as the time between trains for an instance of traintrack simulation 


 ### getHowLong(self):
method for determining a weighted random number to be used as the length of the trains for an instance of traintrack simulation


 ### simulate (TRAINTRACK self, INT duration):
 method that updates and returns the traintracks trackOccupancy list for a given number of seconds ie. game duration.