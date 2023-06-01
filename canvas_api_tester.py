from canvasapi import Canvas

# Canvas API URL
API_URL = "https://bcourses.berkeley.edu/"
# Canvas API key
API_KEY = "1072~V9Z8obSxt9LM1sQTn717w6JeSBHpzc2UQrT2AqQDGK8wt2d7MczMCf6eevvH4ghO"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Test getting a course
course = canvas.get_course(1513858)
print('Fetched Course')
# print('Course Title', course.name)
# print('')

# # Test getting users
# users = course.get_users(enrollment_type=['student'])
# for user in users:
#     print('User:', user)
# print('')

# # Test getting assignments
# assignments = course.get_assignments()
# for assignment in assignments:
#     print(assignment)

quizzes = course.get_quizzes()
for quiz in quizzes:
    if quiz.title == 'New Test Quiz':
        test_quiz = quiz

test_quiz.delete()

print('Deleted Old Quiz')

test_quiz = course.create_quiz(quiz={
    'title': "New Test Quiz",
    'description': "This is a test to see if the Canvas API is working properly.",
    'quiz_type': 'assignment',
    'allowed_attempts': -1,
    'scoring_policy': 'keep_highest',
    'published': False
})

print('Created New Quiz')

import pset2mcq_bank 

layout = \
    [(2, 0, 1, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q", "r"])]

bank_factor = 2

for (n_question, min_depth, max_depth, connectives, prop_vars) in layout:

    new_quiz_group = test_quiz.create_question_group(
        quiz_groups = [
            {
                'pick_count': n_question,
                'question_points': 1
            }
        ]
    )

    print('Created New Quiz Group')

    question_lst = pset2mcq_bank.q1mcq( \
        true=n_question*bank_factor//2,\
        false=n_question*bank_factor//2,\
        min_depth=min_depth,\
        max_depth=max_depth,\
        connectives=None,\
        prop_vars=prop_vars)
    
    print('Generated Questions')

    for (text, answer) in question_lst:

        def canvas_latex(string):
            def aux(string, n):
                if len(string) == 0:
                    return ''
                first = string[0]
                rest = string[1:]
                if first == '$':
                    if n % 2 == 0:
                        return '\(' + aux(rest, n+1)
                    else:
                        return '\)' + aux(rest, n+1)
                else:
                    return first + aux(rest, n)
            return aux(string, 0)
        
        text = canvas_latex(text)

        if answer: answer = 100
        else: answer = 0

        new_question = test_quiz.create_question(question={
            'question_text': text,
            'quiz_group_id': new_quiz_group.id,
            'question_type': 'multiple_choice_question',
            'answers': [
                {
                    'answer_text': 'Yes',
                    'answer_weight': answer
                },
                {
                    'answer_text': 'No',
                    'answer_weight': 100-answer
                },
                ]
        }
        )

        print('Added New Question')