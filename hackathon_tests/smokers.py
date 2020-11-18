from problog.program import PrologString
from problog.logic import Term
from problog.engine import DefaultEngine
from problog.sdd_formula import SDD

from sys import argv
from math import e


p = PrologString(f"""

person(ann).
person(bob).
person(carl).


friend(ann,bob).
friend(carl, bob).


%friend(X,Y) :- friend(Y,X).
0.3::smokes(X) :- person(X).


% smokes(X) ^ friend(X,Y)) -> smokes(Y)
temp1(X,Y) :- smokes(X), friend(X,Y).
temp2(Y) :- smokes(Y).
c(X,Y) :- temp2(Y); \+ temp1(X,Y).

%constraint(c(X,Y)) :- person(X), person(Y).
mln_constraint(c(X,Y),0.3) :- person(X), person(Y).
query(smokes(bob)).
""")



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
