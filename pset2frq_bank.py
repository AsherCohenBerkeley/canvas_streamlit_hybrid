from tabulate import tabulate # you need tabulate to render the truth tables

from pyquiz import *
from pyquiz.expr import *

import random

from nltk import Prover9, Mace, Prover9Command
from nltk.test.inference_fixt import setup_module 

from nltk.sem.drt import DrtParser
from nltk.sem import logic
logic._counter._value = 0

from nltk.sem import Expression
read_expr = Expression.fromstring

Prover9.config_prover9(Prover9, r'/Users/ashercohen/bin')
Mace.config_prover9(Mace, r'/Users/ashercohen/bin')

alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]

l_to_n_dict = {
    "\\leftrightarrow" : "<->",
    "\\to" : "->",
    "\\rightarrow" : "->",
    "\\wedge" : "&",
    "\\vee": "|",
    "\\neg": "-"
}

n_to_l_dict = {value: key for (key, value) in l_to_n_dict.items()}

def latex_to_nltk_prop(latex):
    #Initialize output
    output = latex
    #Replace various strings (paying attention to spaces)
    # "p\wedge q" and "p \wedge q" both get sent to "p & q"
    for (key, value) in l_to_n_dict.items():
        output = output.replace(" " + key, " " + value)
        output = output.replace(key, " " + value)
    #Return
    return output

def nltk_to_latex_prop(nltk):
    #Initialize output
    output = nltk
    #Replace various strings (paying attention to spaces)
    for (key, value) in n_to_l_dict.items():
        output = output.replace(" " + key + " ", " " + value + " ")
        output = output.replace(key + " ", " " + value + " ")
        output = output.replace(" " + key, " " + value + " ")
        output = output.replace(key, " " + value + " ")
    #Return
    return output

def random_prop_frml(min_depth = 2, max_depth = 3, connectives = None, prop_vars = None):

    """Returns random propositional formula in nltk syntax"""

    if connectives == None:
        connectives = ['-', '&', '|', '->', '<->']

    if prop_vars == None:
        prop_vars = ["p","q"]

    #bias towards more complicated formulas
    n = random.randint(min_depth, max_depth)

    #recursive call
    if n == 0:
        return random.choice(prop_vars)
    else:
        con = random.choice(connectives)
        if con == '-':
            sub_form = random_prop_frml(max(0,min_depth-1), max_depth-1, connectives, prop_vars)
            return '-' + sub_form
        else:
            sub_form1 = random_prop_frml(max(0,min_depth-1), max_depth-1, connectives, prop_vars)
            sub_form2 = random_prop_frml(max(0,min_depth-1), max_depth-1, connectives, prop_vars)
            return '(' + sub_form1 + con + sub_form2 + ')'

corpus = [\
    """
104 The water tastes cold
105 The animals drink their water
106 The animals go wild
107 The animals leave the barn""",\
#    """
#123 They tell him to write the letter
#124 They force him into writing the letter
#125 They leave the room
#126 He reveals the bad news""",\
    """
    | The boss is happy
    | The employees are happy
    | The shareholders are happy
    | The public is happy""",\
#    """The crowds cheer in the streets
#152 The streets fill with people
#153 The government is excited
#155 The crisis comes to an end  """,\
#    """You hear animals roaring in the meadows
#156 The fields are full of animals 
#157 You hear birds chirping in the woods 
#159 You enjoy life in the jungle""", \
    """He breaks his arm
156 He is in the hospital
157 He feels sick
159 He takes the week off work""", \
    """The yeast is alive
156 The cake rises
157 The dough is salted
159 The children are happy""", \
    """She listens to music
156 She meditates
157 She has a good night's sleep
159 She eats well during the day""", \
    """They like ink pens
156 They like chalk
157 They like styluses
159 They like whiteboard markers""", \
    ]

digits = [chr(ord("0")+i) for i in range(ord("9")+1-ord("0"))]

mod_corpus = []

for topic in corpus:
    topic = topic.replace("\n", "")
    for digit in digits:
        topic = topic.replace(digit, "|")
    sents = topic.split("|")
    temp_sents = []
    for sent in sents:
        while True:
            if len(sent) > 0 and sent[0] == " ": 
                sent = sent[1:]
            else:
                break
        while True:
            if len(sent) > 0 and sent[-1] == " ":
                sent = sent[:-1]
            else:
                break
        temp_sents.append(sent)
    sents = [sent for sent in temp_sents if sent != ""]
    mod_corpus.append(sents)

