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
0.3::a(1).
0.2::b(1).

constr(X) :- a(X).
constr(X) :- b(X).

0.3::constr_aux(X).
constr_constr(X) :- constr(X), constr_aux(X).
constr_constr(X) :- \+constr(X), \+constr_aux(X).
constraint(constr_constr(X)).
query(a(1)).
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
sdd = SDD.createFrom(gp) # Use SDDs

# Evaluate the circuit to obtain probabilities
result = sdd.evaluate()

print(result)

print(2*(e**w) / (3*(e**w) +1))
