from _pydecimal import Decimal

# import numpy as np


def heuristic1(clauses, truthvalues):
    # Jeroslow Wang
    # Count how many times all literals occur and then choose the most common for the split.

    choice = clauses[0][0]
    best_jw = 0
    for literal in truthvalues:
        if truthvalues[literal] is None:
            pos = 0
            neg = 0
            for clause in clauses:
                if literal in clause:
                    pos += Decimal(2 ** -len(clause))
                elif -literal in clause:
                    neg += Decimal(2 ** -len(clause))
            if (pos + neg) > best_jw:
                best_jw = pos + neg
                # choose the positive or negative literal? positive gives less backtracks.
                choice = literal
                # if pos >= neg:
                #     choice = literal
                # else:
                #     choice = -literal
    # print(best_jw)
    # print(choice)
    return choice

    # diction = {}
    # for clause in clauses:
    #     for literal in clause:
    #         if abs(literal) not in diction:
    #             diction[abs(literal)] = 1
    #         else:
    #             diction[abs(literal)] += 1
    # # print(diction)
    #
    # maxi = max(diction, key=diction.get)
    # # print(maxi)
    # return maxi


k = 1


def heuristic2(clauses):
    # count how many times all literals occur and then pick the highest value for the split.
    small_diction = {}
    pos_diction = {}
    neg_diction = {}
    extra_list = []
    min_length = len(min(clauses, key=len))
    for clause in clauses:
        if len(clause) == min_length:
            for literal in clause:
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
        score = (pos_count + neg_count) * 2 ** k + pos_count * neg_count
        small_diction[literal] = score

    if not small_diction:
        return clauses[0][0]

    choice = max(small_diction, key=small_diction.get)
    return choice

