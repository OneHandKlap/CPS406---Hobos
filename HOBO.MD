# Hobo Class
## Brief overview of Hobos

Hobos are datastructures that store and use track information to model the behavioural pattern that describes them. There are 5 "levels" of Hobo 0-4. Each is characterized by a different method by which it decides to move to another track.

Instance Variables:

- self.HP: pretty self-explanatory, this just represents the total number of times that the Hobo may be hit before the game ends. This number was arbitrarily set.
-self.info: This 2d array represents two time slices of TrainTrack information. The first array, info[0] represents what the Hobo sees as the state of the train tracks right now, and is gather by him "looking around." The second array, info[1] represents what the traintracks will be in the following second. The only way in which this array is populated is by the paper plane, which may or may not be accurate (the veracity rating was arbitrarily set to 60%)
-self.runningResults: This 2d array represents the hobos memories of trains that have passed. As long as a track's state has not changed (ie. it stays empty or stays full) a 1 or 0 will be appended to the list at the index that corresponds with the track number. When the state does change, that index is replaced by the new value. In this way the hobo is remarking the duration of particular states and can use it to calculate runningL0 and L1 values
-self.runningL0 & self.running L1: These lists use values from running results in order to compute what the hobo determines is the likely value based on the train tracks behaviour up until this point
self.positionHistory: a list of all the track numbers that the hobo has been on for the duration of the game

 ## API

 ### init (self)
Initializing a Hobo creates a blank slate to act with. At first we incorporated the ability to add generative learning to Hobos, by allowing it to take in the runningResults from previous generations, however this idea was left behind.

 ### act (self, INT smartness)
This method is the heart of the hobo class. Passing in an int determines the behavioural profile that will be used to act.

0-Totally random choice
1-First empty track
2-First empty track, if no empty tracks then use paper plane
3-First empty track, if no empty tracks then use math
4-Use math

Returns nothing, merely updates Hobo's current position.

 ### updateResults (self)
 
 This method runs after every game second, and is what the Hobo does in order to update his memory of the tracks, and to gather information on what the L0 and L1 values might be given the behaviour of those tracks

Returns nothing merely updates Hobo's runningResults/runningL0/runningL1

  ### doMaths (self)

  This method returns a list of "safeness scores" representing the liklihood that the track will be empty next turn. This is accomplished by using the runningL0 and runningL1 values to generate poisson distribution values, and based on how long each track has been in its current state generates the likelihood that it will either remain empty or become empty in the next second.

  It returns a list of doubles.