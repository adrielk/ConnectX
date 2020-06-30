# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:59:22 2020

Code Names - Text Edition

Graphical edition will come soon once I learn how to use pygame....

@author: Adriel Kim
"""

from GameBoardClass import GameGrid as grid
from CardClass import Card
from random import sample
from random import randint
import GameRoundManager as gm
import csv
import numpy as np


def getWords(wordsFile):
    results = []
    
    with open(wordsFile) as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # each row is a list
            for word in row:
                if(word!= ''):
                    results.append(word)
    return results
            
def constructRandomWordGrid(dims, wordsList):
    dimX = dims[0]
    dimY = dims[1]
    #randomly sample words for grid
    randWords = sample(wordsList, int(dimX*dimY))
        
    wordMatrix = grid(dimX, dimY, randWords)#np.array(gridCards).reshape((dimX, dimY))  
    for i in range(dimX):
        for k in range(dimY):
            word = randWords[(i*dimX)+k]
            newCard = Card(front = word, back = word)
            wordMatrix.insert_piece(newCard, (i,k))
            
    return wordMatrix

#returns a list of all combinations of row and column tuples of a grid
#Note: is there a way to vectorize this?
def generateAllIndices(grid):
    indices = []
    for r in range(0, grid.shape[0]):
        for c in range(0, grid.shape[1]):
            indices.append((r,c))
    return indices

def getAdjacentValues(grid, index):
    adjacents = []
    gridDimR = grid.shape[0]
    gridDimC = grid.shape[1]
    row = index[0]
    col = index[1]
    
    if(row+1 < gridDimR):
        adjacents.append(grid[row+1, col])
        if((col+1)<gridDimC):
            adjacents.append(grid[row+1, col])
    if(row-1 >= 0):
        adjacents.append(grid[row-1,col])
        if(col+1<gridDimC):
            adjacents.append(grid[row-1,col+1])
    if(col+1 < gridDimC):
        adjacents.append(grid[row, col+1])
    if(col-1 >= 0):
        adjacents.append(grid[row, col-1])
        if(row+1<gridDimR):
            adjacents.append(grid[row+1, col-1])
        if(row-1 >=0):
            adjacents.append(grid[row-1,col-1])
            
    return adjacents
    
    
            
"""
Game notes: One team contains 8 agents/spots on keycard. The other team has 9 agents/spots. And there is 1 deadly assassin card spot
Maybe a better implementaiton would be making the back of each gard be the agent...! All other guards will be a wrong guess!

There will be certain probabilities of clustering. a clustering of 2 will have a high chance, 3 will have a lower chance, and 4 
will have an even lower chance. A clustering of 1 has hte lowest chance.

OR probability of being red is based on number of red adjacent
"""
def constructKeyCard(dims, rSpots, bSpots, rProb, bProb):
    keyCard = np.full((dims[0],dims[1]), "Wrong_Guess")
    possibleIndices = generateAllIndices(keyCard)
    
    
    for i in range(0, rSpots):
        randIndex = randint(0, len(possibleIndices)-1)
        randRow = possibleIndices[randIndex][0]
        randCol = possibleIndices[randIndex][1]
        
       #adjacents = getAdjacentValues(keyCard, randIndex)
        keyCard[randRow, randCol] = "Red_Agent"
        
        possibleIndices.remove(possibleIndices[randIndex])
        
    for i in range(0, bSpots):
        randIndex = randint(0, len(possibleIndices)-1)
        randRow = possibleIndices[randIndex][0]
        randCol = possibleIndices[randIndex][1]
        
        keyCard[randRow, randCol] = "Blue_Agent"
        
        possibleIndices.remove(possibleIndices[randIndex])
    
    randIndex = randint(0, len(possibleIndices)-1)
    randRow = possibleIndices[randIndex][0]
    randCol = possibleIndices[randIndex][1] 
    keyCard[randRow, randCol] = "Assassin"
    return keyCard
    


allWords = getWords("CodenamesWordList.csv")+getWords("CodenamesWordList2.csv")
wordGrid = constructRandomWordGrid((5,5), allWords)
print(wordGrid)
wordGrid.printboard()

keyCard = constructKeyCard((5,5),8, 9, 0.7,0.7)
print(keyCard)