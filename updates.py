# Update list of clauses with the new truthvalues.
# If we don't find any new literals to assign a truthvalue to, we set variable stuck on True.


def update_clauses(clauses, truthvalues):
    stuck = False
    for clause in [*clauses]:
        clause_not_removed = True

        # Remove clauses that contain a positive or negative literal that's True.
        # Remove the literals that are True from all clauses.
        for literal in [abs(literal) for literal in clause]:
            if truthvalues[literal] is True:
                if (literal in clause) & clause_not_removed:
                    stuck = True
                    clause_not_removed = False
                    clauses.remove(clause)

                elif (-literal in clause) & clause_not_removed:
                    stuck = True
                    clause.remove(-literal)

            elif truthvalues[literal] is False & clause_not_removed:
                if (-literal in clause) & clause_not_removed:
                    stuck = True
                    clause_not_removed = False
                    clauses.remove(clause)
                elif (literal in clause) & clause_not_removed:
                    stuck = True
                    clause.remove(literal)

    return stuck


# Takes a literal that gets a truthvalue and updates the dictionary truthvalues.
def update_truthvalues(literal, truthvalues):
    lit = abs(literal)
    if lit == literal:
        truthvalues[lit] = True
    else:
        truthvalues[lit] = False

    lite = lit
