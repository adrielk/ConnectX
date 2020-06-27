# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:44:20 2020

@author: Adriel Kim

"""
from GamePieceClass import GamePiece as gp
from PlayerClass import Player as plr
from random import randint
import numpy as np

def playerSetUp(teamNum):
    print("Enter name for player "+str(teamNum))
    pName = input()
    playerPieces = [gp(teamNum)]
    return plr(pName, teamNum, playerPieces) 

def decideFirst(players):
    print("Flipping "+str(len(players))+" sided coin")
    result = randint(0, len(players)-1)
    firstPlayer = players[result]
    firstPlayer.makeFirst()
    print(str(firstPlayer.getName())+" goes first!")
    return firstPlayer

def playerTurn(grid, playerPiece, rowMatters = True):
    row1 = 0
    if rowMatters:
        print("Enter row")
        row1 = int(input())
    print("Enter column")
    col1 = int(input())
    grid.insert_piece(playerPiece, (row1, col1))
    
    """
Takes in a grid and finds game piece part of a sequence
Assumptions: There exists only 1 sequence in the grid
"""
def getSequenceOwner(grid, length):
    #amtrix representing grid
    rawGrid = grid.get_board()
    #grid sequence vars
    seq = grid.findsequences(length)[0]
    startPoint = seq[1]
    startR = startPoint[0]
    startC = startPoint[1]
    #a gamePiece part of sequence
    gamePiece = rawGrid[startR, startC]
    #NOTE we can possibily use gamePiece's name (str) to identify it as well. But for now we'll identify based on int
    return gamePiece

def hasSequence(grid, length):
    return len(grid.findsequences(length)) !=0
    
        
def displayBoard(grid):
    gridInt = grid.createIntGrid()
    rowLabels = np.arange(0, gridInt.shape[0]).reshape(gridInt.shape[0], 1)
    colLabels = np.arange(-1, gridInt.shape[1]).reshape(1, gridInt.shape[1]+1)
    colLabels = np.where(colLabels == -1, '', colLabels)
    newGrid = np.concatenate((rowLabels, gridInt), axis = 1)
    newGrid = np.concatenate((colLabels, newGrid), axis = 0)
    newGrid = np.where(newGrid == None, '~', newGrid)
    print(newGrid,'\n')