english_trlns = {
    "<->": ["%s if and only if %s", "%s just in case %s"],
    "->": ["if %s, then %s", "%s only if %s"],
    "&": ["%s, and %s"],
    "|": ["%s, or %s"],
    "-": ["it's not the case that %s"]
}

english_to_nltk = {"%s, unless %s": "(-%s -> %s)"}

for (key, value) in english_trlns.items():
    for phrase in value:
        if key != "-": english_to_nltk[phrase] = f"(%s {key} %s)"
        else: english_to_nltk[phrase] = "-%s"

def english_trans(form,atom_trnls):
    if len(form) == 1:
        return atom_trnls[form]
    elif len(form) == 2:
        return random.choice(english_trlns["-"]) % english_trans(form[1:],atom_trnls=atom_trnls)
    else:
        form = form[1:-1]
        for sym in english_trlns.keys():
            i = form.find(sym)
            if i != -1:
                return random.choice(english_trlns[sym]) % \
                    (english_trans(form[:i], atom_trnls=atom_trnls),\
                    english_trans(form[i+len(sym):], atom_trnls=atom_trnls))

class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Node({(self.value.__repr__())}, {(self.left.__repr__())}, {(self.right.__repr__())})"
    def nltk(self):
        if self.left == None:
            if self.right == None:
                return self.value
            return f'-{self.right.nltk()}'
        return f'({self.left.nltk()}{self.value}{self.right.nltk()})'

def random_tree_english(min_depth=0, max_depth=1, unary_node=None, binary_node=None, leaf=None):
    if unary_node == None: unary_node = english_trlns["-"]
    if binary_node == None:
        binary_node = []
        for (key, value) in english_trlns.items():
            if key != "-": binary_node += value
        binary_node.append("%s, unless %s")
    if leaf == None:
        leaf = ["p", "q", "r"]
    n = random.randint(min_depth, max_depth)
    if n == 0:
        return Node(random.choice(leaf), None, None)
    else:
        value = random.choice(unary_node+binary_node)
        if value in unary_node: 
            return Node(value, \
                None, \
                random_tree_english(max(0, min_depth-1), max_depth-1, unary_node, binary_node, leaf))
        else:
            return Node(value, \
                random_tree_english(max(0, min_depth-1), max_depth-1, unary_node, binary_node, leaf), \
                random_tree_english(max(0, min_depth-1), max_depth-1, unary_node, binary_node, leaf))

unary_conn = ["-"]
binary_conn = ["&","|","->","<->"]

def random_tree(min_depth=0, max_depth=1, unary_node=None, binary_node=None, leaf=None):
    if unary_node == None: unary_node = unary_conn
    if binary_node == None: binary_node = binary_conn
    if leaf == None:
        leaf = ["p", "q", "r"]
    n = random.randint(min_depth, max_depth)
    if n == 0:
        return Node(random.choice(leaf), None, None)
    else:
        value = random.choice(unary_node+binary_node)
        if value in unary_node: 
            return Node(value, \
                None, \
                random_tree(max(0, min_depth-1), max_depth-1, unary_node, binary_node, leaf))
        else:
            return Node(value, \
                random_tree(max(0, min_depth-1), max_depth-1, unary_node, binary_node, leaf), \
                random_tree(max(0, min_depth-1), max_depth-1, unary_node, binary_node, leaf))

def q0frq():
    #choose random topic
    topic = random.choice(mod_corpus)
    #choose two distinct sentences
    sent1 = random.choice(topic)
    sent2 = sent1
    while sent2 == sent1: sent2 = random.choice(topic)
    conn = "-"
    while conn == "-" or conn == "->" or conn == "<->": conn = random.choice(list(english_trlns.keys()))
    ambig_sent = (random.choice(english_trlns["-"]) % \
        (random.choice(english_trlns[conn]) % (sent1, sent2)))
    ambig_sent = ambig_sent.capitalize() + "."
    begin_essay_question()
    text(f"""We say that an English sentence is <u>ambiguous</u> if its logical structure
    can be read in at least two non-equivalent ways. Using this definition, explain why the sentence 
    <i>"{ambig_sent}"</i> is ambiguous.""")
    end_question()

