def initiate_truthvalues(clauses, truthvalues):
    for clause in clauses:
        for literal in clause:
            # put negative literal in set of negative literals
            if abs(literal) not in truthvalues:
                truthvalues[abs(literal)] = None
