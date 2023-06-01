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
    st.session_state.students = st.session_state.course.get_users(enrollment_type=['student'])
    st.session_state.student_name_to_id = {s.name: s.id for s in st.session_state.students}

    st.session_state.columns = st.session_state.course.get_custom_columns()
    for col in st.session_state.columns:
        if col.title == 'Streamlit API':
            st.session_state.test_column = col

    st.session_state.sent_scores = False

    st.session_state.n_questions = 0

    st.session_state.bank_factor = 1
    st.session_state.layout = [
        (2, 0, 1, None, ["p", "q"]), \
        (2, 1, 2, None, ["p", "q"]), \
        (2, 2, 2, None, ["p", "q", "r"])
    ]

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

    st.session_state.answers = []

    n = 0
    for i, question_lst in enumerate(st.session_state.question_lsts):

        new_quiz_group = st.session_state.test_quiz.create_question_group(
            quiz_groups = [
                {
                    'pick_count': n_question,
                    'question_points': 1
                }
            ]
        )

        for j, (text, answer) in enumerate(question_lst):

            st.session_state.answers.append(answer)

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
            
            canvas_text = canvas_latex(text)

            if answer: canvas_answer = 100
            else: canvas_answer = 0

            new_question = st.session_state.test_quiz.create_question(question={
                'question_name': f'Question {n+1}',
                'question_text': canvas_text,
                'quiz_group_id': new_quiz_group.id,
                'question_type': 'text_only_question',
                # 'answers': [
                #     {
                #         'answer_text': 'Yes',
                #         'answer_weight': canvas_answer
                #     },
                #     {
                #         'answer_text': 'No',
                #         'answer_weight': 100-canvas_answer
                #     },
                #     ]
            }
            )

            print('Added New Question')
            n += 1
            st.session_state.n_questions += 1

if 'student_name' in st.session_state and len(st.session_state.student_name) != 0:
    try:
        input_id = st.session_state.student_name_to_id[st.session_state.student_name]
        for d in st.session_state.test_column.get_column_entries():
            if d.user_id == input_id:
                st.session_state.ColumnData = d
        # input_ColumnData.update_column_data(column_data={
        #     'content': int(input_ColumnData.content) + 1
        # })
    except KeyError:
        pass
    
st.text_input('Please input your name as written on bCourses', key='student_name', disabled = 'ColumnData' in st.session_state)

if 'student_name' in st.session_state and len(st.session_state.student_name) != 0 and 'ColumnData' not in st.session_state:
    st.write("We couldn't find a student on the bCourses roster by this name? Are you sure this is exactly as you full name is written on bCourses?")

if 'ColumnData' in st.session_state:
    st.write('')
    st.write('')
    n = 0
    for i, question_lst in enumerate(st.session_state.question_lsts):
        for j, (text, answer) in enumerate(question_lst):

            st.subheader(f'Question {n+1}')
            st.write(text)
            default_option = '---'
            student_answer = st.selectbox(
                'Your Answer', 
                options=[default_option, 'Yes', 'No'], key=f'{n}',
                label_visibility='collapsed',
                disabled = st.session_state.sent_scores 
                )
            st.write('')
            st.write('')
            st.write('')
            n += 1

    def submit_answers_button():
        overall_score = 0

        translation_table = {'Yes': True, 'No': False}
        
        for i in range(st.session_state.n_questions):
            student_answer = st.session_state[f'{i}']
            if student_answer in translation_table:
                if translation_table[student_answer] == st.session_state.answers[i]:
                    overall_score += 1
        
        print(overall_score)

        st.session_state.ColumnData.update_column_data(column_data={
            'content': overall_score
        })

        st.session_state.sent_scores = True
    st.button('Submit Answers', on_click=submit_answers_button)