def q1frq(n_sentence=5):
    topic = random.choice(mod_corpus)
    random.shuffle(topic)
    letters_to_sent = {chr(ord("p")+i):topic[i] for i in range(len(topic))}
    
    def aux(tree):
        if tree.left == None:
            if tree.right == None:
                if tree.value[0] == "-": return random.choice(english_trlns["-"]) % letters_to_sent[tree.value[1:]]
                else: return letters_to_sent[tree.value]
            else:
                return tree.value % aux(tree.right)
        else:
            return tree.value % (aux(tree.left), aux(tree.right))

    def aux2(tree):
        if tree.left == None:
            if tree.right == None:
                return tree.value
            else:
                return english_to_nltk[tree.value] % aux2(tree.right)
        else:
            return english_to_nltk[tree.value] % (aux2(tree.left), aux2(tree.right))
    
    def aux3(tree):
        if tree.left == None:
            if tree.right == None:
                return tree
            return Node(random.choice(english_trlns[tree.value]),tree.left,aux3(tree.right))
        return Node(random.choice(english_trlns[tree.value]),aux3(tree.left),aux3(tree.right))

    html_sent = "<ul>"
    answer_lst = []
    sent_count = 0
    while sent_count < n_sentence:
        skel = random_tree(\
            min_depth = 1, \
            max_depth=1, \
            unary_node=[], \
            binary_node=None, \
            leaf=list(letters_to_sent.keys())+list(map(lambda x: "-"+x, letters_to_sent.keys())))
        if Prover9Command(goal = read_expr(skel.nltk())).prove() or Prover9Command(goal = read_expr(f'-{skel.nltk()}')).prove(): continue
        if skel.left.nltk() == skel.right.nltk(): skel = skel.left
        print(skel.nltk())
        skel = aux3(skel)
        html_sent += "<li>" + aux(skel).capitalize() + ".</li>"
        answer_lst.append(aux2(skel))
        sent_count += 1
    html_sent += "</ul>"

    replace_dct = {}
    for form in answer_lst:
        for char in form:
            if char in alphabet and char not in replace_dct:
                replace_dct[char] = chr(ord('p') + len(replace_dct))
    answer_lst_new = []
    for form in answer_lst:
        new_form = ''
        for char in form:
            if char in replace_dct:
                new_form += replace_dct[char]
            else:
                new_form += char
        answer_lst_new.append(new_form)
    print(answer_lst_new)

    answer = '<ul>'
    for form in answer_lst_new:
        answer += f'<li>${nltk_to_latex_prop(form)}$</li>'
    answer += '</ul>'
    html_sent += "</ul>"

    begin_essay_question()
    text(html_sent)
    comment_general("One possible translation is as follows. <p><p>"+answer)
    end_question()

