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

    NOTE:X is rows, Y is columns

"""
    
import numpy as np

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
    Returns a dictionary where piece number is key and value is 
        parallel arrays of row and column values for each piece number
    """
    def getPieceLocations(self):
        pLocs = dict()
        for p in self._pieces:
            locs = np.where(self._grid == p)#Tuples of row and col of piece
            pLocs[p] = locs
        return pLocs
    
    
    #Fix issues with gravity
    def insert_piece(self, pieceNum, location):
        locX = location[0]
        locY = location[1]
        grav = self._grav
        if type(pieceNum) != int:
            raise Exception("Please enter integer for piece number")
        if type(locX) != int or type(locY)!=int:
            raise Exception("Plese enter integers into tuple for location")
        if grav == False:
           self._grid[locX,locY] = pieceNum
        else:
           colStack = list(self._grid[:, locY])
           # if(colStack[-1]!=-1 and colStack[0]==-1):
           #     colStack.reverse()
           
           while len(colStack) > 0 and colStack[-1] == -1:
               print(colStack.pop())
          
           colStack.append(pieceNum)
           while(len(colStack)<self._X):
               colStack.append(-1)
               
           # colStack.reverse()
           colStackNp = np.array(colStack).reshape(len(colStack),1)
           # print(colStackNp)
           # print((self._grid[:,0:locY]))
           # print(self._grid[:,locY:-1])
           
           new_grid = np.concatenate((self._grid[:,0:locY],colStackNp),axis = 1)
           new_grid = np.concatenate((new_grid, self._grid[:,locY:-1]),axis = 1)
           self._grid = new_grid
            

    
    



            
        
    


