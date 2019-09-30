def get_pure_literals(clauses):
    negative_literals = []
    positive_literals = []
    for clause in clauses:
        for literal in clause:

            # Get list of negative literals and list of positive literals which are currently in the list of clauses.
            if literal < 0:
                if abs(literal) not in negative_literals:
                    negative_literals.append(abs(literal))
                    test = abs(literal)
            else:
                if literal not in positive_literals:
                    positive_literals.append(literal)

    # Get the difference of the lists
    list_difference = list(set(positive_literals) ^ (set(negative_literals)))

    return list_difference
