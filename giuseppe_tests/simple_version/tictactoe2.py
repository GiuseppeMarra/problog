from problog.formula import LogicFormula
from problog.program import PrologString
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF

from simple_version.cproblog import CProblogString


model = """
:- use_module(library(apply)).


symbol(cross).
symbol(circle).

""" +\
". ".join("cell(c%d)" % i for i in range(9)) + ".\n" +\
"""


%You can't use an already used cell
only_one_symbol_in_cell(C):- \+ cell(C).
only_one_symbol_in_cell(C):- cell(C), symbol(S), \+ play(S,C).
only_one_symbol_in_cell(C):- play(S,C), symbol(S1), S1\=S, \+ play(S1,C).
constraint(only_one_symbol_in_cell(C)).

%Anytime, only one move can be done
%two_plays(T) :- play(S,C,T), cell(C1), C1\=C, play(S,C1,T).
%two_plays(T) :- play(S,C,T), symbol(S1), S1\=S, play(S1,C,T). %unnecessary given the previous constraint
%two_plays(T) :- play(S,C,T), cell(C1), symbol(S1),C1\=C, S1\=S, play(S1,C1,T). %unnecessary given the previous constraint
%only_one_play_in_time(T) :- time(T), \+ two_plays(T).
%constraint(only_one_play_in_time(T)).

%Players need to alternate themselves at each timestep
alternate_play(S) :- symbol(S), cell(C), play(S,C), \+ last(S).
constraint(alternate_play(S)).

0.05::play(S,C):-  symbol(S), cell(C).




evidence(play(circle, c3)).

query(play(S, C)).


"""

print(model)


program = PrologString(model)

formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
# circuit = DDNNF.create_from(formula)
print(circuit.evaluate())
print("END")






