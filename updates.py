# update list of clauses
def update_clauses(clauses, truthvalues):
    changed = False
    for clause in [*clauses]:
        # print(clause)
        # print(clauses)
        clause_not_removed = True

        for literal in [*truthvalues]:

            if truthvalues[literal] is True:
                if (literal in clause) & clause_not_removed:
                    changed = True
                    clauses.remove(clause)
                    clause_not_removed = False

                elif (-literal in clause) & clause_not_removed:
                    changed = True
                    clause.remove(-literal)

            elif truthvalues[literal] is False & clause_not_removed:
                if (-literal in clause) & clause_not_removed:
                    changed = True
                    clauses.remove(clause)
                    clause_not_removed = False
                elif (literal in clause) & clause_not_removed:
                    changed = True
                    clause.remove(literal)

    return changed


def update_literals(literal, negative_literals, positive_literals, all_literals):

    if literal in all_literals:
        all_literals.remove(literal)
    if -literal in all_literals:
        all_literals.remove(-literal)
    if literal in negative_literals:
        negative_literals.remove(literal)
    if -literal in negative_literals:
        negative_literals.remove(-literal)
    if literal in positive_literals:
        positive_literals.remove(literal)
    if -literal in positive_literals:
        positive_literals.remove(-literal)

