def get_pure_literals(clauses):
    negative_literals = set()
    positive_literals = set()
    for clause in clauses:
        for literal in clause:

            # Get list of negative literals and list of positive literals which are currently in the list of clauses.
            if literal < 0:
                # if abs(literal) not in negative_literals:
                negative_literals.add(abs(literal))
            else:
                # if literal not in positive_literals:
                positive_literals.add(literal)

    # Get the difference of the lists
    disjunction = positive_literals ^ negative_literals
    list_difference = []
    for literal in disjunction:
        if literal in negative_literals:
            list_difference.append(-literal)
        else:
            list_difference.append(literal)

    return list_difference
