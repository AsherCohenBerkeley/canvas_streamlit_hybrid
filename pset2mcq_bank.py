from tabulate import tabulate # you need tabulate to render the truth tables

import random

from nltk import Prover9, Prover9Command

from nltk.sem import logic
logic._counter._value = 0

from nltk.sem import Expression
read_expr = Expression.fromstring

Prover9.config_prover9(Prover9, r'/Users/ashercohen/bin')

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
    """
123 They tell him to write the letter
124 They force him into writing the letter
125 They leave the room
126 He reveals the bad news""",\
    """
    | The boss is happy
    | The employees are happy
    | The shareholders are happy
    | The public is happy""",\
    """The crowds cheer in the streets
152 The streets fill with people
153 The government is excited
155 The crisis comes to an end  """,\
    """You hear animals roaring in the meadows
156 The fields are full of animals 
157 You hear birds chirping in the woods 
159 You enjoy life in the jungle""", \
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

def q1mcq(true=1, false=1, min_depth=0, max_depth=1, connectives = None, prop_vars = None):
    questions = []

    true_counter = 0
    false_counter = 0
    
    while true_counter < true or false_counter < false:
        conc = random_prop_frml(min_depth=min_depth, max_depth=max_depth, connectives=connectives, prop_vars=prop_vars)
        prem = conc
        while prem == conc: prem = random_prop_frml(min_depth=min_depth, max_depth=max_depth, connectives=connectives, prop_vars=prop_vars)
        
        bound = 18
        if len(prem) > bound or len(conc)>bound: continue

        try: validity = Prover9Command(read_expr(conc), assumptions = [read_expr(prem)]).prove()
        except: continue

        if (validity and true_counter < true and (not (prem, conc, validity) in questions)):
            true_counter += 1
            questions.append((prem, conc, validity))
            print((prem, conc, validity, true_counter))
        elif ((not validity) and false_counter < false and (not ((prem, conc, validity) in questions))):
            false_counter += 1
            questions.append((prem, conc, validity)) 
            print((prem, conc, validity, false_counter))
    
    random.shuffle(questions)
    
    output = []
    for (prem, conc, validity) in questions:
        output.append((rf"Is ${nltk_to_latex_prop(conc)}$ a logical consequence of ${nltk_to_latex_prop(prem)}$?",validity))

    return output

print(q1mcq())