def q2frq(n_premise=3, n_valid=10, n_invalid=10):
    
    def aux(tree, letters_to_sent):
        if tree.left == None:
            if tree.right == None:
                if tree.value[0] == "-": return random.choice(english_trlns["-"]) % letters_to_sent[tree.value[1:]]
                else: return letters_to_sent[tree.value]
            else:
                return tree.value % aux(tree.right, letters_to_sent)
        else:
            return tree.value % (aux(tree.left, letters_to_sent), aux(tree.right, letters_to_sent))

    def aux2(tree):
        if tree.left == None:
            if tree.right == None:
                return tree.value
            else:
                return english_to_nltk[tree.value] % aux2(tree.right)
        else:
            return english_to_nltk[tree.value] % (aux2(tree.left), aux2(tree.right))
    
    def aux3(tree):
        if tree.left == None:
            if tree.right == None:
                return tree
            return Node(random.choice(english_trlns[tree.value]),tree.left,aux3(tree.right))
        return Node(random.choice(english_trlns[tree.value]),aux3(tree.left),aux3(tree.right))

    questions = []

    valid_counter = 0
    invalid_counter = 0

    while valid_counter<n_valid or invalid_counter<n_invalid:
        topic = random.choice(mod_corpus)
        random.shuffle(topic)
        letters_to_sent = {chr(ord("p")+i):topic[i] for i in range(len(topic))}

        eng_prem = ""
        log_prem = []
        while len(log_prem)<n_premise:
            skel = random_tree(\
                min_depth = 1, \
                max_depth=1, \
                unary_node=[], \
                binary_node=None, \
                leaf=list(letters_to_sent.keys())+list(map(lambda x: "-"+x, letters_to_sent.keys())))
            if Prover9Command(goal = read_expr(skel.nltk())).prove() or Prover9Command(goal = read_expr(f'-{skel.nltk()}')).prove(): continue
            if skel.left.nltk() == skel.right.nltk(): skel = skel.left
            skel = aux3(skel)
            if aux2(skel) in log_prem: continue
            eng_prem += "" + aux(skel, letters_to_sent).capitalize() + ". "
            log_prem.append(aux2(skel))

        composite_prem = ""
        for premise in log_prem: composite_prem += premise + " & "
        composite_prem = composite_prem[:-3]

        if Prover9Command(goal=read_expr(composite_prem)).prove() or \
            Prover9Command(goal=read_expr(f"-({composite_prem})")).prove():
            continue
        
        skel = random_tree(\
                    min_depth = 1, \
                    max_depth=1, \
                    unary_node=[], \
                    binary_node=None, \
                    leaf=list(letters_to_sent.keys())+list(map(lambda x: "-"+x, letters_to_sent.keys())))
        if skel in log_prem: continue
        if Prover9Command(goal = read_expr(skel.nltk())).prove() or Prover9Command(goal = read_expr(f'-{skel.nltk()}')).prove(): continue
        if skel.left.nltk() == skel.right.nltk(): skel = skel.left
        log_conc = skel.nltk()
        skel = aux3(skel)
        eng_conc = "Therefore, " + aux(skel, letters_to_sent).lower() + "."
        validity = Prover9Command(goal=read_expr(log_conc), assumptions=[read_expr(premise) for premise in log_prem]).prove()
        if (validity and valid_counter == n_valid) or ((not validity) and invalid_counter==n_invalid): continue
        if validity:
            non_sequitur = False
            for i in range(len(log_prem)): non_sequitur = non_sequitur or Prover9Command(goal=read_expr(log_conc),assumptions=list(map(read_expr, log_prem[:i]+log_prem[i+1:]))).prove()
            if non_sequitur: continue
            valid_counter += 1

            #arrange letters alphabetically
            log_forms = log_prem + [log_conc]
            replace_dct = {}
            for form in log_forms:
                for char in form:
                    if char in alphabet and char not in replace_dct:
                        replace_dct[char] = chr(ord('p') + len(replace_dct))
            log_forms_new = []
            for form in log_forms:
                new_form = ''
                for char in form:
                    if char in replace_dct:
                        new_form += replace_dct[char]
                    else:
                        new_form += char
                log_forms_new.append(new_form)
            log_prem = log_forms_new[:-1]
            log_conc = log_forms_new[-1]

            questions.append((eng_prem, log_prem, eng_conc, log_conc, validity))
        else:
            invalid_counter += 1

            #arrange letters alphabetically
            log_forms = log_prem + [log_conc]
            replace_dct = {}
            for form in log_forms:
                for char in form:
                    if char in alphabet and char not in replace_dct:
                        replace_dct[char] = chr(ord('p') + len(replace_dct))
            log_forms_new = []
            for form in log_forms:
                new_form = ''
                for char in form:
                    if char in replace_dct:
                        new_form += replace_dct[char]
                    else:
                        new_form += char
                log_forms_new.append(new_form)
            log_prem = log_forms_new[:-1]
            log_conc = log_forms_new[-1]

            questions.append((eng_prem, log_prem, eng_conc, log_conc, validity))
        print(log_prem, log_conc, validity)
        print(valid_counter, invalid_counter)
    
    random.shuffle(questions)

    for (eng_prem, log_prem, eng_conc, log_conc, validity) in questions:
        begin_essay_question()

        text(eng_prem+eng_conc)

        latex_prem = "$\{"
        for premise in log_prem:
            latex_prem += nltk_to_latex_prop(premise)+","
        latex_prem = latex_prem[:-1] + "\}$"

        latex_conc = f"${nltk_to_latex_prop(log_conc)}$"

        if validity: eng_answer = "VALID"
        else: eng_answer = "NOT VALID"

        comment_general(f"""
        One way to represent the set of premises used in this argument was {latex_prem}. 
        One way to represent the conclusion was {latex_conc}.
        This argument was {eng_answer}.
        """)
        end_question()

