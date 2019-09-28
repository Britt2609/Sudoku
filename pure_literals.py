def get_pure_literals(clauses):
    negative_literals = []
    positive_literals = []
    for clause in clauses:
        for literal in clause:

            # Get list of negative literals and list of positive literals which are currently in the list of clauses.
            if literal < 0:
                if abs(literal) not in negative_literals:
                    negative_literals.append(abs(literal))
            else:
                if literal not in positive_literals:
                    positive_literals.append(literal)

    # Get the difference of the lists
    list_difference = list(set(positive_literals) ^ set(negative_literals))
    # for i in positive_literals + negative_literals:
    #     if i > 0:
    #         if i not in positive_literals or -i not in negative_literals:
    #             list_difference.append(i)
    #     else:
    #         if -i not in positive_literals or i not in negative_literals:
    #             list_difference.append(i)

    return list_difference
