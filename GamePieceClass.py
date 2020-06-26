# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:46:44 2020

@author: Adriel Kim
"""


class GamePiece:
     def __init__(self, num, name = None, color = None,):
         """

         Parameters
         ----------
         color : string
             Color of game piece for the purposes of visuals.
         name : string
             Name of game piece. Ex: Rook, pawn, redChecker, blackChecker, etc.
         num : int
             Unique number identify game piece. 
             Game pieces with the same color but different names and different nums will be considered
             belonging to the same player
         Returns
         -------
         None.

         """
         self._color = color
         self._name = name
         self._id = num

     def getPieceNum(self):
        return self._id
    
     def getPieceName(self):
         return self._n
    
     def getPieceColor(self):
         return self._c
     
     def __str__(self):
        return ("Name: "+str(self._name)+", Color: "+str(self._color)+", Id = "+str(self._id))
    
         