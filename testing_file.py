import pset2mcq_bank 

layout = \
    [(2, 0, 1, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q", "r"])]

bank_factor = 2

question_lsts = []

for (n_question, min_depth, max_depth, connectives, prop_vars) in layout:

    question_lst = pset2mcq_bank.q1mcq( \
        true=n_question*bank_factor//2,\
        false=n_question*bank_factor//2,\
        min_depth=min_depth,\
        max_depth=max_depth,\
        connectives=None,\
        prop_vars=prop_vars)

    question_lsts.append(question_lst)

print(question_lsts)