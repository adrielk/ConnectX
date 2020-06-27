# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:55:03 2020

Connect 4 - Text Version

Exact same implementation as TicTacToe but with game baord's gravity enabled!

@author: Adriel Kim
"""

from GameBoardClass import GameGrid as grid
#Dependancy that deals with managing player turns and round set up for games
import GameRoundManager as gm

def PlayConnectX(player1, player2, dims, length):
    """
    Parameters
    ----------
    player1 : PlayerClass object
        PlayerClass object representing player1.
    player2 : PlayerClass object
        PlayerClass object representing player2.
    dims : tuple
        Dimensions (R,C) of our game board.
    length : int
        Minimum length of sequence required to win the game.
    Returns
    -------
    None.

    """
    #general vars
    players = [player1, player2]
    gridX = grid(dims[0],dims[1],pieces = [1,2], gravity = True)
    #player and piece vars
    firstPlr = gm.decideFirst(players)#Learning note: players can be changed by this method as they are refernces
    p1Piece = firstPlr.getPieces()[0]
    players.remove(firstPlr)
    secondPlr = players[0]
    p2Piece = secondPlr.getPieces()[0]  
    
    print("\nWelcome to Connect -",length,'!\n')
    
    while gridX.isFull() == False and gm.hasSequence(gridX, length)  == False:
        gm.displayBoard(gridX)
        print(str(firstPlr.getName()), "'s turn")
        gm.playerTurn(gridX, p1Piece, rowMatters = False)
        gm.displayBoard(gridX)
        if gm.hasSequence(gridX, length):
            break 
        print(str(secondPlr.getName()),"s turn")
        gm.playerTurn(gridX, p2Piece, rowMatters = False)
        gm.displayBoard(gridX)
        
    
    if gm.hasSequence(gridX, length) == True:
        winningPiece = gm.getSequenceOwner(gridX, length)
        if winningPiece.getPieceNum() == p1Piece.getPieceNum():
            print(str(firstPlr.getName()), " Wins!")
        else:
            print(str(secondPlr.getName()), " Wins!")
    else:
        print("Draw!")
    

player1 = gm.playerSetUp("O")
player2 = gm.playerSetUp("X")
PlayConnectX(player1, player2, (6,7), 4)