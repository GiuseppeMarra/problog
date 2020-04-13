from problog.program import PrologString
from problog.formula import LogicFormula
from problog.core import transform
from problog.constraint import TrueConstraint
from simple_version.fol_parser import Formula, EVID
import re


class CProblogString():

    def __init__(self, s):
        self.s = s



def preprocess(l):
    return [k for k in l if len(k)>0]

@transform(CProblogString, LogicFormula)
def cProbLog2LogicFormula(model,destination=None, **kwdargs):
    # todo,now it is just a stupid parser to test the idea

    model = model.s
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
    D = []
    for c in constraints:
            d = c.split("constraint(")[1][:-1] #skip last parenthesis
            D.append("(%s)" % d)
    D = " and ".join(D)
    L = [s.replace("not", "\\+") for s in Formula(definition=D).to_evidence()]

    problog_program.extend(L[:-1])
    evidences.append(L[-1])
    new_model = ".\n".join(preprocess(problog_program) + preprocess(evidences) + preprocess(queries)) + "."
    print(new_model)
    problog_formula = LogicFormula.create_from(PrologString(new_model))
    keys = []
    for k, v  in problog_formula._names[problog_formula.LABEL_EVIDENCE_POS].items():
        if EVID in k.functor:
            keys.append((k,v))
    for k,v in keys:
        problog_formula._names[problog_formula.LABEL_EVIDENCE_POS].pop(k)
        problog_formula.add_constraint(TrueConstraint(v))
        # problog_formula.add_name(name=k,key=v, label=problog_formula.LABEL_EVIDENCE_POS)


    return problog_formula