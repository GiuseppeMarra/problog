from problog.formula import LogicFormula
from problog.sdd_formula import SDD
from fol_grounding.cproblog import CProblogString


model = """
person(joe).
person(mary).
likeSoccer(joe).
likeFashion(mary).
0.5::male(X); 0.5::female(X):-person(X).
0.9::male(X):-likeSoccer(X).  
0.9::female(X):-likeFashion(X).


constraint(not (male(X) <-> female(X))).

query(male(joe)).
query(female(joe)).
"""

# constraint((not male(X) or female(X)) and (not female(X) or male(X))).


#

ontology = {"constants": ["joe", "mary"],
            "predicates": {"male":1, "female":1, "person":1, "likeSoccer":1, "likeFashion":1}}




program = CProblogString(model, ontology)
formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
print(circuit.evaluate())






