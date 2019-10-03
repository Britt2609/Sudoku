# Updates.py moet nog worden gecommend

import random
import time
import csv
from copy import deepcopy

from heuristics import heuristic1, heuristic2
from io_tools import read_sudokus, read_dimacs
from pure_literals import get_pure_literals
from updates import update_clauses, update_truthvalues


# Make a random decision which literal to give a truthvalue.
def random_choice(literals):
    new_choice = random.choice(literals)
    return new_choice


class Satisfier():

    def __init__(self):
        self.number_of_splits = 0
        self.number_of_backtracks = 0
        self.number_of_simplifications = 0

    def solve(self, clauses, truthvalues):
        # Check for tautologies in the clauses (only need to do this once).
        for clause in [*clauses]:
            # If tautology is found, remove the corresponding clause.
            for literal in clause:
                if -literal in clause:
                    clauses.remove(clause)
                    break
        return self.dp(clauses, truthvalues)

    # The Davis Putnam algorithm searches for easy choices untill there are none left. When none are left,
    # it runs an heuristic that decides which literal to give a truthvalue.
    # This algorithm uses backtracking with those decisions.
    def dp(self, clauses, truthvalues):

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
                self.number_of_simplifications += 1
                possible = True
                while possible:
                    # Check if the list of clauses contains an unit clause.
                    # For the SAT to be solvable, the literal in the unit clause has to be True.
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

            # If clauses contains an empty clause, the problem is unsatisfiable.
            if [] in clauses:
                return clauses, truthvalues, False

            # If clauses is empty, we found a solution so the problem is satisfiable.
            elif not clauses:
                return clauses, truthvalues, True

            # When we get here, it means there are no more 'simple' decisions, so we start splitting.
            # Keep track of previous clauses and truthvalues for when we need to backtrack.
            clauses_before_splitting = deepcopy(clauses)
            truthvalues_before_splitting = deepcopy(truthvalues)

            # Get the literals we need to choose from.
            all_literals = []
            for literal in truthvalues:
                if truthvalues[literal] is None:
                    all_literals.append(literal)

            # Check which heuristic is chosen, if input is invalid, choose random.
            if heuristic == "heuristic 1":
                choice = heuristic1(clauses_before_splitting, truthvalues)
            elif heuristic == "heuristic 2":
                choice = heuristic2(clauses_before_splitting)
            else:
                choice = random_choice(all_literals)
            self.number_of_splits += 1

            # Update the truthvalues and clauses with the new choice.
            update_truthvalues(choice, truthvalues)
            update_clauses(clauses_before_splitting, truthvalues_before_splitting)

            # Try to simplify again.
            clauses, truthvalues, result = \
                self.dp(clauses, truthvalues)

            # If the SAT is solved, return the values.
            if result:
                return clauses, truthvalues, result

            # If SAT not solved, first try the opposite from the last choice.
            # If that doesn't work, that means that we need to backtrack.
            update_truthvalues(-choice, truthvalues_before_splitting)

            self.number_of_backtracks += 1
            return self.dp(clauses_before_splitting, truthvalues_before_splitting)


# Read in sudoku files and solve the sudokus one by one.
def main():

    print("Which heuristic would you like to use?\n Type \"heuristic 1\" for the Jereslow Wang,"
          " type \"heuristic 2\" for the MOM\'s")
    global heuristic
    heuristic = input("Select: ")

    if heuristic != "heuristic 1" and heuristic != "heuristic 2":
        print("invalid input, split decisions will now be made random")

    # Open the file with SAT problems (like 'sudoku.txt').
    print("Which SAT problem do you want to solve? Please give the file name (in dimacs)")
    SAT_problem = input("Select: ")

    # Open file
    problem = read_dimacs(SAT_problem, 'r')

    # For experimenting
    sudokus = read_sudokus("1000 sudokus.txt")

    # Append the rules to the clauses (only for experimenting).
    rules = read_dimacs('sudoku-rules.txt')

    # Make csv file to get the data for experimenting.
    with open('output.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["runtime", "number_of_splits", "number_of_backtracks", "number_of_simplifications"])

    for problem in sudokus:
        # Make deepcopy for if we want to solve more SAT's at once.
        clauses = deepcopy(problem)
        rules_copy = deepcopy(rules)
        clauses.extend(rules_copy)

        # Make dictionary to keep track of truth values of literals.
        literals = list(set([abs(x) for c in clauses for x in c]))
        truthvalues = {lit: None for lit in literals}

        # Run DP algorithm which checks for unit clauses and pure literals and makes a split when needed.
        satisfier = Satisfier()
        start_time = time.time()
        _, truthvalues, result = satisfier.solve(clauses, truthvalues)
        runtime = time.time() - start_time
        number_of_splits = satisfier.number_of_splits
        number_of_backtracks = satisfier.number_of_backtracks
        number_of_simplifications = satisfier.number_of_simplifications

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

        print("--- %s seconds ---" % runtime)
        print("number of splits: %i" % number_of_splits)
        print("number of backtracks: %i" % number_of_backtracks)

        if number_of_splits != 0:
            with open('output.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([runtime, number_of_splits, number_of_backtracks, number_of_simplifications])
            # numb = 0
            # for literal in truthvalues:
            #     if truthvalues[literal] is True:
            #         print(literal)
            #         numb += 1


# Call the main function


# Keep track of runtime.

main()
