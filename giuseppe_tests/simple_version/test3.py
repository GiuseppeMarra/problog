from problog.program import SimpleProgram
from problog.logic import Constant,Var,Term,AnnotatedDisjunction
from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable
from problog.cproblog import SimpleConstrainedLogicProgram, Constraint
from problog.formula import LogicFormula, LogicDAG
from problog.logic import Term
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF

coin,heads,tails,win,query = Term('coin'),Term('heads'),Term('tails'),Term('win'),Term('query')
C = Var('C')
# p = SimpleProgram()
p = SimpleConstrainedLogicProgram()
coin_c1 = coin(Constant('c1'))
coin_c2 = coin(Constant('c2'))
p += coin_c1
p += coin_c2
p += AnnotatedDisjunction([heads(C,p=0.4), tails(C,p=0.6)], coin(C))
p += Constraint(coin_c1 | coin_c2)
p += (win << heads(C))
p += query(win)


lf = LogicFormula.create_from(p)   # ground the program
dag = LogicDAG.create_from(lf)     # break cycles in the ground program
cnf = CNF.create_from(dag)         # convert to CNF
ddnnf = DDNNF.create_from(cnf)       # compile CNF to ddnnf