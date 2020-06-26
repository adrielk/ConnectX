# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 00:05:36 2020

Tic-Tac-Toe using GameGrid, GamePiece, and Player Classes
Text Version

To do:
    Tic-Tac-Toe tournament. Very easy to implement with this framework.
    Error handling? Or just use GUI

@author: Adriel Kim
"""

from GameBoardClass import GameGrid as grid
from GamePieceClass import GamePiece as gp
from PlayerClass import Player as plr
from random import randint

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

def playerTurn(grid, playerPiece):
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
    grid.printboard("~")
    
def ticTacToe3x3(player1, player2):
    #general vars
    players = [player1, player2]
    grid3x3 = grid(3,3,pieces = [1,2])
    #player and piece vars
    firstPlr = decideFirst(players)#Learning note: players can be changed by this method as they are refernces
    p1Piece = firstPlr.getPieces()[0]
    players.remove(firstPlr)
    secondPlr = players[0]
    p2Piece = secondPlr.getPieces()[0]    
    
    while grid3x3.isFull() == False and hasSequence(grid3x3, 3) == False:
        displayBoard(grid3x3)
        print(str(firstPlr.getName()), "'s turn")
        playerTurn(grid3x3, p1Piece)
        displayBoard(grid3x3)
        if hasSequence(grid3x3, 3):
            break 
        print(str(secondPlr.getName()),"s turn")
        playerTurn(grid3x3, p2Piece)
        displayBoard(grid3x3)
        
    
    if hasSequence(grid3x3, 3) == True:
        winningPiece = getSequenceOwner(grid3x3, 3)
        if winningPiece.getPieceNum() == p1Piece.getPieceNum():
            print(str(firstPlr.getName()), " Wins!")
        else:
            print(str(secondPlr.getName()), " Wins!")
    else:
        print("Draw!")
        


player1 = playerSetUp("X")
player2 = playerSetUp("O")

ticTacToe3x3(player1, player2)
