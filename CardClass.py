# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:49:04 2020

Two-sided card class
#Perhaps this can be extended by a deck card class

@author: Adriel Kim
"""
from GamePieceClass import GamePiece
#Extended class of game piece
class Card(GamePiece):
    def __init__(self, front, back, name = None):
        """
        Parameters
        ----------
        front : string
            Text on front of card.
        back : string
            Text on back of card.
        name : TYPE, optional
            Specific name/type of card The default is None.

        Returns
        -------
        None.

        """
        self.front = front
        self.back = back
        self.name = name
        self.front_facing = True
      
    #getters    
    def getFront(self):
        return self.front
    
    def getBack(self):
        return self.back
    
    def getName(self):
        return self.name
    
    #This is obivously disgusting, you need to come up with a better hierarchy of game pieces
    def getPieceNum(self):
        if(self.front_facing == True):
            return self.front
        else:
            return self.back
    #methods
    
    def setFace(self, front_facing):
        self.front_facing = front_facing
        
    def setBack(self, back_face):
        self.back = back_face
    
    def flipCard(self):
        self.front_facing = not self.front_facing
        
    def __str__(self):
        if(self.front_facing == True):
            return(self.front)
        else:
            return(self.back)
    
        