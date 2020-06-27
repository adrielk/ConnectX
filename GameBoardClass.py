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
    NOTE: None represents an empty grid point
    
    To do:
        add more documentation.
        Add a UI layer class
        More objects: card deck, etc (implement UNO!)

"""
    
import numpy as np
from GamePieceClass import GamePiece as gP

class GameGrid:
    def __init__(self, sizeX, sizeY, pieces, gravity = False):
        """
        Parameters
        ----------
        sizeX : int
            Dimension of rows
        sizeY : int
            Dimension of columns
        pieces : list
            List containing GamePiece objects. This is the domain of pieces our grid will deal with.
        gravity : bool, optional
            Whether or not the gameboard is subject to gravity. Think Connect-4 vs Checkers.
            The default is False.

        Returns
        -------
        None.

        """
        self._X = sizeX #int
        self._Y = sizeY #int
        self._grid = np.full((sizeX, sizeY), None)#Will consist of matrix of GamePiece objects
        #self._intGrid = np.full((sizeX,sizeY), 0)#purely for display purposes
        self._pieces = pieces
        self._grav = gravity
    
    def get_size(self):
        return (self.X, self.Y)
    
    def get_board(self):
        return self._grid
    
    def get_boardInts(self):
        intGrid = self.createIntGrid()
        return intGrid
    
    def get_pieces(self):
        return self._pieces
    
    def get_gravity(self):
        return self._grav
    
    def set_board(self, new_grid):
        self._grid = new_grid
        
    def isEmpty(self):
        compareGrid = np.full((self.X, self.Y), None)
        #test if same shape, same element value
        return np.array_equal(compareGrid, self.grid)
    
    def isFull(self):
        result = np.where(self._grid == None)
        full = True
        for res in result:
            if len(res) !=0:
                full = False
        return full
    
    def printboard(self, nilSymbol = 0):
        intGrid = self.createIntGrid()
        pGrid = np.where(intGrid == None,nilSymbol, intGrid)
        print(pGrid,"\n")
    
    """
    Private helper method for getlocations and findSequence, which relys on an integer matrix of piece Id's
    """        
    def createIntGrid(self):
        intGrid = self._grid.copy()#must copy if we don't want it to act as a reference
        #print(intGrid)
        nilVal = None
        for i in range(0, self._X):
            for k in range(0, self._Y):
                if intGrid[i,k] == None:
                    intGrid[i,k] = nilVal
                else:
                    #print(intGrid[i,k])
                    intGrid[i,k] = intGrid[i,k].getPieceNum()#replaces gamePiece Object with its unique Id
        return intGrid

    """
    Helpers for findSequence. Vertically traversing down a column. Returns ending indices and whether or not length matches. 
        Horizontal traversal works the same way.
    NOTE: Sequences are repeated if they are longer than required length. These will still be valid sequences
    
    """

    def _verticalTraversal(self, startPoint, length, grid):
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
        pieceNum = grid[indX,indY]
        Xdim = self._X
        #accumulator
        curLength = 0
        #returns
        endPoint = (-1, -1)
        
        while indX < Xdim:
            curPiece = grid[indX, indY]
            if curPiece == pieceNum:
                curLength += 1
                endPoint = (indX , indY)
            else:
                break
            indX += 1
        
        return endPoint, curLength >= length
    
    def _horizontalTraversal(self, startPoint, length, grid):
        #grid vars
        
        indX = startPoint[0]
        indY = startPoint[1]
        pieceNum = grid[indX,indY]
        Ydim = self._Y
        #accum
        curLength = 0
        #returns
        endPoint = (-1 , -1)
        
        while indY < Ydim:
            curPiece = grid[indX, indY]
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
    def _diagonalTraversal(self, startPoint, length, forward, grid):
        #grid vars
        indX = startPoint[0]
        indY = startPoint[1]
        pieceNum = grid[indX, indY]
        Ydim = self._Y
        Xdim = self._X
        #accum
        curLength = 0
        
        #returns
        endPoint = (-1, -1)
        
        while indY < Ydim and indX < Xdim:
            curPiece = grid[indX, indY]
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
    
    def _isEmptySymbol(self, symbol):
        return symbol == None #Empty = True
        
    
    """
    Sequence is defined as adjacent identical pieces either vertically, horiztonally, or diagonally
    
    Given length (length of sequence), return a dictionary of sequences with corresponding start, length, and traversal type.
    3 Traversal types: "vert" ,"horz", "forDiag", "backDiag"
    
    NOTE: There could be a recursive implementation of this...
    
    Optimization Note: Stop vertical looping at a point where it's no longer possible to have a long enough sequence
    
    """    

    def findsequences(self, length):
        """
        Parameters
        ----------
        length : int
            Length of sequence we're looking for.

        Returns
        -------
        seqs : list
            list of tuples of sequences. 
            Each tuple contains the sequence type (str), the starting point (tuple), and ending point (tuple).

        """
        grid = self.createIntGrid()
        seqs = []
        Xdim = self._X
        Ydim = self._Y
        #Vertical Check
        for i in range(0, Xdim):
            for k in range(0, Ydim):
                curPoint = (i, k)
                if(self._isEmptySymbol(grid[i,k]) == False): #grid[i,k] != -1):
                    #vertical check
                    endP, exists = self._verticalTraversal(curPoint, length, grid)
                    if exists == True:
                        seqs.append(("vert", curPoint, endP))#starting and ending point of sequence
                    #horizontal check
                    endP2, exists2 = self._horizontalTraversal(curPoint, length, grid)
                    if exists2 == True:
                        seqs.append(("horz", curPoint, endP2))
                    #back diagonal check
                    endP3, exists3 = self._diagonalTraversal(curPoint, length, False, grid)
                    if exists3 == True:
                        seqs.append(("backDiag", curPoint, endP3))
                    #forward diagonal check
                    endP4, exists4 = self._diagonalTraversal(curPoint, length, True, grid)
                    if exists4 == True:
                        seqs.append(("forDiag", curPoint, endP4))
                
        return seqs                            
    """
    Returns a dictionary where piece number is key and value is 
        parallel arrays of row and column values for each piece number
        This method of retrieving locations assumes that each piece has a unique pieceNum (id) associated with it.
    """          
    def getlocations(self):
        intGrid = self.createIntGrid();
        pLocs = dict()
        for p in self._pieces:
            #Since we're traversing pieces, we need to get unique id with getPieceNum
            locs = np.where(intGrid == p.getPieceNum())#Tuples of row and col of piece
            pLocs[p] = locs
        return pLocs
    """
    Similar to getlocations but only returns tuples of the locations
    """
    def getPopulated(self):
        locationSet = {}        
        for i in range(0, self._X):
            for k in range(0, self._Y):
                if self._grid[i,k] != None:
                    locationSet.add((i,k))
        return locationSet
    
    """
        gamePiece is a GamePiece object. 
        To do: Insert actual game piece object at point. But what will actually be displayed is the game piece num.
            Basically, the gamegrid should be a matrix of pieces, not integers! None = ~
    """
    def insert_piece(self, gamePiece, location):
        """
        Parameters
        ----------
        gamePiece : GamePiece object/Card object
            GamePiece object we want to put on the board.
        location : tuple
            Tuple of ints representing location of gamePiece (R,C).

        Raises
        ------
        Exception
            Occurs when tuple elements are not all of type int.
            Or when a piece is out of bounds.
        Returns
        -------
        None.

        """
        locX = location[0]
        locY = location[1]
        #pieceNum = gamePiece.getPieceNum()
        grav = self._grav
        # if type(pieceNum) != int:
        #     raise Exception("Please enter integer for piece number")
        if type(locX) != int or type(locY)!=int:
            raise Exception("Plese enter integers into tuple for location")
        if grav == False:
           self._grid[locX,locY] = gamePiece
        else:
           if(self._grid[0,locY] != None):
                raise Exception("Piece out of bounds of game board")
          
           for i in range(self._X-1, -1,-1):
               cur = self._grid[i , locY]
               if cur == None:
                   self._grid[i , locY] = gamePiece 
                   break
    """
    shapeMatch returns true when shapes of both grids are the same and when the set of locations at which their game pieces 
    are populated are equal.
    """           
    def shapeMatch(self, otherGrid):
        sameShape = self._grid.shape == otherGrid.get_board().shape
        myLocs = self.getPopulated()
        otherLocs = otherGrid.getPopulated()
        
        return sameShape and otherLocs == myLocs
               
    """
    Overrided equals method which compares based on equality of integer grid representation of grid matrices
    """
    def __eq__(self, otherGrid):
        myIntGrid = self.createIntGrid()
        otherIntGrid = otherGrid.createIntGrid()
        return myIntGrid == otherIntGrid
        

    def __str__(self):
        return ("Dimensions (R x C): ("+str(self._X)+","+str(self._Y)+
                "), "+"Number of pieces: "+str(len(self._pieces))+", Gravity = "+str(self._grav))
    
                
        
    


