'''
Created on Sep 28, 2016

@author: Varun
'''
import random
import math

class ArmStats(object):
    
    def __init__(self, armId):
        self.armId = armId
        self.cumReward = 0
        self.armRunCount = 0
        self.ucbIndex = 0
        
    def rewardMean(self):
        return self.cumReward/self.numberOfRuns
    
    def addReward(self, currReward):
        self.cumReward = self.cumReward + currReward
        
    def incrementArmRunCount(self):
        self.armRunCount = self.armRunCount+1
        
    def calculateUCB1Index(self, totalCount):
        self.ucbIndex = self.rewardMean() + math.sqrt((2 * math.log(totalCount)/self.armRunCount))
        return self.ucbIndex

class Algo(object):
    '''
        Each instance for a context. This class encapsulates the logic of algorithm per context
    '''


    def __init__(self, listOfArms, dictOfUserId2Artists, randomOrder):
        '''
        Constructor
        '''
        self.listOfArms = listOfArms
        self.dictOfUserId2Artists = dictOfUserId2Artists
        self.totalRuns = 0
        self.randomOrder = randomOrder
        self.listOfArmStats = []
        
       
    def run(self, userId):
            #Select all arms in random order
            if self.totalRuns <= len(self.listOfArms):
                selectedArm = self.listOfArms[self.randomOrder[self.totalRuns]]
                #Check if for this context the selected artists song has ever been played.
                #If played reward 1 else 0
                currReward = 1 if selectedArm in self.dictOfUserId2Artists[userId] else 0
                stats = ArmStats(selectedArm)
                stats.addReward(currReward)
                stats.incrementArmRunCount()
                self.listOfArmStats.append(stats)
            else:
                #Select the arm which maximizes the reward.
                # Step1. Calculate Index based on current total Runs
                maxIndex = max([armStat.calculateUCB1Index(self.totalRuns) for armStat in self.listOfArmStats])
                #Step2. Select the arm with this maxIndex
                maxIndexArmList = filter(lambda armstat: armstat.ucbIndex == maxIndex, self.listOfArmStats)
                randomMaxArm = random.sample(xrange(len(maxIndexArmList)), 1)
                #Step3. Get Reward for this Arm
                currReward = 1 if randomMaxArm in self.dictOfUserId2Artists[userId] else 0
                #Step4. Update Arm Stats
                randomMaxArm.addReward(currReward)
                randomMaxArm.incrementArmRunCount()
                
            self.totalRuns = self.totalRuns + 1
    
