from problog.program import PrologString
from problog.logic import Term
from problog.engine import DefaultEngine
from problog.sdd_formula import SDD



#p = PrologFile('path/to/myprogram.pl')
p = PrologString("""

0.5:: a.
0.5:: b.    

d:- a, \+b.

p = ew / (ew +1)

0.2::c.

c:- a.
c:- b.
constraint(c).
query(d).
query(c).
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