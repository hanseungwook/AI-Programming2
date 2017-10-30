#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Seungwook Han (sh3264)
"""

import random
import sys
import time
import math

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

states = {}

# Computes the utility for the player
# # of tiles of player - # of tiles of opponent
def compute_utility(board, color):
    score = get_score(board)
    if (color == 1):
        return score[0] - score[1]
    elif (color == 2):
        return score[1] - score[0]


############ MINIMAX ###############################
# This min node recursive fnuction gets the possible moves that
# the opponent can play. If there are no possible moves, then
# it computes the current player's utility and caches it. If
# there are
def minimax_min_node(board, color):
    # If the current board is in cached states, return the stored value
    if (board not in states):
        # Getting the opponent's color
        oppColor = color
        if (oppColor == 1):
            oppColor = 2
        elif (oppColor == 2):
            oppColor = 1

        # Getting the possible moves of the opposite color
        possibleMoves = get_possible_moves(board, oppColor)
        if not possibleMoves:
            util = compute_utility(board, color)
            states[board] = util
            return util

        # For every possible move, play in the opponent's color
        # and pass the nextBoard with the current player's color
        best = float('inf')
        for move in possibleMoves:
            nextBoard = play_move(board, oppColor, move[0], move[1])
            best = min(best, minimax_max_node(nextBoard, color))

        return best

    else:
        return states.get(board)


def minimax_max_node(board, color):
    #If the current board is in cached states, return the stored value
    if (board not in states):
        # Getting the possible moves of the color
        possibleMoves = get_possible_moves(board, color)
        if not possibleMoves:
            util = compute_utility(board, color)
            states[board] = util
            return util

        # For every possible move, play in the color and pass
        # the nextBoard with the same color
        best = float('-inf')
        for move in possibleMoves:
            nextBoard = play_move(board, color, move[0], move[1])
            best = max(best, minimax_min_node(nextBoard, color))

        return best

    else:
        return states.get(board)

    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
def select_move_minimax(board, color):
    # Get possible moves of the color
    possibleMoves = get_possible_moves(board, color)

    nextMove = None
    best = float('-inf')
    states.clear()

    # For every possible move, find the move that results in maximizing
    # the current player's utility
    for move in possibleMoves:
        nextBoard = play_move(board, color, move[0], move[1])
        util = None
        #  Caching / checking cache of next board
        if nextBoard in states:
            util = states.get(nextBoard)
        else:
            util = minimax_min_node(nextBoard, color)
            states[nextBoard] = util

        if (util > best):
            nextMove = move
            best = util

    return nextMove

############ ALPHA-BETA PRUNING #####################

def alphabeta_min_node(board, color, alpha, beta, level=0, limit=float('inf')):

    from heapq import heappush
    from heapq import heappop

    # Run only if the current ply is less than or equal to the limit
    # If not, return the approximate heuristic function calculated
    # by the utiilty function
    if (level <= limit):
        level += 1
        # If the current board is in cached states, return the stored value
        if (board not in states):
            # Get the opponent's color
            oppColor = color
            if (oppColor == 1):
                oppColor = 2
            elif (oppColor == 2):
                oppColor = 1

            # Get all possible moves that could be made with the opponent's color
            possibleMoves = get_possible_moves(board, oppColor)
            if not possibleMoves:
                util = compute_utility(board, color)
                states[board] = util
                return util

            # Create a heap with the negative of the utility function, which will
            # order from highest to lowest in the # of tiles of current - # of tiles of opponent
            pqPossibleMoves = []
            for move in possibleMoves:
                heappush(pqPossibleMoves, (-(compute_utility(board, color)), move))

            # Run while the heap is not empty
            best = float('inf')
            while (pqPossibleMoves):
                # Pop the move with the lowest (-(# of tiles of current - # of tiles of opponent))
                move = heappop(pqPossibleMoves)[1]
                nextBoard = play_move(board, oppColor, move[0], move[1])
                best = min(best, alphabeta_max_node(nextBoard, color, alpha, beta, level, limit))
                if (best <= alpha):
                    return best
                beta = min(beta, best)

            return best

        else:
            return states.get(board)

    # If the level > limit, then estimate the true utility with our utility function
    # and cache it if it does not exist in the states
    else:
        util = compute_utility(board, color)
        if (board not in states):
            states[board] = util
        return util


def alphabeta_max_node(board, color, alpha, beta, level=0, limit=float('inf')):

    from heapq import heappush
    from heapq import heappop

    # Run only if the current ply is less than or equal to the limit
    # If not, return the approximate heuristic function calculated
    # by the utiilty function
    if (level <= limit):
        level += 1
        # If the current board is in cached states, return the stored value
        if (board not in states):
            # Get all possible moves of the color
            possibleMoves = get_possible_moves(board, color)
            if not possibleMoves:
                util = compute_utility(board, color)
                states[board] = util
                return util

            # Creating the heap with the - (computed utility), which will order
            # the list from highest to lowest in (# of tiles of current player -
            # # of tiles of opponent)
            pqPossibleMoves = []
            for move in possibleMoves:
                heappush(pqPossibleMoves, (-(compute_utility(board, color)), move))

            best = float('-inf')
            # Run while the heap is not empty
            while (pqPossibleMoves):
                move = heappop(pqPossibleMoves)[1]
                nextBoard = play_move(board, color, move[0], move[1])
                best = max(best, alphabeta_min_node(nextBoard, color, alpha, beta, level, limit))
                if (best >= beta):
                    return best
                alpha = max(alpha, best)

            return best

        else:
            return states.get(board)

    # If the level > limit, then estimate the true utility with our utility function
    # and cache it if it does not exist in the states
    else:
        util = compute_utility(board, color)
        if (board not in states):
            states[board] = util
        return util


def select_move_alphabeta(board, color):

    from heapq import heappush
    from heapq import heappop

    # Get all possible moves and make a heap from the list with - (computed utility)
    possibleMoves = get_possible_moves(board, color)

    pqPossibleMoves = []
    for move in possibleMoves:
        heappush(pqPossibleMoves, (-(compute_utility(board, color)), move))

    nextMove = None
    best = float('-inf')

    level = 0
    limit = 4
    alpha = float('-inf')
    beta = float('inf')
    states.clear()

    # Run while the heap is not empty
    while (pqPossibleMoves):
        move = heappop(pqPossibleMoves)[1]
        nextBoard = play_move(board, color, move[0], move[1])
        util = None
        #  Caching / checking cache of next board
        if nextBoard in states:
            util = states.get(nextBoard)
        else:
            util = alphabeta_min_node(nextBoard, color, alpha, beta, level, limit)
            states[nextBoard] = util

        if (util > best):
            nextMove = move
            best = util

    return nextMove


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Wall-e") # First line is the name of this AI
    color = int(input()) # Then we read the color: 1 for dark (goes first),
                         # 2 for light.

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
