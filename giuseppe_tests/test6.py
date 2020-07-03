from problog.formula import LogicFormula
from problog.program import PrologString
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF

from simple_version.cproblog import CProblogString


model = """
isclass(a).
isclass(b).
cite(second,third).
class(first, a).
paper(first).
paper(second).
paper(third).
hasWord(second, aword).

0.5::class(X,a); 0.5::class(X,b):- paper(X).
0.3::class(X,a):- paper(X), hasWord(X, aword).


% cite(X,Y) -> class(X,Z) <-> class(Y,Z).
same_class(X,Y,Z) :- class(X,Z), class(Y,Z).
same_class(X,Y,Z) :- \+ class(X,Z), \+ class(Y,Z).
manifold(X,Y,Z):- cite(X,Y), isclass(Z), same_class(X,Y,Z).
manifold(X,Y,Z):- \+cite(X,Y).
constraint(manifold(X,Y,Z)).

mutually_exclusive(X) :- class(X,a), \+ class(X,b).
mutually_exclusive(X) :- class(X,b), \+ class(X,a).
constraint(mutually_exclusive(X)).


query(class(X, a)).
query(class(X, b)).
"""



program = PrologString(model)

formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
# circuit = DDNNF.create_from(formula)
print(circuit.evaluate())
print("END")






