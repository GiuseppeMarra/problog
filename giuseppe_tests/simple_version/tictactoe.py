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
". ".join("time(%d)" % i for i in range(9)) + ".\n" +\
"""

0.05::play(S,C,T):-  symbol(S), cell(C), time(T).


%You can't use an already used cell
only_one_symbol_in_cell(C):- \+ cell(C).
only_one_symbol_in_cell(C):- play(S,C,T), symbol(S1), S1\=S, \+ play(S1,C,T1).
constraint(only_one_symbol_in_cell(C)).

%Anytime, only one move can be done
two_plays(T) :- play(S,C,T), cell(C1), C1\=C, play(S,C1,T).
%two_plays(T) :- play(S,C,T), symbol(S1), S1\=S, play(S1,C,T). %unnecessary given the previous constraint
%two_plays(T) :- play(S,C,T), cell(C1), symbol(S1),C1\=C, S1\=S, play(S1,C1,T). %unnecessary given the previous constraint
only_one_play_in_time(T) :- time(T), \+ two_plays(T).
constraint(only_one_play_in_time(T)).

%Players need to alternate themselves at each timestep
alternate_play(T) :- \+ time(T).
alternate_play(T) :- T == 0.
alternate_play(T) :- play(S,C,T), T1 is T - 1, \+ play(S,C1, T1). 
constraint(alternate_play(T)).


evidence(play(circle, c3, 0)).


query(play(cross, C, 1)).


"""

print(model)


program = PrologString(model)

formula = LogicFormula.create_from(program)
print(formula)
circuit = SDD.create_from(formula)
# circuit = DDNNF.create_from(formula)
print(circuit.evaluate())
print("END")






