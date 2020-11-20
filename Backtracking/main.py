# Gabriel Corella
# CISC 481: Artificial Intelligence Program 2

import time
from random import randint

# Implement a backtracking search which
# takes a CSP and finds a valid assignment for
# all the variables in the CSP, if one exists.
# It should leverage your AC-3 implementation to maintain
# Part 5 [30 pts] arc consistency.

def detectCollision(x, y, assignments):
    for i, j in assignments:
        if (i, j) != (x, y):
            if (y + x == j + i) or (y - x == j - i):
                return False
            elif j == y:
                return False

    return True

# returns a list of domain values for a given row
def getDeletedValues(assignments, row, domains):
    values = []
    for col in domains[row]:
        if detectCollision(row, col, assignments):
            values.append(col)

    return values


# returns updated domains based on current assignments
# and a boolean for notifying empty domains. If any domain
# becomes empty, returns an empty list False.
# Also reutrns the row with minimum remaining domains (if specified). If multiple
# rows have minimum domains, returns first one.

def minRVals(assignments, domains, unassigned, n, mrv=False):
    minsize = 9999
    newdomains = {}
    nextrow = len(assignments)
    list = []

    for i in unassigned:
        values = getDeletedValues(assignments, i, domains)
        if len(values) == 0:
            return {}, True, nextrow
        newdomains[i] = values

        if mrv:
            size = len(values)
            if size == minsize:
                list.append(i)
            if size < minsize:
                nextrow = i
                minsize = size
                del list[:]

    if len(list) != 0:
        index = randint(0, len(list)-1)
        nextrow = list[index]

    return newdomains, False, nextrow

def backtracking(assingments, row, n):
    # If all queens are placed, we are done
    if len(assignments) == n:
        return assignments

    for col in range(n):
        assingments.add((row, col))

        if detectCollision(row, col, assingments) and backtracking(assingments, row+1, n) != None:
            return assignments

        assingments.remove((row, col))

    return None
# returns the NxN board list
def createBoard(size):
    return [['_'] * size for row in range(size)]

# backtracking algorithm with forward check
# if all queens are placed then we are done.
def backtrackingFC(assignments, domains, unassigned, row, n):

    if len(assignments) == n:
        return assignments

    # iterate over columns for a given row
    for col in domains[row]:
        assignments.add((row, col))
        unassigned.remove(row)

        newdomains, isempty, nextrow = minRVals(assignments, domains, unassigned, n)

        if not isempty:
            if backtrackingFC(assignments, newdomains, unassigned, row + 1, n) != None:
                return assignments

        assignments.remove((row, col))
        unassigned.add(row)

    return None


# backtracking algorithm with forward checking and MRV
# Write a function minimum-remaining-values that
# takes a CSP and a set of variable assignments as input,
# and returns the variable with the fewest values in its domain among the unassigned variables in the CSP.
def backtrackingFCMRV(assignments, domains, unassigned, row, n):
    # If all queens are placed, we are done
    if len(assignments) == n:
        return assignments

    for col in domains[row]:
        assignments.add((row, col))
        unassigned.remove(row)

        newdomains, isempty, nextrow = minRVals(assignments, domains, unassigned, n, True)
        if not isempty:
            if backtrackingFCMRV(assignments, newdomains, unassigned, nextrow, n) != None:
                return assignments
        assignments.remove((row, col))
        unassigned.add(row)
    return None


def start(n):
    domains = {}
    unassigned = set()
    for i in range(n):
        unassigned.add(i)
        values = []
        for j in range(n):
            values.append(j)
        domains[i] = values
    return domains, unassigned

# printing and display of board is slightly off
def printBoard(assignments, size):
    if not assignments:
        print ("No solution")
        return
    board = createBoard(size)
    for i, j in assignments:
        board[i][j] = 'Q'
    for row in board:
        for i in row:
            print(str(i) + ' '),
        print("")


if __name__ == '__main__':
    # change n to set the number of queens
    n = 4
    assignments = set()
    domains, unassigned = start(n)
    # prints the locations of the queens
    print(backtrackingFCMRV(assignments, domains, unassigned, 0, n))
    #printBoard(assignments, n)


# For visual representation refer to JavaScript file attached in ZIP
