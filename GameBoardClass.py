# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 23:36:44 2020

Board Class for:
Connect X - Text Version
Future: Implement with pygame

@author: Adriel Kim
"""

"""
This is simple a board.
In real life and board has the following capabilities:
    A board can have game pieces placed on it. 
    It has a grid (matrix), allowing us to identify a game piece's precise location
    A board has a specific size
    A board has gravity
    A board can have a specific pattern (like a chess board)
        In order to make it easy to change, simply add color attributes to grid squares
    We can see if a board has a line (a sequence of adjacent pieces)
    
    NOTE:X is rows, Y is columns
    NOTE: -1 represents an empty grid point
    
    To do:
        add more documentation.

"""
    
import numpy as np
from GamePieceClass import GamePiece

class GameGrid:
    #pieces is the domain of pieces that will be used. They must be integers
    def __init__(self, sizeX = 0, sizeY = 0, pieces = [0 ,1], gravity = False):
        self._X = sizeX #int
        self._Y = sizeY #int
        self._grid = np.full((sizeX, sizeY), -1)
        self._pieces = pieces
        self._grav = gravity
    
    def get_size(self):
        return (self.X, self.Y)
    
    def get_board(self):
        return self._grid
    
    def get_pieces(self):
        return self._pieces
    
    def get_gravity(self):
        return self._grav
    
    def set_board(self, new_grid):
        self._grid = new_grid
        
    def isEmpty(self):
        compareGrid = np.full((self.X, self.Y), -1)
        #test if same shape, same element value
        return np.array_equal(compareGrid, self.grid)
    
    def isFull(self):
        result = np.where(self._grid == -1)
        full = True
        for res in result:
            if len(res) !=0:
                full = False
        return full

    """
    Helpers for findSequence. Vertically traversing down a column. Returns ending indices and whether or not length matches. 
        Horizontal traversal works the same way.
    NOTE: Sequences are repeated if they are longer than required length. These will still be valid sequences
    
    """

    def _verticalTraversal(self, startPoint, length):
        """
        Parameters
        ----------
        startPoint : tuple
            Tuple representing starting point: (row, col)
        length : int
            Minimum length of sequence
        Returns
        -------
        endPoint : tuple
            Tuple representing end of sequence: (row, col)
        Boolean
            This bool represents whether of not a path was found at the startPoint

        """
        #grid variables
        indX = startPoint[0]#rows(what we want to traverse along)
        indY = startPoint[1]#cols
        pieceNum = self._grid[indX,indY]
        Xdim = self._X
        #accumulator
        curLength = 0
        #returns
        endPoint = (-1, -1)
        
        while indX < Xdim:
            curPiece = self._grid[indX, indY]
            if curPiece == pieceNum:
                curLength += 1
                endPoint = (indX , indY)
            else:
                break
            indX += 1
        
        return endPoint, curLength >= length
    
    def _horizontalTraversal(self, startPoint, length):
        #grid vars
        
        indX = startPoint[0]
        indY = startPoint[1]
        pieceNum = self._grid[indX,indY]
        Ydim = self._Y
        #accum
        curLength = 0
        #returns
        endPoint = (-1 , -1)
        
        while indY < Ydim:
            curPiece = self._grid[indX, indY]
            if curPiece == pieceNum:
                curLength += 1
                endPoint = (indX, indY)
            else:
                break
            indY += 1
        
        return endPoint, curLength >= length
    
    """
    Note: forward is a boolean. True means forward diagonal, False means backward diagonal
    """
    def _DiagonalTraversal(self, startPoint, length, forward):
        #grid vars
        indX = startPoint[0]
        indY = startPoint[1]
        pieceNum = self._grid[indX, indY]
        Ydim = self._Y
        Xdim = self._X
        #accum
        curLength = 0
        
        #returns
        endPoint = (-1, -1)
        
        while indY < Ydim and indX < Xdim:
            curPiece = self._grid[indX, indY]
            if curPiece == pieceNum:
                curLength += 1
                endPoint = (indX, indY)
            else:
                break
            if forward == True:
                indY += 1
                indX += 1
            else:
                indY += 1
                indX -= 1
            
        
        return endPoint, curLength >= length
    """
    Sequence is defined as adjacent identical pieces either vertically, horiztonally, or diagonally
    
    Given length (length of sequence), return a dictionary of sequences with corresponding start, length, and traversal type.
    3 Traversal types: "vert" ,"horz", "forDiag", "backDiag"
    
    NOTE: There could be a recursive implementation of this...
    
    Optimization Note: Stop vertical looping at a point where it's no longer possible to have a long enough sequence
    
    """    

    def findSequences(self, length):
        grid = self._grid
        seqs = []
        Xdim = self._X
        Ydim = self._Y
        #Vertical Check
        for i in range(0, Xdim):
            for k in range(0, Ydim):
                curPoint = (i, k)
                if(grid[i,k] != -1):
                    #vertical check
                    endP, exists = self._verticalTraversal(curPoint, length)
                    if exists == True:
                        seqs.append(("vert", curPoint, endP))#starting and ending point of sequence
                    #horizontal check
                    endP2, exists2 = self._horizontalTraversal(curPoint, length)
                    if exists2 == True:
                        seqs.append(("horz", curPoint, endP2))
                    #back diagonal check
                    endP3, exists3 = self._DiagonalTraversal(curPoint, length, False)
                    if exists3 == True:
                        seqs.append(("backDiag", curPoint, endP3))
                    #forward diagonal check
                    endP4, exists4 = self._DiagonalTraversal(curPoint, length, True)
                    if exists4 == True:
                        seqs.append(("forDiag", curPoint, endP4))
                
        return seqs                
        
    """
    Returns a dictionary where piece number is key and value is 
        parallel arrays of row and column values for each piece number
    """          
    def getPieceLocations(self):
        pLocs = dict()
        for p in self._pieces:
            locs = np.where(self._grid == p)#Tuples of row and col of piece
            pLocs[p] = locs
        return pLocs
    
    """
        gamePiece is a GamePiece object. 
    """
    def insert_piece(self, gamePiece, location):
        locX = location[0]
        locY = location[1]
        pieceNum = gamePiece.getPieceNum()
        grav = self._grav
        if type(pieceNum) != int:
            raise Exception("Please enter integer for piece number")
        if type(locX) != int or type(locY)!=int:
            raise Exception("Plese enter integers into tuple for location")
        if grav == False:
           self._grid[locX,locY] = pieceNum
        else:
           if(self._grid[0,locY]!= -1):
                raise Exception("Piece out of bounds of game board")
          
           for i in range(self._X-1, -1,-1):
               cur = self._grid[i , locY]
               if cur == -1:
                   self._grid[i , locY] = pieceNum 
                   break


    
                
        
    


