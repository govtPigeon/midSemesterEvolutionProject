from matplotlib import pyplot as plt
import pandas as pd
import statistics as stats
import random
import re
import sys
import io

#looking for this line to start reading coordinates
node_line = 'NODE_COORD_SECTION\n'
end_nodes = 'TOUR_SECTION\n'
coordList = []
csv_lines = []
results = []
endRowCheck = 0
random.seed()
#read file and clean whitespace via tokenization
with open('intercityCosts5.txt', 'r') as cityCost:
    lines = cityCost.readlines()
    endIndex = len(lines) - 1
    halfIndex = int(endIndex/2)
    for line in lines:
        csv_lines.append(line.split())

choiceList = [i for i in range(0, endIndex+1)]
#convert lines(strings) to integers
for line in csv_lines:
    results.append(list(map(float, line)))
df = pd.DataFrame(results)
print(df)

# grab coordinates from list
# xCoords = [float(coordSet[1]) for coordSet in coordList]
# yCoords = [float(coordSet[2]) for coordSet in coordList]
# print(xCoords)
# print(yCoords)
#print(df.shape[0])
# dfSmall = pd.Series(df[0])
# #print(dfSmall)
# dfSmall = dfSmall.nsmallest(len(dfSmall))
#plt.plot(xCoords, yCoords, '.')
#plt.show()

#select initial population
visitedList = []
parents = []
costList = []
column = 0
_ = 0
i = 1
#pick min in each column to generate initial parents. generates # of cities parents. checks to make sure move has not already been made.
while _ < len(df):
    colHold = column
    visitedList.append(column)
    countHold = _
    tempCost = []
    _ = 0
    while _ < len(df) - 1:
        dfSmall = pd.Series(df[column])
        dfSmall = dfSmall.nsmallest(len(dfSmall))
        smallIndexList = dfSmall.index.tolist()
        selectMove = smallIndexList[i]
        if selectMove in visitedList:
            while selectMove in visitedList:
                i += 1
                selectMove = smallIndexList[i]
        visitedList.append(selectMove)
        tempCost.append(dfSmall[selectMove])
        i = 1
        _ += 1
        column = selectMove
    visitedList.append(colHold)
    dfSmall = pd.Series(df[column])
    tempCost.append(dfSmall[colHold])
    parents.append(visitedList)
    costList.append(tempCost)
    visitedList = []
    column = colHold + 1
    _ = countHold + 1

dfSmall = pd.Series(df[selectMove])
costSum = [sum(i) for i in costList]
_ = 0
for i in parents:
    print('path: ' + str(i) + ' cost: ' + str(costSum[_]))
    _ += 1

costStdDev = stats.stdev(costSum) + stats.stdev(costSum)/2
print(costStdDev)
print(str(min(costSum)) + '\n')
costMin = min(costSum)
#prune 'bad parents'. parents are bad if their cost - the minimum cost is greater than the stdDev + stdDev/2 (taking stdDev of the cost of all paths)
evalParents = []
parentIndex = 0
evalCost = []
for i in costSum:
    if(i - costMin < costStdDev):
        evalParents.append(parents[parentIndex])
        evalCost.append(costSum[parentIndex])
    parentIndex += 1
#pruned parents
_ = 0
for i in evalParents:
    print('path: ' + str(i) + ' cost: ' + str(evalCost[_]))
    _ += 1
#evalute pruned parents
fitness = [abs(costMin - i) for i in evalCost]
print(fitness)

#perform crossover
test = str(evalParents[0][1:halfIndex+1]) + str(evalParents[1][halfIndex+1:endIndex+1])
test1 = (test.strip('[').strip(']').replace('][', ', '))
test1 = test1.split(',')

#generate gene choices. swap repeats in secondHalf list for gene choices. the purpose of this is to "clean" the crossed over parents. when crossed, there will be repeat values. this removes those.
gens = 0
firstHalf = [int(i.strip()) for i in test1[:halfIndex]]
secondHalf = [int(i.strip()) for i in test1[halfIndex:]]
seenList = firstHalf
potentParent = firstHalf + secondHalf
indexRepeat = [secondHalf.index(i) for i in secondHalf if i in firstHalf]
geneChoices = [int(i) for i in choiceList if i not in potentParent]
cleanParentMinCost = []
_ = 0
for i in geneChoices:
    cleanParentMinCost.append(pd.Series(df[geneChoices[_]][firstHalf[0]]))
    _ += 1
cleanParentMinCost = [int(j) for i in cleanParentMinCost for j in i]
saveGeneIndex = cleanParentMinCost.index(min(cleanParentMinCost))
saveGene = [geneChoices[saveGeneIndex]]
geneChoices.pop(saveGeneIndex)
for i in indexRepeat:
    secondHalf[i] = random.choice(geneChoices)

newParent = saveGene + firstHalf + secondHalf + saveGene
print(newParent)

# test code to visualize matplotlib plotting
# point1 = [1,1]
# point2 = [1,3]
# point3 = [3,1]
#
# x_values = [point1[0], point2[0], point3[0], point1[0]]
# y_values = [point1[1], point2[1], point3[1], point1[0]]
# plt.plot(x_values, y_values)

#plt.show()