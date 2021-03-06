# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:59:22 2020

Code Names Module - Text Edition

Graphical edition will come soon once I learn how to use pygame....

To do:
    - Document code
    - Put together building blocks to make the game!
    - Interface keycard with constructRandomWordGrid. (make back of word cards equal to corresponding keycard value)
    

@author: Adriel Kim
"""

from GameBoardClass import GameGrid as grid
from CardClass import Card
from random import sample
from random import randint
import GameRoundManager as gm
import csv
import numpy as np
import copy


def getWords(wordsFile):
    results = []
    
    with open(wordsFile) as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # each row is a list
            for word in row:
                if(word!= ''):
                    results.append(word)
    return results
            
"""
Constructs a grid (matrix) of random words of a given dimension (dims). Words are from a list (wordsList)
The objects of this grid are of the Card object.
"""
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
"""
Returns a list of adjacent values relative to a point on a grid
(NOT USED)
"""
def getAdjacentValues(grid, index):
    adjacents = []
    gridDimR = grid.shape[0]
    gridDimC = grid.shape[1]
    row = index[0]
    col = index[1]
    
    if(row+1 < gridDimR):
        adjacents.append((row+1, col))
        if((col+1)<gridDimC):
            adjacents.append((row+1, col))
    if(row-1 >= 0):
        adjacents.append((row-1,col))
        if(col+1<gridDimC):
            adjacents.append((row-1,col+1))
    if(col+1 < gridDimC):
        adjacents.append((row, col+1))
    if(col-1 >= 0):
        adjacents.append((row, col-1))
        if(row+1<gridDimR):
            adjacents.append((row+1, col-1))
        if(row-1 >=0):
            adjacents.append((row-1,col-1))
            
    return adjacents
    
    
def getGridDims(grid):
    return grid.get_size()[0], grid.get_size()[1]

"""
Game notes: One team contains 8 agents/spots on keycard. The other team has 9 agents/spots. And there is 1 deadly assassin card spot
All other guards will be a wrong guess!
"""
def constructKeyCard(dims, rSpots, bSpots, aSpots):
    arraySize = dims[0] * dims[1]
    keyCard = np.full(arraySize, "Wrong_Guess")
    
    #I suppose this is returnign a list of random indices. First paramter is range of of indices. size is number of elements.
    #replace determines whether we're sampling with replacement or not. replace = False means no duplicates(no replacement)
    randomIndices = list(np.random.choice(np.arange(arraySize), replace = False,
                                     size = rSpots + bSpots + aSpots))

    redIndices = randomIndices[:rSpots]
    blueIndices = randomIndices[rSpots:(rSpots+bSpots)]
    assassinIndices = randomIndices[-1]
    keyCard[redIndices] = 'Red_Agent'
    keyCard[blueIndices]  = 'Blue_Agent'
    keyCard[assassinIndices] = "Assassin"
    keyCard = keyCard.reshape(dims[0],dims[1])
    return keyCard
    
def setCardGridBacking(wordGrid, keyCard):
    dimX, dimY = getGridDims(wordGrid)
    newBoard = copy.deepcopy(wordGrid)
    
    board = newBoard.get_board()
    for i in range(0, dimX):
        for k in range(0, dimY):
            board[i][k].setBack(keyCard[i][k])
    
    return newBoard

def flipAllCards(wordsGrid):
    dimX, dimY = getGridDims(wordGrid)
    for i in range(0, dimX):
        for k in range(0, dimY):
            wordsGrid.flip_card(i,k)#flips card at specifc index

def getUniqueCounts(matrix):
    return np.unique(matrix, return_counts = True)

def getKeyCardCounts(keyCard):
    unique, counts = getUniqueCounts(keyCard)
    #the counts are in the following order: Assassin, Blue_Agent, Red_Agent, Wrong_Guess
    return counts[0], counts[1], counts[2], counts[3], unique

"""
There are 2 code masters. The code masters give clues to their teammates as to what words to choose.
The more words their clues encompass, the better. The code masters must also tell exactly how many words their
clue encompasses. Their goal is to match the key card for their respective team before the other team does.

Teams get to keep going until either all words are selected or they choose a wrong card. I believe teams can also make a random
guess if they so choose after selecting all the cards correctly.

If an assassin card is chose, then the team that choses automatically loses. There is only 1 assassin card.


Pseudo Implementation:
    while both teams have all their cards and no one has chosen assassin
        code master turn. tell code master to come up with a clue for X amount of words
        ask code master to select card (row and col)
        card is flipped
        if card is assassin, output opposing team as winner
        if card is valid, then loop for another turn 
        if card is wrong, then next code master's turn
        code master can choose to pass
        if card is last one for that team, then code master wins
        
To Do:
    implement the game itself according to the rules above. Use GameRoundManager module to help you. (DONE)
    Test for bugs, play test.
    Then, start working on the UI layer for all these things. This requires careful planning. (Flask integration for web app usage.)***
"""
def PlayCodeNames(master1, master2, wordGrid, keyCard):
    #Player set up
    players = [master1, master2]
    firstMaster = gm.decideFirst(players)
    players.remove(firstMaster)
    secondMaster = players[0]
    #Board and keycard setup
    displayBoard = setCardGridBacking(wordGrid, keyCard)#For display purposes only
    assinCount, blueCount, redCount, wrongCount, uniqueList = getKeyCardCounts(keyCard)
    currentMaster = firstMaster
    """
    print(firstMaster)
    print(secondMaster)
    print("%d, %d, %d, %d" % (assinCount, blueCount, redCount, wrongCount))
    """
    print("Key Card:")
    print(keyCard,'\n')

    while(blueCount > 0 and redCount > 0 and assinCount > 0):
        #displayBoard.printboard()
        gm.displayBoard(displayBoard)
        print("%s's turn! Come up with a clue and select a card!" % (currentMaster.getName()))
        print("Card row: ")
        row = int(input())
        print("Card column: ")
        col = int(input())
        
        keyCardElem = keyCard[row][col]
        
        if(keyCardElem == uniqueList[0]):
            assinCount -= 1;
        elif(keyCardElem == uniqueList[1]):
            blueCount -= 1;
        elif(keyCardElem == uniqueList[2]):
            redCount -= 1;
        
        displayBoard.flip_card(row, col)
        #displayBoard.printboard()
        gm.displayBoard(displayBoard)
        if(blueCount == 0 or redCount == 0):
            gm.congratulateWinner(currentMaster)
        
        if (currentMaster == firstMaster):
            currentMaster =  secondMaster
        else:
            currentMaster = firstMaster

        if(assinCount == 0):
            gm.congratulateWinner(currentMaster)
        print("____________________________________________________________________________________")
        

#Setting up the word grid
allWords = getWords("CodenamesWordList.csv")+getWords("CodenamesWordList2.csv")
wordGrid = constructRandomWordGrid((5,5), allWords)
print(wordGrid)
wordGrid.printboard()

#Setting up the key card
keyCard = constructKeyCard((5,5),8, 9, 1)
"""
print(keyCard)
unique, counts = getUniqueCounts(keyCard)
print(counts)
print(unique)

#Setting the key card as the back of respective cards of the word grid
newBoard = setCardGridBacking(wordGrid, keyCard)
flipAllCards(newBoard)
newBoard.printboard()#The keycard backing.
flipAllCards(newBoard)#flipping back for game
newBoard.printboard()
"""
master1 = gm.playerSetUp("Red")
master2 = gm.playerSetUp("Blue")
PlayCodeNames(master1, master2, wordGrid, keyCard)




