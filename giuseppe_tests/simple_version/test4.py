from problog.formula import LogicFormula
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF
from simple_version.cproblog import CProblogString
from problog.program import PrologString

# constraint(not( male(X) <-> female(X))).


model = """
person(john).
likesSoccer(john).
0.5::male(X); 0.5::female(X):-person(X).
t(_)::male(X):-likesSoccer(X).  

mutually_exclusive(X) :- male(X), \+ female(X).
mutually_exclusive(X) :- female(X), \+ male(X).
constraint(mutually_exclusive(X)).

query(male(john)).
query(female(john)).
"""




program = PrologString(model)
formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
print(circuit.evaluate())






