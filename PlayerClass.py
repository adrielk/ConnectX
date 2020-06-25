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
    def __init__(self, name, teamNum, first = False, eliminated = False):
        self._name = name
        self._teamId = teamNum
        self._first = first
        self._elim = eliminated
    
    #getters
    def getTeamId(self):
        return self._teamId
    
    def getName(self):
        return self._name
    
    def isFirst(self):
        return self._first
    
    def isEliminated(self):
        return self._elim
    
    #methods
    
    def eliminate(self):
        self._elim = True
    
    def makeFirst(self):
        self._first = True
    
    def __str__(self):
        return ("Name: "+str(self._name)+", Team Id: "
                +str(self._teamId)+", First: "+str(self._first)+", Eliminatd: "+str(self._elim))
    