import streamlit as st
from canvasapi import Canvas
import pset2mcq_bank

# Canvas API URL
API_URL = "https://bcourses.berkeley.edu/"
# Canvas API key
API_KEY = st.secrets["API_KEY"]
# Canvas Course Number
course_number = 1513858

if 'canvas' not in st.session_state:
    st.session_state.canvas = Canvas(API_URL, API_KEY)
    st.session_state.course = st.session_state.canvas.get_course(course_number)
    print('Fetched Course')
    st.session_state.quizzes = st.session_state.course.get_quizzes()

    st.session_state.bank_factor = 2
    st.session_state.layout = \
    [(2, 0, 1, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q", "r"])]

    st.session_state.question_lsts = []

    for (n_question, min_depth, max_depth, connectives, prop_vars) in st.session_state.layout:

        question_lst = pset2mcq_bank.q1mcq( \
            true=n_question*st.session_state.bank_factor//2,\
            false=n_question*st.session_state.bank_factor//2,\
            min_depth=min_depth,\
            max_depth=max_depth,\
            connectives=None,\
            prop_vars=prop_vars)

        st.session_state.question_lsts.append(question_lst)

    for quiz in st.session_state.quizzes:
        if quiz.title == 'New Test Quiz':
            quiz.delete()
            print('Deleted Old Quiz')

    st.session_state.test_quiz = st.session_state.course.create_quiz(quiz={
        'title': "New Test Quiz",
        'description': "This is a test to see if the Canvas API is working properly.",
        'quiz_type': 'assignment',
        'allowed_attempts': -1,
        'scoring_policy': 'keep_highest',
        'published': False
    })

    print('Created New Quiz')

layout = \
    [(2, 0, 1, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q"]), \
    (2, 2, 3, None, ["p", "q", "r"])]

bank_factor = 2

n = 1
for i, question_lst in enumerate(st.session_state.question_lsts):

    # new_quiz_group = test_quiz.create_question_group(
    #     quiz_groups = [
    #         {
    #             'pick_count': n_question,
    #             'question_points': 1
    #         }
    #     ]
    # )

    for j, (text, answer) in enumerate(question_lst):

        # def canvas_latex(string):
        #     def aux(string, n):
        #         if len(string) == 0:
        #             return ''
        #         first = string[0]
        #         rest = string[1:]
        #         if first == '$':
        #             if n % 2 == 0:
        #                 return '\(' + aux(rest, n+1)
        #             else:
        #                 return '\)' + aux(rest, n+1)
        #         else:
        #             return first + aux(rest, n)
        #     return aux(string, 0)
        
        # text = canvas_latex(text)

        # if answer: answer = 100
        # else: answer = 0

        # new_question = test_quiz.create_question(question={
        #     'question_text': text,
        #     'quiz_group_id': new_quiz_group.id,
        #     'question_type': 'multiple_choice_question',
        #     'answers': [
        #         {
        #             'answer_text': 'Yes',
        #             'answer_weight': answer
        #         },
        #         {
        #             'answer_text': 'No',
        #             'answer_weight': 100-answer
        #         },
        #         ]
        # }
        # )

        # print('Added New Question')

        st.subheader(f'Question {n}')
        st.write(text)
        default_option = '---'
        student_answer = st.selectbox('Your Answer', options=[default_option, 'Yes', 'No'], key=f'{n}')
        translation_table = {'Yes': True, 'No': False}
        if student_answer != default_option:
            if translation_table[student_answer] == answer:
                st.write('Yay! Correct!')
            else:
                st.write("Unfortunately, that's wrong.")
        st.write('')
        st.write('')
        st.write('')
        n += 1