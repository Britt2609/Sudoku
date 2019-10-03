from _pydecimal import Decimal


# Two-sided Jeroslow Wang heuristic.
# For every literal take J(I) = sum of (2 to the power -(number of occurrences)).
# Then take the highest value of J(I)+J(-I) and choose the most occurring of I and -I.
def heuristic1(clauses, truthvalues):
    choice = clauses[0][0]
    best_total = 0
    for literal in truthvalues:
        if truthvalues[literal] is None:
            pos_score = 0
            neg_score = 0
            for clause in clauses:
                if literal in clause:
                    pos_score += Decimal(2 ** -len(clause))
                elif -literal in clause:
                    neg_score += Decimal(2 ** -len(clause))
            # Keep track of the best score.
            if (pos_score + neg_score) > best_total:
                best_total = pos_score + neg_score
                # Choose the positive or negative literal (the most occuring).
                if pos_score >= neg_score:
                    choice = literal
                else:
                    choice = -literal
    return choice


    # MOM's heuristic
    # Take the smallest clauses and count how many times all literals occur.
    # Then pick the most occurring for the split.
def heuristic2(clauses):
    k = 2
    small_diction = {}
    pos_diction = {}
    neg_diction = {}
    extra_list = []

    # Get the length of the smallest clauses
    min_length = len(min(clauses, key=len))
    for clause in clauses:
        if len(clause) == min_length:
            for literal in clause:
                # Count the number of occurrences for every positive and negative literal
                if literal > 0:
                    if literal not in pos_diction:
                        extra_list.append(literal)
                        pos_diction[literal] = 1
                    else:
                        pos_diction[literal] += 1
                else:
                    if literal not in neg_diction:
                        extra_list.append(-literal)
                        neg_diction[-literal] = 1
                    else:
                        neg_diction[-literal] += 1
    for literal in extra_list:
        pos_count = pos_diction[literal] if literal in pos_diction else 0
        neg_count = neg_diction[literal] if literal in neg_diction else 0
        # Calculate the scores per pair of positive and negative literal.
        score = (pos_count + neg_count) * 2 ** k + pos_count * neg_count
        small_diction[literal] = score

    if not small_diction:
        return clauses[0][0]

    # Choose the literal with the best score.
    choice = max(small_diction, key=small_diction.get)
    return choice

