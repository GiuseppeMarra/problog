from problog.formula import LogicFormula
from problog.program import PrologString
from problog.sdd_formula import SDD



model = """

row(1). row(2). row(3). row(4). row(5). row(6). row(7). row(8). row(9).
column(1). column(2). column(3). column(4). column(5). column(6). column(7). column(8). column(9).
num(1). num(2). num(3). num(4). num(5). num(6). num(7). num(8). num(9).


cell(2,2,8). cell(3,1,6). cell(3,3,2).
cell(2,6.7). 
cell(1,7,2). cell(2,8,9). cell(3,7,5).
cell(4,2,7).
cell(4,5,6). cell(5,4,9). cell(5,6,1). cell(6,5,2).
cell(6,8,4).
cell(7,3,5). cell(8,2,9). cell(9,3,6).
cell(8,4,4).
cell(7,7,6). cell(7,9,3). cell(8,8,7).


% no number repeats in the same row
multi_in_row(R,N):- cell(R,C1,N), cell(R,C2,N), C1\=C2.

% no number repeats in the same column
multi_in_col(C,N):- cell(R1,C,N), cell(R2,C,N), R1\=R2.

% no number repeats in the same 3*3 box
multi_in_cell(R,C,N):- cell(R,C,N), cell(R1,C1,N), R\=R1, C\=C1,
((R/3)*3 + C/3) == ((R1/3)*3 + C1/3).


evidence(multi_in_row(R,N), false).
evidence(multi_in_col(C,N), false).
evidence(multi_in_cell(R,C,N), false).


query(cell(R,C,N)).
"""
from itertools import product
prob_cell = ""
for i,j,k in product(range(1,10), repeat=3):
    prob_cell+="0.11::cell(%d,%d,%d). \n" % (i,j,k)

model+=prob_cell



program = PrologString(model)
formula = LogicFormula.create_from(program)

print(formula)
circuit = SDD.create_from(formula)
# circuit = DDNNF.create_from(formula)
print(circuit.evaluate())






