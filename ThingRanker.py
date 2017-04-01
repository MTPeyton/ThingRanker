__author__ = 'Matt'

intro = "Please type the name of the file of strings to be ranked, then hit enter.\nEach string must be on a new line."

print(intro)

fileName = input("File Name: ")

with open(fileName) as f:
    numLines = sum(1 for _ in f)

inputList = [None] * numLines

f = open(fileName, 'r')

for line in f:
    inputList.append(line)

for len in inputList:
    print(inputList[len])