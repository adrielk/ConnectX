# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 01:20:26 2020

Tester

@author: Adriel Kim
"""
from GameBoardClass import GameGrid

g = GameGrid(6,7, gravity = True)

g.insert_piece(0,(1,1))
print(g.get_board())

g.insert_piece(0,(3,3))
print(g.get_board())
g.insert_piece(1,(1,3))


print(g.get_board())

locs = g.getPieceLocations()

# for p in g.get_pieces():
#     print(locs[p])
#     for l in locs[p]:
#         print(l)
    