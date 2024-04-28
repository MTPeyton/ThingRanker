__author__ = 'Matthew Peyton'
import random
from math import trunc

intro = "Please type the name of the file of strings to be ranked, then hit enter.\nThe file should be a CSV of strings,initial ELO scores."
print(intro)

fileName = input("File Name: ")

with open(fileName) as f:
    inputList = f.readlines()

f.close()

inputPairs = [x.strip().split(',') for x in inputList]

#-------------------------------------------------------------------------------------------
class RankedItems:
    rankItemPairs = {}
    K = None

    def __init__(self, initialPairs):
        self.K = 50
        self.rankItemPairs = {}
        for k, v in initialPairs:
            if not v:
                v = 2000
            self.rankItemPairs[k] = int(v)

    def randmatch(self):
        item1 = random.choice(list(self.rankItemPairs.keys()))
        item2 = random.choice(list(self.rankItemPairs.keys()))
        while item1 == item2:
            item2 = random.choice(list(self.rankItemPairs.keys()))

        originalR1 = self.rankItemPairs[item1]
        originalR2 = self.rankItemPairs[item2]

        transformedR1 = 10**(originalR1 / 400)
        transformedR2 = 10**(originalR2 / 400)

        expectedR1 = transformedR1 / (transformedR1 + transformedR2)
        expectedR2 = transformedR2 / (transformedR1 + transformedR2)

        #Here is where you present the player with the choices and ask them to choose one
        print("\n" + item1 +" vs. "+ item2)
        choosing = True
        while choosing == True:
            choice = input("Type 1 or 2 to choose the winner, 3 if draw: ")
            if choice == "1":
                score1 = 1
                score2 = 0
                choosing = False
            elif choice == "2":
                score1 = 0
                score2 = 1
                choosing = False
            elif choice == "3":
                score1 = 0.5
                score2 = 0.5
                choosing = False

        newR1 = originalR1 + (self.K * (score1 - expectedR1))
        newR2 = originalR2 + (self.K * (score2 - expectedR2))

        self.rankItemPairs[item1] = newR1
        self.rankItemPairs[item2] = newR2

    def printranks(self):
        d = self.rankItemPairs

        print("\nCurrent Ranks:")
        s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
        for k, v in s:
            print("{:d}".format(trunc(v)), k)

    def writeresults(self,oFile):
        d = self.rankItemPairs
        f2 = open(oFile.strip('.csv') + "results.csv", "w")

        s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
        for k, v in s:
            outstring = k + "," + "{:d}".format(trunc(v)) + "\n"
            f2.write(outstring)
        f2.close()
#--------------------------------------------------------------------------------------------

ranker = RankedItems(inputPairs)

ranker.printranks()

ranking = True

while ranking == True:
    matchNum = input("Enter how many matches to run (0 to exit): ")
    matchNum = int(matchNum)

    if matchNum == 0:
        ranking = False
        ranker.writeresults(fileName)
    else:
        for i in range(0, matchNum):
            ranker.randmatch()
        ranker.printranks()