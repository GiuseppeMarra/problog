from problog.program import PrologString
from problog.logic import Term
from problog.engine import DefaultEngine
from problog.sdd_formula import SDD

from sys import argv
from math import e

""" Vincent's receipt:
mln: 
4 a v b

problog:
constr :- a.
constr :- b.
mln_constraint(constr, 4).

aut translation:
e...::constr_aux.
new_constr :- constr_aux, constr.
new_constr :- \+constr_aux, \+constr.
constraint(new_constr).
"""

w=10

p = PrologString(f"""

0.5:: a.
0.5:: b.    

{e / (e + 1)}::c_aux.
c :- c_aux.

c:- a.
c:- b.

constraint(c).

query(a).

""")

p = PrologString(f"""

0.5:: a.
0.5:: b.    

{e ** w / (e ** w + 1)}::c_aux.

c_or:- a.
c_or:- b.

c_iff :- c_or, c_aux.
c_iff :- \+c_or, \+c_aux.

constraint(c_iff).

query(a).

""")


p = PrologString(f"""
0.5::a.
0.5::b.
c :- a ; b.
%mln_constraint(c,4).
mln_constraint(c,3) :- a.
query(a).
""")

p = PrologString(f"""
0.5::a(cost1).
0.5::b(cost1).
0.5::a(cost2).
0.5::b(cost2).
d(cost1).
d(cost2).
c(X) :- a(X) ; b(X).
mln_constraint(c(X),3) :- d(X).
query(a(cost1)).
query(a(cost2)).
""")


p = PrologString(f"""
0.5::a.
0.5::b.
%mln_constraint((\+a ; b), 0.1).  %a  b
query(a).
""")

# p = PrologString(f"""
# 0.5::a.
# 0.5::b.
# c :- a.
# c :- b.
# mln_constraint(c,1).
# query(a).
# """)

# Prepare ProbLog engine
engine = DefaultEngine(label_all=True)
db = engine.prepare(p)

# Ground program and make acyclic
gp = engine.ground_all(db)

# Create SDD circuit from program
sdd = SDD.createFrom(gp)  # Use SDDs

# Evaluate the circuit to obtain probabilities
result = sdd.evaluate()

print(result)

# print(2*(e**w) / (3*(e**w) +1))
