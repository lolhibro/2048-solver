#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 20:51:40 2018

@author: shrikar.amirisetty
"""

import math
from BaseAI_3 import BaseAI
 
class PlayerAI(BaseAI):
    def getMove(self, grid):
        def getUtility(grid):
    
            utility = 0
    
            """Heuristic 1: Number of empty cells"""
            empty_cells = grid.getAvailableCells()
            utility += len(empty_cells)
    
            """Heuristic 2: Maximum tile number"""
            max_tile_value = grid.getMaxTile()
            utility += math.log(max_tile_value, 2)
    
            """Heuristic 3: Good pattern when maximum value tile is in corner"""
            x1 = 0
            x2 = 3
            y1 = 0
            y2 = 3
            utility1 = 0
            utility2 = 0
    
            if max_tile_value == grid.map[x2][y2]:
                y2temp = y2
                while y2temp != y1 and grid.map[x1][y2temp - 1] != 0:
                    if grid.map[x1][y2temp]/grid.map[x1][y2temp - 1] == 2:
                        utility1 += 1
                        y2temp -= 1
                    else:
                        break
        
                x2temp = x2
                while x2temp != x1 and grid.map[x2temp - 1][y1] != 0:
                    if grid.map[x2temp][y1]/grid.map[x2temp - 1][y1] == 2:
                        utility2 += 1
                        x2temp -= 1
                    else:
                        break
                utility += max(utility1, utility2)
                utility1 = 0
                utility2 = 0
    
            elif max_tile_value == grid.map[x2][y1]:
                y1temp = y1
                while y1temp != y2 and grid.map[x1][y1temp + 1] != 0:
                    if grid.map[x1][y1temp]/grid.map[x1][y1temp + 1] == 2:
                        utility1 += 1
                        y1temp += 1
                    else:
                        break
        
                x2temp = x2
                while x2temp != x1 and grid.map[x2temp - 1][y1] != 0:
                    if grid.map[x2temp][y1]/grid.map[x2temp - 1][y1] == 2:
                        utility2 += 1
                        x2temp -= 1
                    else:
                        break
                utility += max(utility1, utility2)
                utility1 = 0
                utility2 = 0
        
            elif max_tile_value == grid.map[x1][y2]:
                y2temp = y2
                while y2temp != y1 and grid.map[x1][y2temp - 1] != 0:
                    if grid.map[x1][y2temp]/grid.map[x1][y2temp - 1] == 2:
                        utility1 += 1
                        y2temp -= 1
                    else:
                        break
        
                x1temp = x1
                while x1temp != x2 and grid.map[x1temp + 1][y1] != 0:
                    if grid.map[x1temp][y1]/grid.map[x1temp + 1][y1] == 2:
                        utility2 += 1
                        x1temp += 1
                    else:
                        break
                utility += max(utility1, utility2)
                utility1 = 0
                utility2 = 0
        
            elif max_tile_value == grid.map[x1][y1]:
                y1temp = y1
                while y1temp != y2 and grid.map[x1][y1temp + 1] != 0:
                    if grid.map[x1][y1temp]/grid.map[x1][y1temp + 1] == 2:
                        utility1 += 1
                        y1temp += 1
                    else:
                        break
        
                x1temp = x1
                while x1temp != x2 and grid.map[x1temp + 1][y1] != 0:
                    if grid.map[x1temp][y1]/grid.map[x1temp + 1][y1] == 2:
                        utility2 += 1
                        x1temp += 1
                    else:
                        break
                utility += max(utility1, utility2)
                utility1 = 0
                utility2 = 0

            else:
                """Heuristic 4: Attempted patterns when not in the corner"""
                if max_tile_value == grid.map[0 or 3][1 or 2] or grid.map[1 or 2][0 or 3]:
                    utility += 1

            """Heuristic 5: Other adjacency bonuses"""
            utility3 = 0
            utility4 = 0
    
            for x in range(grid.size):
                for y in range(grid.size):
                    if x != 3 and grid.map[x][y] == grid.map[x+1][y]:
                        utility1 += 1
                    if y != 3 and grid.map[x][y] == grid.map[x][y+1]:
                        utility2 += 1
                    if y != 0 and grid.map[x][y] == grid.map[x][y-1]:
                        utility3 += 1
                    if x != 0 and grid.map[x][y] == grid.map[x-1][y]:
                        utility4 += 1
    
            utility += max(utility1, utility2, utility3, utility4)
        
            return utility
        
        """Actual getMove code starts here"""
        
        moves = grid.getAvailableMoves()
        grid_children = []
        
        for direction in moves:
            gridcopy = grid.clone()
            gridcopy.move(direction)
            grid_children += [[gridcopy, direction]]

        move_dict_depth1 = {}
        
        for child in grid_children:
            moves = child[0].getAvailableMoves()
            children_of_child = []
            
            for direction in moves:
                grid_child = child[0].clone()
                grid_child.move(direction)
                children_of_child += [grid_child]
            
            move_dict_depth1[tuple(child)] = children_of_child
        
        alpha = 0
        possible_alpha_depth1 = [0]
        child_to_utility = {}
        
        for i in move_dict_depth1:
            possible_utilities = []

            for grandchild in range(len(move_dict_depth1[i])):
                utility = getUtility(move_dict_depth1[i][grandchild])
                possible_utilities += [utility]
                if utility <= alpha:
                    del(move_dict_depth1[i][grandchild+1:len(move_dict_depth1[i])])
                    break
            
            possible_alpha_depth1 += [min(possible_utilities)]
            child_to_utility[i] = possible_alpha_depth1[-1]
            alpha = max(possible_alpha_depth1)
        
        children_of_child_all = []
        
        for i in move_dict_depth1:
            for x in move_dict_depth1[i]:
                children_of_child_all += [x]
        
        move_dict_depth2 = {}
        children_of_child2 = []
        
        for i in children_of_child_all:
            moves = i.getAvailableMoves()
            children = []
            
            for direction in moves:
                i_child = i.clone()
                i_child.move(direction)
                children += [i_child]
                children_of_child2 += [i_child]
            
            move_dict_depth2[i] = children
            
        move_dict_depth3 = {}
        
        for i in children_of_child2:
            moves = i.getAvailableMoves()
            children = []
            
            for direction in moves:
                i_child = i.clone()
                i_child.move(direction)
                children += [i_child]
            
            move_dict_depth3[i] = children
        
        alpha = 0
        possible_alpha_depth1 = [0]
        child_to_utility = {}     
        
        for i in move_dict_depth3:
            possible_utilities = []

            for finalstate in range(len(move_dict_depth3[i])):
                utility = getUtility(move_dict_depth3[i][finalstate])
                possible_utilities += [utility]
                if utility <= alpha:
                    del(move_dict_depth3[i][finalstate+1:len(move_dict_depth3[i])])
                    break
            
            possible_alpha_depth1 += [min(possible_utilities)]
            child_to_utility[i] = possible_alpha_depth1[-1]

        for i in move_dict_depth2:
            possible_utilities = []
            
            for x in move_dict_depth2[i]:
                possible_utilities += [child_to_utility[x]]
            
            child_to_utility[i] = max(possible_utilities)
        
        final_child_utility_dict = {}
        
        for i in move_dict_depth1:
            possible_utilities = []
            
            for x in move_dict_depth1[i]:
                possible_utilities += [child_to_utility[x]]
            
            final_child_utility_dict[i] = min(possible_utilities)
        
        alpha = max(final_child_utility_dict.values())
        
        for i in final_child_utility_dict:
            if final_child_utility_dict[i] == alpha:
                move = i
        
        return move[1]
            
            
            






