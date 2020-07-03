from problog.program import PrologString
from problog.formula import LogicFormula, LogicDAG
from problog.sdd_formula import SDD
from problog.cnf_formula import CNF
from problog.engine import DefaultEngine
from problog.logic import Term

# model = """person(john).
# person(mary).
#
# 0.7::burglary.
# 0.2::earthquake.
#
# 0.9::alarm <- burglary, earthquake.
# 0.8::alarm <- burglary, \+earthquake.
# 0.1::alarm <- \+burglary, earthquake.
#
# 0.8::calls(X) <- alarm, person(X).
# 0.1::calls(X) <- \+alarm, person(X).
#
#
# %%% Evidence
# evidence(calls(john),true).
# evidence(calls(mary),true).
#
# %%% Queries
# query(burglary).
# query(earthquake)."""


model = PrologString("""
coin(c1). coin(c2).
fakeCoin(c1).
0.4::heads(C); 0.6::tails(C) :- coin(C).
0.8::heads(C):-fakeCoin(C).
win :- heads(C).

evid1(X):-heads(X),\+ tails(X).
evid2(X):-\+ heads(X), tails(X).
evid3(X):-evid1(X).
evid3(X):-evid2(X).

evidence(evid3(X)).

query(heads(c1)).
query(tails(c1)).
""")



formula = LogicFormula.create_from(model)


# print(SDD.create_from(formula).evaluate())
