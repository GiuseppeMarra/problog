from problog.program import PrologString
from problog.formula import LogicFormula
from problog.sdd_formula import SDD
from problog.engine import DefaultEngine
from problog.logic import Term, Var
from problog.tasks.constraint import ConstraintFactory

model = PrologString("""
% Your model here

person(john).
person(mary).
likeSoccer(john).
likeFashion(mary).
0.5::male(X); 0.5::female(X):-person(X).
0.9::male(X):-likeSoccer(X).  
0.9::female(X):-likeFashion(X).

ensure_true(male(john)) :- True.

query(male(john)).
query(female(john)).
""",factory=ConstraintFactory())

formula = LogicFormula.create_from(model)
print(formula)
circuit = SDD.create_from(formula)
print(circuit.evaluate())
