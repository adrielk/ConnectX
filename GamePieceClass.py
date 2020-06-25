# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:46:44 2020

@author: Adriel Kim
"""


class GamePiece:
     def __init__(self, color, name, num):
         self._c = color
         self._n = name
         self._id = num

     def getPieceNum(self):
        return self._id
    
     def getPieceName(self):
         return self._n
    
     def getPieceColor(self):
         return self._c
    
         