import streamlit as st
from canvasapi import Canvas
import pset2mcq_bank

# Canvas API URL
API_URL = "https://bcourses.berkeley.edu/"
# Canvas API key
API_KEY = st.secrets["API_KEY"]
# Canvas Course Number
course_number = 1513858

########################
## INITIALIZE SESSION ##
########################

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
    
    st.session_state.answers = []

    for (n_question, min_depth, max_depth, connectives, prop_vars) in st.session_state.layout:

        question_lst = pset2mcq_bank.q1mcq( \
            true=n_question*st.session_state.bank_factor//2,\
            false=n_question*st.session_state.bank_factor//2,\
            min_depth=min_depth,\
            max_depth=max_depth,\
            connectives=None,\
            prop_vars=prop_vars)
        
        for text, answer in question_lst:
            st.session_state.answers.append(answer)
            st.session_state.n_questions += 1

        st.session_state.question_lsts.append(question_lst)

################
## NAME INPUT ##
################

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

#######################
## DISPLAY QUESTIONS ##
#######################

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

    #########################################
    ## SUBMIT, GRADE, AND SEND TO BCOURSES ##
    #########################################

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