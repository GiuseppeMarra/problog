from problog.formula import LogicFormula
from problog.sdd_formula import SDD
from simple_version.cproblog import CProblogString


model = """
person(john).
person(mary).
likeSoccer(john).
likeFashion(mary).
0.5::male(X); 0.5::female(X):-person(X).
0.9::male(X):-likeSoccer(X).  
0.9::female(X):-likeFashion(X).

constraint(not( male(X) <-> female(X))).


query(male(john)).
query(female(john)).
"""


#



program = CProblogString(model, )
formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
print(circuit.evaluate())






