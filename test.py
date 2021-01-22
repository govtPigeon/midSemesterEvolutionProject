from matplotlib import pyplot as plt
import pandas as pd
import statistics as stats
import random
import re
import sys
import io

def crossover(choiceList, evalParents, halfIndex, endIndex, currentParentList, newParents):
    newParentsTemp = []
    tempParents = []
    pathComplete = []
    badChoice = []
    badChoiceIndex = []
    parentsGenerated = 0
    pick = random.randrange(1, 3)
    mutate = random.randrange(0, 11)

    # cross first half of first parent with second half of second parent
    cross = str(evalParents[currentParentList][0:halfIndex+1]) + str(evalParents[currentParentList+1][halfIndex+1:endIndex+2])
    cross = (cross.strip('[').strip(']').replace('][', ', '))
    cross = cross.split(',')
    firstHalf = [int(i.strip()) for i in cross[1:halfIndex+1]]
    secondHalf = [int(i.strip()) for i in cross[halfIndex+1:-1]]

    if pick == 1:
        for i in firstHalf:
            badChoice.append(int(i))
            if i in secondHalf:
                badChoiceIndex.append(firstHalf.index(int(i)))
        for i in secondHalf:
            if i not in badChoice:
                badChoice.append(i)
        cleanGenes = [i for i in choiceList if i not in badChoice]
        for i in badChoiceIndex:
            choice = random.choice(cleanGenes)
            firstHalf[i] = choice
            cleanGenes.remove(choice)
        parent = str(cleanGenes[0]) + str(firstHalf) + str(secondHalf) + str(cleanGenes[0])
        newParentsTemp.append(parent)
    elif pick == 2:
        for i in secondHalf:
            badChoice.append(int(i))
            if i in firstHalf:
                badChoiceIndex.append(secondHalf.index(int(i)))
        for i in firstHalf:
            if i not in badChoice:
                badChoice.append(i)
        cleanGenes = [i for i in choiceList if i not in badChoice]
        for i in badChoiceIndex:
            choice = random.choice(cleanGenes)
            secondHalf[i] = choice
            cleanGenes.remove(choice)
        parent = str(cleanGenes[0]) + str(firstHalf) + str(secondHalf) + str(cleanGenes[0])
        newParentsTemp.append(parent)
    _ = 0
    for i in newParentsTemp:
        newParentsTemp[_] = re.split('[][]|,', i)
        _ += 1
    for i in newParentsTemp:
        for j in i:
            if j != '':
                tempParents.append(int(j))
        newParents.append(tempParents.copy())
        newParentsTemp.clear()
        tempParents.clear()
    parentsGenerated += 1

    # cross first half of second parent with second half of first parent
    cross = str(evalParents[currentParentList + 1][0:halfIndex + 1]) + str(evalParents[currentParentList][halfIndex + 1:endIndex + 2])
    cross = (cross.strip('[').strip(']').replace('][', ', '))
    cross = cross.split(',')
    # pathComplete.append(cross[0])
    # pathComplete.append(cross[-1])
    firstHalf = [int(i.strip()) for i in cross[1:halfIndex + 1]]
    secondHalf = [int(i.strip()) for i in cross[halfIndex + 1:-1]]

    badChoice = []
    badChoiceIndex = []
    # 50% chance to alter first half.. 50% to alter second half. if pick is 1, alter first half to maintain path validity. if pick is 2, alter second half to maintain path validity.
    if len(newParents) == len(evalParents):
        return newParents
    if pick == 1:
        for i in firstHalf:
            badChoice.append(int(i))
            if i in secondHalf:
                badChoiceIndex.append(firstHalf.index(int(i)))
        for i in secondHalf:
            if i not in badChoice:
                badChoice.append(i)
        #cleanGenes always generates our good gene choices for whatever we're trying to fill. could be start/end of the tour or a mutation.
        cleanGenes = [i for i in choiceList if i not in badChoice]
        for i in badChoiceIndex:
            choice = random.choice(cleanGenes)
            firstHalf[i] = choice
            cleanGenes.remove(choice)
        # parent = str(cleanGenes[0]) + str(firstHalf) + str(secondHalf) + str(cleanGenes[0])
        if mutate > 3:
            firstHalf[random.randrange(0, len(firstHalf))] = cleanGenes[0]
        cleanGenes.clear()
        cleanGenes = choiceList.copy()
        for i in firstHalf:
            cleanGenes.remove(i)
        for j in secondHalf:
            cleanGenes.remove(j)
        parent = str(cleanGenes[0]) + str(firstHalf) + str(secondHalf) + str(cleanGenes[0])
        newParentsTemp.append(parent)
    elif pick == 2:
        for i in secondHalf:
            badChoice.append(int(i))
            if i in firstHalf:
                badChoiceIndex.append(secondHalf.index(int(i)))
        for i in firstHalf:
            if i not in badChoice:
                badChoice.append(i)
        cleanGenes = [i for i in choiceList if i not in badChoice]
        for i in badChoiceIndex:
            choice = random.choice(cleanGenes)
            secondHalf[i] = choice
            cleanGenes.remove(choice)
        #parent = str(cleanGenes[0]) + str(firstHalf) + str(secondHalf) + str(cleanGenes[0])
        if mutate > 3:
            secondHalf[random.randrange(0, len(secondHalf))] = cleanGenes[0]
        cleanGenes = choiceList.copy()
        for i in firstHalf:
            cleanGenes.remove(i)
        for j in secondHalf:
            cleanGenes.remove(j)
        parent = str(cleanGenes[0]) + str(firstHalf) + str(secondHalf) + str(cleanGenes[0])
        newParentsTemp.append(parent)
    _ = 0
    for i in newParentsTemp:
        newParentsTemp[_] = re.split('[][]|,', i)
        _ += 1
    for i in newParentsTemp:
        for j in i:
            if j != '':
                tempParents.append(int(j))
        newParents.append(tempParents.copy())
        newParentsTemp.clear()
        tempParents.clear()

    return newParents

