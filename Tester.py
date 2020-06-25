# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 01:20:26 2020

Tester

@author: Adriel Kim
"""
from GameBoardClass import GameGrid
from GamePieceClass import GamePiece
from PlayerClass import Player as pl

red = GamePiece("red", "redPiece", 1)
black = GamePiece("black", "blackPiece",2)
g = GameGrid(6,7,pieces =[red, black] , gravity = False)

player = pl("Bob", 1)

print(player)
print(red)
print(black)
print(g)

g.printboard()

g.insert_piece(red, (1,2))
g.insert_piece(red, (2,3))
g.insert_piece(red, (3,4))
g.insert_piece(red, (4,5))
g.insert_piece(red, (5,6))

g.insert_piece(black, (5,0))
g.insert_piece(black, (4,1))
g.insert_piece(black, (3,2))
g.insert_piece(black, (2,3))
g.insert_piece(black, (1,4))
g.insert_piece(red, (2,3))


g.printboard()


seqs = g.findsequences(5)

print(seqs)

locs = g.getlocations()

for p in g.get_pieces():
    print(locs[p])
    for l in locs[p]:
        print(l)
    