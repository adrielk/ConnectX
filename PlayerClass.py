# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 00:09:10 2020

@author: Adriel Kim

What a player does:
    1. They are part of a team
    2. They have a name
    3. They have turns
    4. They have priority (whether or not they go first)
    5. They can be a winner
    6. They can be eliminated
    
"""

class Player:
    def __init__(self, name, teamNum, piecesOwned = [], first = False, eliminated = False):
        """

        Parameters
        ----------
        name : str
            Name of piece
        teamNum : int
            DESCRIPTION.
        piecesOwned : list, optional
            List of pieces that the player owns. These can be copied into a grid The default is [].
        first : bool, optional
            Boolean of whether or not a player goes first in a game. The default is False.
        eliminated : bool, optional
            Boolean of whether or not a player is eliminated in a game. The default is False.

        Returns
        -------
        None.

        """
        self._name = name
        self._teamId = teamNum
        self._first = first
        self._elim = eliminated
        self._playerPieces = piecesOwned
    
    #getters
    def getTeamId(self):
        return self._teamId
    
    def getName(self):
        return self._name
    
    def isFirst(self):
        return self._first
    
    def isEliminated(self):
        return self._elim
    
    def getPieces(self):
        return self._playerPieces
    
    #methods
    
    def eliminate(self):
        self._elim = True
    
    def makeFirst(self):
        self._first = True
        
    def setPieces(self, pieces):
        self._playerPieces = pieces
    
    def __str__(self):
        return ("Name: "+str(self._name)+", Team Id: "
                +str(self._teamId)+", First: "+str(self._first)+", Eliminatd: "+str(self._elim))
    