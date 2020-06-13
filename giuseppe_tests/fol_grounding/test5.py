from problog.program import SimpleProgram
from problog.logic import Not, And, Or, Constant,Var,Term,AnnotatedDisjunction
from fol_grounding.cproblog import ConstrainedLogicProgram, SimpleConstrainedLogicProgram, Constraint
from problog.program import PrologString, LogicProgram, SimpleProgram
from problog.formula import LogicFormula
from problog.core import transform
from problog.constraint import ClauseConstraint
from fol_grounding.fol_parser import Formula, EVID
import re

person,likeSoccer,likeFashion,male,female,query = Term('person'),Term('likeSoccer'),Term('likeFashion'),Term('male'),Term('female'),Term('query')
X = Var('X')
X2 = Var('X2')
mary = Constant('mary')
john = Constant('john')
p = SimpleConstrainedLogicProgram()
p += person(mary)
p += person(john)
p += likeSoccer(john)
p += likeFashion(mary)
p += AnnotatedDisjunction([male(X,p=0.5), female(X,p=0.5)], person(X))
p += male(X, p=0.9) << likeSoccer(X)
p += female(X, p=0.9) << likeFashion(X)
p += query(male(john))

non_constrained_logic_formula = LogicFormula.create_from(p)
for i in p:
    print(i)

p += Constraint(And(Or(Not("\+", male(X2)),female(X2)),Or(Not("\+", female(X2)),male(X2))))




def analyse_constraint(c, vars):
    if isinstance(c, Not):
        analyse_constraint(c.child, vars)
    elif isinstance(c, And) or isinstance(c, Or) :
        analyse_constraint(c.op1, vars)
        analyse_constraint(c.op2, vars)
    elif isinstance(c, Term):
        for v in c.args:
            if isinstance(v, Var) and v not in vars:
                vars.append(v)
    else:
        raise Exception("GroundingError: malformed constraint")

# constants = [non_constrained_logic_formula.]

# for c in p.constraints():
#     vars = []
#     analyse_constraint(c.op, vars)
#     for

# @transform(ConstrainedLogicProgram, LogicFormula)
# def createConstraintLogicProgram(model, destination, **kwargs):
















