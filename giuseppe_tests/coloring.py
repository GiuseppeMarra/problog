from problog.formula import LogicFormula
from problog.program import PrologString
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF

from simple_version.cproblog import CProblogString


model = """
color(red).
color(green).

edge(a,b).
edge(a,e).
edge(c,d).

color(a,green)

path(X,Y):-edge(Z,Y), path(X,Z).



% cite(X,Y) -> class(X,Z) <-> class(Y,Z).
same_color(X,Y):- edge(X,Y), color(Z), color(X,Z), color(Y,Z).
same_color(X,Y):- \+ edge(X,Y).
constraint(same_color(X,Y)).

mutually_exclusive(X) :- color(X,red), \+ color(X,green).
mutually_exclusive(X) :- color(X,green), \+ color(X,red).
constraint(mutually_exclusive(X)).



query(color(X, a)).
query(color(X, b)).
"""



program = PrologString(model)

formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
# circuit = DDNNF.create_from(formula)
print(circuit.evaluate())
print("END")