def main():
    #----------------#
    random.seed()
    mutate = random.randrange(1, 10)
    #----------------#
    #looking for this line to start reading coordinates
    node_line = 'NODE_COORD_SECTION\n'
    end_nodes = 'TOUR_SECTION\n'
    coordList = []
    csv_lines = []
    results = []
    endRowCheck = 0
    #read file and clean whitespace via tokenization
    with open('intercityCosts17.txt', 'r') as cityCost:
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
    #select initial population
    visitedList = []
    parents = []
    costList = []
    column = 0
    _ = 0
    i = 1
    #pick min in each column to generate initial parents. generates # of cities parents. checks to make sure move has not already been made.
    while _ < len(df):
        colCount = column
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
        visitedList.append(colCount)
        dfSmall = pd.Series(df[column])
        tempCost.append(dfSmall[colCount])
        parents.append(visitedList)
        costList.append(tempCost)
        visitedList = []
        column = colCount + 1
        _ = countHold + 1

    costSum = [sum(i) for i in costList]
    _ = 0
    for i in parents:
        print('path: ' + str(i) + ' cost: ' + str(costSum[_]))
        _ += 1

    costStdDev = stats.stdev(costSum) + stats.stdev(costSum)/2
    print(costStdDev)
    print(str(min(costSum)) + '\n')
    costMin = min(costSum)
    evalCost = []
    #didn't want to change all variable names for evalParents. lazy but..............
    evalParents = parents.copy()
    _ = 0
    print("::PRE::")
    for i in evalParents:
        print('path: ' + str(i))# + ' cost: ' + str(evalCost[_]))
        _ += 1
    #fitness = [abs(costMin - i) for i in evalCost]
    #print(fitness)

    gens = 0
    tempCostList = []
    while gens < 300:
        newParents = []
        currentParentList = 0
        #perform crossover USE A FUNCTION HERE
        while len(newParents) < len(evalParents):
            #crossover function also mutates with 70% chance
            crossover(choiceList, evalParents, halfIndex, endIndex, currentParentList, newParents)
            currentParentList += 1
        #evalParents = newParents.copy()
        print("::CROSSOVER::MUTATION::")

        #while pIndex < colCount + 1:
        costList.clear()
        for i in newParents:
            tempCost.clear()
            pIndex = 1
            for move in i:
                dfSmall = pd.Series(df[i[pIndex]])
                tempCost.append(dfSmall[move])
                pIndex += 1
                if pIndex == colCount + 2:
                    pIndex = 0
                    break
            costList.append(tempCost.copy())
        _ = 0
        for i in newParents:
            costSum = sum(costList[_])
            tempCostList.append(costSum)
            print('path: ' + str(i) + ' cost: ' + str(costSum))
            _ += 1
            if costSum == 33523:
                input()
        gens += 1

    print("here")
    print(min(tempCostList))
    print()
main()



#extra trash

# for i in costSum:
#     if(i - costMin < costStdDev):
#         evalParents.append(parents[parentIndex])
#         evalCost.append(costSum[parentIndex])
#     parentIndex += 1
# pruned parents
