import math
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