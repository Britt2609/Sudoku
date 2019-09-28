# Give all literals truthvalue None.
def initiate_truthvalues(clauses, truthvalues):
    for clause in clauses:
        for literal in clause:
            if abs(literal) not in truthvalues:
                truthvalues[abs(literal)] = None
