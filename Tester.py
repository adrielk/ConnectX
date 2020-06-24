# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 01:20:26 2020

Tester

@author: Adriel Kim
"""
from GameBoardClass import GameGrid

def printBoard(grid):
    print(g.get_board(),'\n')

g = GameGrid(6,7, gravity = False)

printBoard(g)


g.insert_piece(0, (1,2))
g.insert_piece(0, (2,3))
g.insert_piece(0, (3,4))
g.insert_piece(0, (4,5))
g.insert_piece(0, (5,6))

g.insert_piece(0, (5,0))
g.insert_piece(0, (4,1))
g.insert_piece(0, (3,2))
g.insert_piece(0, (2,3))
g.insert_piece(0, (1,4))


printBoard(g)

seqs = g.findSequences(5)

print(seqs)

#locs = g.getPieceLocations()

# for p in g.get_pieces():
#     print(locs[p])
#     for l in locs[p]:
#         print(l)
    