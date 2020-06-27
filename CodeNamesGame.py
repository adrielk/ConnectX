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


allWords = getWords("CodenamesWordList.csv")+getWords("CodenamesWordList2.csv")
wordGrid = constructRandomWordGrid((5,5), allWords)
print(wordGrid)
wordGrid.printboard()