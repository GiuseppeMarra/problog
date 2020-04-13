from __future__ import print_function

from problog.program import PrologString, SimpleProgram
from problog.formula import LogicFormula
from problog.core import transform
from problog.engine import DefaultEngine
from problog.constraint import ClauseConstraint, TrueConstraint
from fol_grounding.fol_parser import Formula, EVID
import re

from problog.errors import GroundingError
from problog.logic import Term, Var, Constant, AnnotatedDisjunction, Clause, And, Or, Not, AggTerm, list2term, term2str
from problog.core import transform, ProbLogObject
from problog.clausedb import  ClauseDB
from problog.parser import DefaultPrologParser, Factory
from problog.core import ProbLogError
from collections import namedtuple, defaultdict
from problog.engine import GenericEngine
from problog.formula import LogicFormula
from problog.program import LogicProgram

import os
import sys







class CProblogString():

    def __init__(self, string, ontology):
        self.string = string
        self.ontology = ontology



def preprocess(l):
    return [k for k in l if len(k)>0]

@transform(CProblogString, LogicFormula)
def cProbLog2LogicFormula(model,destination=None, **kwdargs):
    # todo,now it is just a stupid parser to test the idea


    ontology = model.ontology
    model = model.string
    lines = re.split("\.\s+", model.replace("\n"," "))
    problog_program = []
    evidences = []
    queries = []
    constraints = []

    for line in lines:

        if "query" in line:
            queries.append(line)
        elif "evidence" in line:
            evidences.append(line)
        elif "constraint" in line:
            constraints.append(line)
        else:
            problog_program.append(line)
    F = []
    for c in constraints:
            d = c.split("constraint(")[1][:-1] #skip last parenthesis
            F.append(Formula(definition=d))
            print(F[-1].toString())



    engine = DefaultEngine()


    """Handling the program"""
    new_model = (".\n".join(preprocess(problog_program) + preprocess(evidences) + preprocess(queries)) + ".")
    p = PrologString(new_model)
    db = engine.prepare(p)
    problog_formula = engine.ground_all(db)



    """Handling the constraints"""

    """Ground all the ontology"""
    var_names = ["X"+str(i) for i in range(1000)]
    queries = []
    for predicate, arity in ontology["predicates"].items():
        vars = [Var(n) for n in var_names[:arity]]
        queries.append(Term(predicate, *vars))
    problog_formula = engine.ground_all(db, target=problog_formula, queries=queries)
    dictionary_name_node = {str(node.name): node for node in problog_formula._nodes if "choice" not in str(node.name)}

    """Ground the constraints"""
    from itertools import product
    for formula in F:
        arity = len(formula.variables)
        for constant_instant in product(*[ontology["constants"] for _ in range(arity)]):
            root_op = formula.ground_formula(problog_formula, constant_instant, atom_dict=dictionary_name_node)
            problog_formula.add_constraint(TrueConstraint(root_op))

    return problog_formula


class Constraint(Term):
    """A Constraint"""
    def __init__(self, op, **kwdargs):
        Term.__init__(self, '[', op, **kwdargs)
        self.op = op

    def __repr__(self):
        r = term2str(self.op)
        if isinstance(self.op, Or) or isinstance(self.op, And):
            r = '(%s)' % r
        self.repr = "%s" % r
        self.reprhash = hash(self.repr)
        return self.repr

    @property
    def predicates(self):
        return [self.op.signature]


class ConstrainedLogicProgram(LogicProgram):
    """ConstrainedLogicProgram"""

    def add_constraint(self, constraint, scope=None):
        raise NotImplementedError("ConstrainedLogicProgram.add_constraint is an abstract method.")
    def constraints(self):
        raise NotImplementedError("ConstrainedLogicProgram.constraints is an abstract method.")




class SimpleConstrainedLogicProgram(SimpleProgram):
    """SimpleConstrainedLogicProgram"""

    def __init__(self):
        super(SimpleConstrainedLogicProgram, self).__init__()
        self.__clauses = []
        self.__constraints = []

    def constraints(self):
        return self.__constraints

    def add_constraint(self, constraint, scope=None):
        if type(constraint) is list:
            for c in constraint:
                self.__constraints.append(c)
        else:
            self.__constraints.append(constraint)

    def __iter__(self):
        return iter(self.__clauses + self.__constraints)

    def __iadd__(self, clausefactconstraint):
        """Add clause or fact or constraint using the ``+=`` operator."""
        self.add_statement(clausefactconstraint)
        return self

    def add_statement(self, clausefactconstraint, scope=None):
        if isinstance(clausefactconstraint, Constraint):
            self.add_constraint(clausefactconstraint,scope=scope)
        else:
            super(SimpleConstrainedLogicProgram, self).add_statement(clausefactconstraint,scope)