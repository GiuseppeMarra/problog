from problog.program import PrologString
from problog.logic import Term
from problog.engine import DefaultEngine
from problog.sdd_formula import SDD

from sys import argv

pc = 0.2 # c = a v b
# P(A) = P(A | c)P(c) + P(A | not c)(1-P(c))
# 2/3 * 2/10 + 1/2 * 8/10 = 32/60

p = PrologString(f"""

0.5:: a.
0.5:: b.    

d:- a, \+b.

%p = ew / (ew +1)

{1-pc}::c_aux.
c :- c_aux.

c:- a.
c:- b.
constraint(c).
%query(d).
%query(c).
query(a).

""")


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

print("mln", 32/60)
print((2 * 0.2 * 0.25 + 2*0.8*0.25)/(4 * 0.8 * 0.25 + 3*0.2*0.25))
print((2 * 0.2 * 0.25 + 2*0.8*0.25)/(4 * 0.8 * 0.25 + 4*0.2*0.25))