def tree_to_nltk(tree):
    if tree.value in unary_conn:
        return f"{tree.value}{tree_to_nltk(tree.right)}"
    elif tree.value in binary_conn:
        return f"({tree_to_nltk(tree.left)}{tree.value}{tree_to_nltk(tree.right)})"
    else:
        return tree.value

def tree_to_conseq(tree):
    def aux(tree):
        if tree.value in unary_conn:
            sub = tree_to_conseq(tree.right)
            return sub + [f"{tree.value}{sub[-1]}"]
        elif tree.value in binary_conn:
            sub1 = tree_to_conseq(tree.left)
            sub2 = tree_to_conseq(tree.right)
            return sub1 + sub2 + [f"({sub1[-1]}{tree.value}{sub2[-1]})"]
        else:
            return [tree.value]
    raw = aux(tree)
    return [el for i, el in enumerate(raw) if el not in raw[:i]]

def q3frq(min_depth=2, max_depth=3, prop_vars = None):

    if prop_vars == None: prop_vars = ["p", "q", "r"]

    bound_form = 20
    bound_seq = 7

    nltk_form = "a"*(bound_form+1)
    conseq = [""]*(bound_seq+1)

    while len(nltk_form)>bound_form or len(conseq)>bound_seq:
        tree_form = random_tree(min_depth=min_depth, max_depth=max_depth, leaf=prop_vars)
        nltk_form = tree_to_nltk(tree_form)
        conseq = tree_to_conseq(tree_form)

    begin_essay_question()
    text(rf"Find a construction sequence for the formula ${nltk_to_latex_prop(nltk_form)}$.")

    latex_conseq = ""
    for subformula in conseq: latex_conseq+=nltk_to_latex_prop(subformula)+", "
    latex_conseq = latex_conseq[:-2]
    
    comment_general(rf"One possible construction sequence is $\langle {latex_conseq} \rangle$.")
    end_question()

def q4frq(n_questions = 2, min_depth=1, max_depth=2, n_letters=3):
    assert n_letters <= max_depth+1 #more letters requires longer formula to accomodate
    assert n_letters <= 3 #too many letters means huge truth table and bound is too small
    prop_letters = [chr(ord("p")+i) for i in range(n_letters)]

    def vals(prop_vars):
        if len(prop_vars) == 1:
            return [prop_vars[0],"-"+prop_vars[0]]
        first = prop_vars[0]
        sub = vals(prop_vars[1:])
        return list(map(lambda x: first+"&"+x, sub)) + list(map(lambda x: "-"+first+"&"+x, sub))
    valuations = vals(prop_letters)

    def sat(form):
        return not Prover9Command(goal=read_expr("- ("+ form + ")"), assumptions=[]).prove()

    bound = 15

    nltk_forms = []

    while len(nltk_forms)<n_questions:
        #we want our formulas to have all prop vars
        proper = False
        while not proper:
            form = random_prop_frml(\
                min_depth=min_depth,\
                max_depth=max_depth,\
                prop_vars=prop_letters)
            if len(form)>bound: continue
            if form in nltk_forms: continue
            proper = True
            for letter in prop_letters:
                proper = proper and (letter in form)
                if not proper: break 
        nltk_forms.append(form)
    
    for nltk_form in nltk_forms:
        answers = list(map(lambda val: sat(f"{nltk_form}&{val}"), valuations))

        table = [list(map(lambda form: rf"${nltk_to_latex_prop(form)}$", \
            prop_letters+[nltk_form]))]

        for (val, ans) in zip(valuations, answers):
            row = list(map(lambda x: not x[0]=="-", val.split("&")))
            row.append(ans)
            table.append(row)

        begin_essay_question()
        text(rf"Construct a truth table for the formula ${nltk_to_latex_prop(nltk_form)}$.")
        comment_general("""One possible solution is as follows. <p><p>
        <style>
        table, th, td {
        border:1px solid black;
        }
        </style>""" + \
        tabulate(table, \
            headers='firstrow', \
            stralign = 'center', \
            numalign = 'center', \
            tablefmt="html"))
        end_question()