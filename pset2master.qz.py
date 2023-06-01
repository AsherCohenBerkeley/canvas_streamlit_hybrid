from pyquiz import *

import pset2frq_bank, pset2mcq_bank

begin_quiz(
    title="Problem Set 2 (Multiple Choice)",
    description=rf"This problem set is a graded quiz. There is no time limit. You have as many attempts as you want but you must submit your final answers by the due date. On each new attempt, you will be shown a different set of questions. Your highest score will be graded.",
    quiz_type = "assignment",
    # unlimited attempts
    allowed_attempts = -1
)

#QUESTION 1

layout = \
    [(2, 0, 1, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q", "r"])]

bank_factor = 40

#Introduction
begin_text_only_question()
text("Which of the following are valid consequences?")
end_question()

for (n_question, min_depth, max_depth, connectives, prop_vars) in layout:
    begin_group(pick_count=n_question, points=1)
    pset2mcq_bank.q1mcq( \
        true=n_question*bank_factor//2,\
        false=n_question*bank_factor//2,\
        min_depth=min_depth,\
        max_depth=max_depth,\
        connectives=None,\
        prop_vars=prop_vars)
    end_group()

print("Done generating question 1 (MCQ)")

#QUESTION 2

#Introduction
begin_text_only_question()
text("Which of the following pairs of formulas are logically equivalent?")
end_question()

#Choose layout of question
#i.e. first 5 questions: depth 2, prop_vars p and q; next 5 questions: depth 3, prop_vars p, q, and r
layout = \
    [(2, 0, 1, ["p", "q"]), \
    (2, 2, 2, ["p", "q"]), \
    (2, 2, 2, ["p", "q", "r"])]

#bank_factor = (number of questions in bank) / (number of questions displayed)
bank_factor = 20

#Create questions as detailed in layout
for (n_question, min_depth, max_depth, prop_vars) in layout:
    begin_group(pick_count=n_question, points=1)
    #bank_factor = (number of questions in bank) / (number of questions displayed)
    pset2mcq_bank.q2mcq( \
        n_valid=n_question*bank_factor//2, \
        n_invalid=n_question*bank_factor//2, \
        min_depth=min_depth, \
        max_depth=max_depth, \
        connectives=None, \
        prop_vars=prop_vars)
    end_group()

print("Done generating question 2 (MCQ)")

#QUESTION 3

#Introduction
begin_text_only_question()
text("Which of the following are tautologies?")
end_question()

#Choose layout of question
#i.e. first 5 questions: depth 2, prop_vars p and q; next 5 questions: depth 3, prop_vars p, q, and r
layout = \
    [(2, 2, 2, None, ["p", "q"]), \
    (2, 2, 2, None, ["p", "q", "r"])]

#bank_factor = (number of questions in bank) / (number of questions displayed)
bank_factor = 40

#Create questions as detailed in layout
for (n_question, min_depth, max_depth, connectives, prop_vars) in layout:
    begin_group(pick_count=n_question, points=1)
    #bank_factor = (number of questions in bank) / (number of questions displayed)
    pset2mcq_bank.q3mcq( \
        n_valid=n_question*bank_factor//2, \
        n_invalid=n_question*bank_factor//2, \
        min_depth=min_depth, \
        max_depth=max_depth, \
        connectives=connectives, \
        prop_vars=prop_vars)
    end_group()

print("Done generating question 3 (MCQ)")

#QUESTION 4

#Introduction
begin_text_only_question()
text("Which of the following are satisfiable?")
end_question()

#Choose layout of question
#i.e. first 5 questions: depth 2, prop_vars p and q; next 5 questions: depth 3, prop_vars p, q, and r
layout = \
    [(1, 1, 2, None, ["p", "q", "r"]),
    (3, 2, 3, None, ["p", "q", "r"])]

#bank_factor = (number of questions in bank) / (number of questions displayed)
bank_factor = 40

#Create questions as detailed in layout
for (n_question, min_depth, max_depth, connectives, prop_vars) in layout:
    begin_group(pick_count=n_question, points=1)
    #bank_factor = (number of questions in bank) / (number of questions displayed)
    pset2mcq_bank.q4mcq( \
        n_valid=n_question*bank_factor//2, \
        n_invalid=n_question*bank_factor//2, \
        min_depth=min_depth, \
        max_depth=max_depth, \
        connectives=connectives, \
        prop_vars=prop_vars)
    end_group()

print("Done generating question 4 (MCQ)")

#QUESTION 5

#Introduction
begin_text_only_question()
text("The following are verbatim questions from practice LSAT exams (mostly taken from the Law School Admission Council, the Manhattan Review, or CrackLSAT.net). These so-called 'analytical reasoning' problems are really just logic puzzles in disguise. Try your hand at solving them.")
end_question()

pset2mcq_bank.q5mcq(pick_count=2, points=2)

print("Done generating question 5 (MCQ)")

end_quiz()

"---------------------------------------------------------------------------------------------------"

begin_quiz(
    title="Problem Set 2 (Free Response)",
    description=rf"This problem set is a graded quiz. You may take the quiz only once. There is no time limit, but you must submit your final answers by the due date.",
    quiz_type = "assignment",
    # only one attempt
    allowed_attempts = 1
)

#Intro
print('')
print('')
print('')
print('')
print('')
pdf_url = input(\
            """Please upload the LaTeX cheatsheet to the "Files" page of the bCourse for this class. Then, when you click on the title of the PDF in files, you should see a preview of the PDF.\nIn the search bar, you should find a URL like: \n'https://bcourses.berkeley.edu/courses/___________________' \n\nCopy the entire URL and paste it here.\n""")

begin_text_only_question()
text(\
    rf"""<p>From here on out, for your multiple choice responses, we strongly recommend you use a typesetting software called LaTeX. For those of you who don't know, LaTeX is a very famous typesetting software for mathematical expressions. It's the tool of choice for professional math and science researchers around the world when it comes to incorporating mathematical expressions into typed text. </p>
    <p>LaTeX has become so widespread that if you ever plan on engaging with STEM during your career, chances are you'll have to become familiar with LaTeX eventually, so in our opinion, you might as well start learning it now. But if you've never heard of LaTeX before, do not worry. It is a relatively simple software to get the hang of. The more you practice, the more comfortable you will become. And trust us, it really will upgrade the aesthetics of your answers tenfold.</p>
    <p>For your convenience, we've written a <a href={pdf_url}>LaTeX cheatsheet</a> designed specifically for this course. All of the important logical expressions are organized by the week at which you'll be learning them. On each line, you'll first see a LaTeX command followed by a picture of the output that LaTeX command would generate.</p>
    <p>To use LaTeX in a multiple choice question response box on bCourses, simply go to Insert>Equation and then make sure "Directly edit LaTeX" is checked. Then write the commands you'd like to implement (you should see the corresponding pictures autogenerate underneath) and then click "Done".</p>
    <p>If you ever have any questions about how to use LaTeX, please feel free to consult the course staff on either Ed Discussion or office hours. We really hope you come to love this amazing mathematical tool.</p>""")
end_question()

#QUESTION 0

bank_factor = 100

begin_group(pick_count=1, points=1)
for i in range(bank_factor):
    pset2frq_bank.q0frq()
end_group()

print("Done generating question 0 (FRQ)")

#QUESTION 1

#Intro
begin_text_only_question()
text(\
    rf"<p>Translate each of the following English sentences into our formal propositional language. Make sure to provide a key of what your propositions $p$, $q$, $r$, $s$, $p_1$, $p_2$ etc. stand for. </p><p>We recommend you read the discussion of 'only if' at the end of Section 2.5 of <i>Logic in Action</i>, before completing these problems. In the textbook, there is also talk about ambiguity in the term 'unless.' In this course, unless otherwise specified, a sentence like $p$ unless $q$ always corresponds semantically to the formula ${pset2frq_bank.nltk_to_latex_prop('(-p -> q)')}$ in our formal language. </p><p>Finally, as you saw in the previous exercise, the phrase 'it's not the case that' can sometimes lead to ambiguity. Thus, in this exercise, we set the convention that the phrase 'it's not the case that __' always modifies the truth value of the claim immediately following it and nothing more. In other words, a sentence like 'it's not the case that it's sunny, if and only if the weather is bad.' would correspond to a formula like ${pset2frq_bank.nltk_to_latex_prop('(-p <-> q)')}$ where $p$ means 'it's sunny' and $q$ means 'the weather is bad.'</p>")
end_question()

layout = [\
    (2, 5),
]

bank_factor = 100

for (pick_count, n_sentence) in layout:
    begin_group(pick_count=pick_count, points=n_sentence)
    for i in range(bank_factor*pick_count):
        pset2frq_bank.q1frq(n_sentence)
    end_group()

print("Done generating question 1 (FRQ)")

#QUESTION 2

#Intro
begin_text_only_question()
text(rf"For each of the following English arguments, represent the form of the argument using a set of formulas for the premises and a single formula as the conclusion. Then indicate whether the form of argument is valid.")
end_question()

layout = [\
    (3, 3),
]

bank_factor = 40

for (pick_count, n_premise) in layout:
    begin_group(pick_count=pick_count, points=2)
    pset2frq_bank.q2frq(\
        n_premise=n_premise,\
        n_valid = pick_count*bank_factor//2,\
        n_invalid = pick_count*bank_factor//2
            )
    end_group()

print("Done generating question 2 (FRQ)")

#QUESTION 3

#No intro

layout = [\
    (1, 2, 2, ["p", "q"]),
    (1, 3, 3, ["p", "q", "r"])
]

bank_factor = 100

for (pick_count, min_depth, max_depth, prop_vars) in layout:
    begin_group(pick_count=pick_count, points=2)
    for i in range(bank_factor):
        pset2frq_bank.q3frq(\
            min_depth=min_depth,\
            max_depth=max_depth,\
            prop_vars=prop_vars)
    end_group()

print("Done generating question 3 (FRQ)")

#QUESTION 4

#No intro

layout = [\
    (1, 2, 2, 2),
    (2, 3, 3, 3)
]

bank_factor = 50

for (pick_count, min_depth, max_depth, n_letters) in layout:
    begin_group(pick_count=pick_count, points=2)
    pset2frq_bank.q4frq(\
        n_questions = pick_count*bank_factor, \
        min_depth=min_depth,\
        max_depth=max_depth,\
        n_letters=n_letters)
    end_group()

print("Done generating question 4 (FRQ)")

#QUESTION 5

begin_group(pick_count=1, points=0)
begin_essay_question()
text(r"<p>(EXTRA CREDIT +4 points at most) On the duality between $\wedge$ and $\vee$. </p><p>Given a formula $\phi$ whose only connectives are $\neg$, $\wedge$, and $\vee$, let $\phi^{\ast}$ be the result of interchanging $\wedge$ and $\vee$ and replacing each proposition letter by its negation. More formally, we recursively define a function $(\cdot)^{\ast}$ on the set of formulas whose only connectives are $\neg$, $\wedge$, and $\vee$ as follows.</p><p><ul><li>for any atomic formula $p$, $p^{\ast} = \neg p$</li><li>$(\neg \phi)^{\ast} = \neg(\phi^{\ast})$</li><li>$(\phi \wedge \psi)^{\ast} = (\phi^{\ast} \vee \psi^{\ast})$</li><li>$(\phi \vee \psi)^{\ast} = (\phi^{\ast} \wedge \psi^{\ast})$</li></ul> </p><p>Use induction and the semantics of propositional logic to show that, for any formula $\phi$ whose only connectives are $\neg$, $\wedge$, and $\vee$, $\phi^{\ast}$ is logically equivalent to $\neg \phi$.</p>")
comment_general(r"<p>Rubric</p><p><ul><li>$+1$ point for mentioning base case</li><li>$+1$ point for outlining three inductive steps (one for $\neg$, $\wedge$, and $\vee$)</li><li>$+1$ point for trying to use valuations/semantics</li><li>$+1$ point for successfully using valuations/semantics</li></ul></p>")
end_question()
end_group()

print("Done generating question 5 (FRQ)")

end_quiz()
