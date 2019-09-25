def get_pure_literals(clauses):
    negative_literals = []
    positive_literals = []
    for clause in clauses:
        for literal in clause:

            # put negative literal in set of negative literals
            if literal < 0:
                if literal not in negative_literals:
                    negative_literals.append(literal)

            # put positive literal in set of positive literals
            else:
                if literal not in positive_literals:
                    positive_literals.append(literal)

    list_difference = []
    for i in positive_literals + negative_literals:
        if i > 0:
            if i not in positive_literals or -i not in negative_literals:
                list_difference.append(i)
        else:
            if -i not in positive_literals or i not in negative_literals:
                list_difference.append(i)

    return list_difference
