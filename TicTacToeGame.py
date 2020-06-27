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
#Dependancy that deals with managing player turns and round set up for games
import GameRoundManager as gm

def ticTacToe3x3(player1, player2):
    #general vars
    players = [player1, player2]
    grid3x3 = grid(3,3,pieces = [1,2])
    #player and piece vars
    firstPlr = gm.decideFirst(players)#Learning note: players can be changed by this method as they are refernces
    p1Piece = firstPlr.getPieces()[0]
    players.remove(firstPlr)
    secondPlr = players[0]
    p2Piece = secondPlr.getPieces()[0]    
    
    print("Welcome to Tic-Tac-Toe!")
    
    while grid3x3.isFull() == False and gm.hasSequence(grid3x3, 3) == False:
        gm.displayBoard(grid3x3)
        print(str(firstPlr.getName()), "'s turn")
        gm.playerTurn(grid3x3, p1Piece)
        gm.displayBoard(grid3x3)
        if gm.hasSequence(grid3x3, 3):
            break 
        print(str(secondPlr.getName()),"s turn")
        gm.playerTurn(grid3x3, p2Piece)
        gm.displayBoard(grid3x3)
        
    
    if gm.hasSequence(grid3x3, 3) == True:
        winningPiece = gm.getSequenceOwner(grid3x3, 3)
        if winningPiece.getPieceNum() == p1Piece.getPieceNum():
            print(str(firstPlr.getName()), " Wins!")
        else:
            print(str(secondPlr.getName()), " Wins!")
    else:
        print("Draw!")
        


player1 = gm.playerSetUp("X")
player2 = gm.playerSetUp("O")

ticTacToe3x3(player1, player2)
