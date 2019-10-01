# Updates.py moet nog worden gecommend

import random
import sys
import time
import csv
from copy import deepcopy

import mxklabs.dimacs
from mxklabs.dimacs import Dimacs

from heuristics import heuristic1
from read import readin
from pure_literals import get_pure_literals
from init_truthvalues import initiate_truthvalues
from updates import update_clauses
from heuristics import heuristic2

# Initiate a dictionary to keep track of the truthvalues of all the literals.
# Contains only positive literals as keys, with True or False (or None if not assigned yet) as value.
truthvalues = {}

# Initiate variable to keep track of the number of splits.
number_of_splits = 0

# Initiate variable to check if a sudoku is solved.
solved = False


# Make a random decision which literal to give a truthvalue.
def random_choice(literals):
    new_choice = random.choice(literals)

    return new_choice


# Takes a literal that gets a truthvalue and updates the dictionary truthvalues.
def update_truthvalues(literal, truthvalues):
    lit = abs(literal)
    if lit == literal:
        truthvalues[lit] = True
    else:
        truthvalues[lit] = False


# The Davis Putnam algorithm searches for easy choices untill there are none left. When none are left,
# it runs an heuristic that decides which literal to give a truthvalue.
# This algorithm uses backtracking with those decisions.
def dp(clauses, truthvalues):

    # If an empty clause is found, the current SAT problem is unsolvable.
    if [] in clauses:
        return clauses, truthvalues, False

    # If the list of clauses is empty, we found a solution.
    elif not clauses:
        return clauses, truthvalues, True

    # Try to solve the SAT when the SAT is not solved yet and is still solvable.
    else:
        stuck = False
        # Make easy decisions while possible.
        while not stuck:
            possible = True
            while possible:
                # Check if the list of clauses contains an unit clause.
                # For the SAT to be solvable, the literal in the unit clause has to be true.
                for clause in [*clauses]:
                    if len(clause) == 1:
                        literal = clause[0]
                        update_truthvalues(literal, truthvalues)

                stuck = not update_clauses(clauses, truthvalues)
                possible = not stuck

            # Gets difference of negative and positive literals, which are the pure literals.
            list_of_pure_literals = get_pure_literals(clauses)

            # Update truthvalues with the pure literals.
            for literal in list_of_pure_literals:
                update_truthvalues(literal, truthvalues)

            # If a pure literal is found, empty the set for next usage and update the clauses.
            if list_of_pure_literals:
                list_of_pure_literals = []
            stuck = not update_clauses(clauses, truthvalues)

        if [] in clauses:
            return clauses, truthvalues, False

        elif not clauses:
            return clauses, truthvalues, True

        clauses_before_splitting = deepcopy(clauses)
        truthvalues_before_splitting = deepcopy(truthvalues)

        all_literals = []
        for literal in truthvalues:
            if truthvalues[literal] is None:
                all_literals.append(literal)

        if heuristic == "heuristic 1":
            choice = heuristic1(clauses_before_splitting)
        elif heuristic == "heuristic 2":
            choice = heuristic2(clauses_before_splitting)
        else:
            choice = random_choice(all_literals)

        global number_of_splits
        number_of_splits += 1

        update_truthvalues(choice, truthvalues)
        update_clauses(clauses_before_splitting, truthvalues_before_splitting)

        clauses, truthvalues, result = \
            dp(clauses, truthvalues)

        if result:
            return clauses, truthvalues, result

        update_truthvalues(-choice, truthvalues_before_splitting)

        return dp(clauses_before_splitting, truthvalues_before_splitting)


# Read in sudoku files and solve the sudokus one by one.
def main():

    # print("What file do you want to use as input?: ")
    # global SAT_problem_filename
    # SAT_problem_filename = input("Name: ")

    # print("What filename do you want to use for output?: ")
    # global SAT_solution_filename
    # SAT_solution_filename = input("Name: ")

    print("Which heuristic would you like to use?\n Type \"heuristic 1\" for the Moms,"
          " type \"heuristic2\" for the other one")
    global heuristic
    heuristic = input("Select: ")

    if heuristic != "heuristic 1" and heuristic != "heuristic 2":
        print("invalid input, split decisions will now be made random")

    start_time = time.time()

    # Open the file with SAT problems.

    # problem = mxklabs.dimacs.read(SAT_problem_filename)
    # solved = mxklabs.dimacs.read(SAT_solution_filename)

    # SAT_file = open(SAT_problem_filename, 'r')
    # file_contents = SAT_file.readlines()
    # unsolved = readin(file_contents)
    # print(unsolved)

    csvFile = open('output.csv', 'w')
    writer = csv.writer(csvFile)

    # for i in range(1, 9):
    global truthvalues
    truthvalues = {}

    global number_of_splits
    number_of_splits = 0

    global solved
    solved = False

    global result
    result = False

    global clauses
    clauses = []

    # sudoku_file = open('sudoku-example.txt', 'r')
    # sudoku_file = open('test_dimacs_general.txt', 'r')
    # sudoku_file = open('sudo2.txt', 'r')

    sudoku_file = open("sudo1.txt", 'r')
    file_contents = sudoku_file.readlines()
    sudoku_unsolved = readin(file_contents)

    # Open the file with sudoku rules (already in DIMAC notation).
    sudoku_rules = open('sudoku-rules.txt', 'r')
    rules = sudoku_rules.readlines()
    sudoku_rules.close()

    # Append the rules to the clauses.
    clauses = readin(rules)

    # Append the sudoku to the clauses.
    for filled_in in sudoku_unsolved:
        clauses.insert(0, filled_in)

    # Make dictionary to keep track of truth values of literals.
    initiate_truthvalues(clauses, truthvalues)

    # Check for tautologies in the clauses (only need to do this once).
    for clause in [*clauses]:

        # If tautology is found, remove the corresponding clause.
        for literal in clause:
            if -literal in clause:
                clauses.remove(clause)
                break

    # Run DP algorithm which checks for unit clauses and pure literals and makes a split when needed.
    clauses, truthvalues, result = dp(clauses, truthvalues)

    # If we found a solution and we have literals that don't have a value yet,
    # we can assign them a truthvalue randomly.
    if result:
        for literal in truthvalues:
            if truthvalues[literal] is None:
                truthvalues[literal] = random.choice([True, False])
        print("Satisfiable")
    else:
        print("Unsatisfiable")
    print(truthvalues)

    runtime = (time.time() - start_time)
    print("--- %s seconds ---" % runtime)
    print("number of splits: %i" % number_of_splits)

    writer.writerow([runtime, number_of_splits])
    csvFile.close()
    for literal in truthvalues:
        if truthvalues[literal] is True:
            print(literal)

# Call the main function


# Keep track of runtime.

main()
