'''
Created on Sep 25, 2016

@author: Varun

'''
import random
from ucb.algo import Algo

def partitionContexts():
    listOfContextPartitions = []
    listOfUsers = []
    f = open("C:\\UCLA MS\\EE238\\lastfm-dataset-1K\\userid-profile.tsv")
    for line in f:
        if line.find("#id") >= 0:
            continue
        userInfo = line.split("\t")
        if userInfo[1] is None or "" == userInfo[1]:
            userInfo[1] = 'm'
        if userInfo[2] is None or "" == userInfo[2]:
            userInfo[2] = 'UnSpecified'
        if userInfo[3] is None or "" == userInfo[3]:
            userInfo[3] = 'United States'
        userContext = userInfo[1], userInfo[2], userInfo[3]
        
        listOfUsers.append((userInfo[0],userInfo[1], userInfo[2], userInfo[3]))
        listOfContextPartitions.append(userContext)
    
    listOfContextPartitions = list(set(listOfContextPartitions))
    print "Number of Contexts"
    print len(listOfContextPartitions)
    print "Number of Users"
    print len(listOfUsers)
    return listOfUsers,listOfContextPartitions



def extractArms():
    userSelectionsFile = open("C:\\UCLA MS\\EE238\\lastfm-dataset-1K\\userid-timestamp-artid-artname-traid-traname.tsv")
    dictOfArtistToSongs = {}
    dictOfUserId2Artist = {}
    listOfUsersListened = []
    for line in userSelectionsFile:
        userSelRec = line.split("\t")
        userId = userSelRec[0]
        artist = userSelRec[3]
        song = userSelRec[5]
        listOfUsersListened.append(userId)
        if dictOfArtistToSongs.get(artist) is None:
            dictOfArtistToSongs[artist] = [song]
        else:
            existingSongList = dictOfArtistToSongs[artist]
            existingSongList.append(song)
            #dictOfArtistToSongs[artist] = list(set(existingSongList))
            
        if dictOfUserId2Artist.get(userId) is None:
            dictOfUserId2Artist[userId] = [artist]
        else:
            existingArtistList = dictOfUserId2Artist[userId]
            existingArtistList.append(song)
            #dictOfUserId2Artist[artist] = list(set(existingArtistList))
    
    print "Number of Arms"
    print len(dictOfArtistToSongs.keys())
    print len(listOfUsersListened)
    return dictOfArtistToSongs, dictOfUserId2Artist


def runUCB1Algo(listOfUsers, listOfContexts, dictOfArtists2Songs, dictOfUserId2Artists):
    dictOfContext2AlgoRuns = {}
    for context in listOfContexts:
        randomSelOrder = random.sample(xrange(len(dictOfArtists2Songs.keys())), len(dictOfArtists2Songs.keys()))
        algoForContext = Algo(dictOfArtists2Songs.keys(),dictOfUserId2Artists, randomSelOrder)
        dictOfContext2AlgoRuns[context] = algoForContext
    
    #Run the algo for each context 50000 times
    totalRunsOfAlgo = 1000000 
    randomUserSelOrder = random.sample(xrange(len(listOfUsers)), len(listOfUsers))
    userSelIndex = 0
    for i in xrange(0, totalRunsOfAlgo):
        if (i!=0 and (i % len(listOfUsers) == 0)):
            #Change random order of users
            userSelIndex = 0
            randomUserSelOrder = random.sample(xrange(len(listOfUsers)), len(listOfUsers))
        selectedUser = listOfUsers[randomUserSelOrder[userSelIndex]]
        selectedUserContext = selectedUser[1:]
        #TODO Chnage the randomorder after number of runs exceeds the arms number
        dictOfContext2AlgoRuns[selectedUserContext].run(selectedUser[0])
        
        


if __name__ == '__main__':
    '''
        Reading User Profile File for available contexts and
        storing as a dict and assigning partitions

    Context Partitions lists with tuple of Gender,Country,Age
    '''
    listOfUsers, listOfContexts = partitionContexts()
    dictOfArtists2Songs, dictOfUserId2Artists = extractArms()
    runUCB1Algo(listOfUsers, listOfContexts, dictOfArtists2Songs, dictOfUserId2Artists)
    
            
    