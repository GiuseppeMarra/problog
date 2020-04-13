from pyparsing import *
ParserElement.enablePackrat()
from collections import OrderedDict
from collections import namedtuple
from problog.logic import Term, Var, Constant

VARIABLE = "VARIABLE"
IMPLIES = "IMPLIES"
IFF = "IFF"
AND = "AND"
OR = "OR"
NOT = "NOT"
ATOM = "ATOM"
XOR = "XOR"
EVID = "eeevvviiiddd"

name2symb = {IMPLIES: "->",
          IFF: "<->",
          AND: "and",
          OR: "or",
          ATOM: "",
          NOT: "not"}

Node = namedtuple("Node", "op children name")


class Formula(object):

    def __init__(self, definition):
        self.variables = OrderedDict()
        self.atoms = []
        self.logic = None
        self.expression_tree = self.parse(definition)
        self.definition = definition
        self.variables = OrderedDict()
        self.atoms = {}



        self.root = self.parse(self.definition)
        self.cnf_root = self._toCNF(self.root)

    def _parse_action(self, class_name):
        def _create(tokens):
            if class_name in [VARIABLE]:
                name = tokens[0]
                if name not in self.variables:
                    self.variables[name] = Node(VARIABLE, None, name=name)
                return self.variables[name]
            elif class_name in [ATOM]:
                return Node(op=class_name, children=tokens[1:], name = tokens[0]+"("+",".join([t.name for t in tokens[1:]])+")")
            elif class_name in [NOT]:
                args = tokens[0][1:]
                return Node(op=class_name, children=args, name=name2symb[class_name])
            elif class_name in [AND, OR, XOR, IMPLIES, IFF]:
                args = tokens[0][::2]
                return Node(op=class_name, children=args, name=name2symb[class_name])
        return _create

    def parse(self, definition):

        left_parenthesis, right_parenthesis, colon, left_square, right_square = map(Suppress, "():[]")
        symbol = Word(alphas)

        ''' TERMS '''
        var = symbol
        var.setParseAction(self._parse_action(VARIABLE))

        ''' FORMULAS '''
        formula = Forward()
        not_ = Keyword("not")
        and_ = Keyword("and")
        or_ = Keyword("or")
        xor = Keyword("xor")
        implies = Keyword("->")
        iff = Keyword("<->")

        relation = Word(alphas)
        atomic_formula = relation + left_parenthesis + delimitedList(var) + right_parenthesis
        atomic_formula.setParseAction(self._parse_action(ATOM))
        espression = atomic_formula
        formula << infixNotation(espression,
                                 [
                                     (not_, 1, opAssoc.RIGHT,self._parse_action(NOT)),
                                     (and_, 2, opAssoc.LEFT, self._parse_action(AND)),
                                     (or_, 2, opAssoc.LEFT, self._parse_action(OR)),
                                     (xor, 2, opAssoc.LEFT, self._parse_action(XOR)),
                                     (implies, 2, opAssoc.LEFT, self._parse_action(IMPLIES)),
                                     (iff, 2, opAssoc.LEFT, self._parse_action(IFF))
                                 ])

        tree = formula.parseString(definition, parseAll=True)
        return tree[0]

    def _toCNF(self, node):
        pre = "ffff"
        post = self._to_string(node)
        while pre != post:
            pre = post
            def _inner(node):
                if node.op == ATOM:
                    return node
                if len(node.children) > 2:
                    raise Exception("n-ary operation not handled. Please binarize the string with parenteses.")

                ret = None
                for i in range(len(node.children)):
                    # node.children[i] = self._toCNF(node.children[i])
                    node.children[i] = _inner(node.children[i])

                if node.op == IFF:
                    # implies1 = Node(op=IMPLIES, children=node.children, name=name2symb[IMPLIES])
                    # implies2 = Node(op=IMPLIES, children=node.children[::-1], name=name2symb[IMPLIES])
                    # ret =  Node(op=AND, children=[implies1,implies2], name=name2symb[AND])
                    a = node.children[0]
                    b = node.children[1]
                    nota = Node(op=NOT, children=[node.children[0]], name=name2symb[NOT])
                    notb = Node(op=NOT, children=[node.children[1]], name=name2symb[NOT])
                    implies1 = Node(op=OR, children=[nota, b], name=name2symb[OR])
                    implies2 = Node(op=OR, children=[notb, a], name=name2symb[OR])
                    # implies2 = Node(op=OR, children=[a, notb], name=name2symb[OR])
                    ret =  Node(op=AND, children=[implies1,implies2], name=name2symb[AND])
                elif node.op == IMPLIES:
                    nota = Node(op=NOT, children=[node.children[0]], name=name2symb[NOT])
                    ret =  Node(op=OR, children=[nota, node.children[1]], name = name2symb[OR])
                elif node.op == NOT:
                    if node.children[0].op == NOT:
                        ret = node.children[0].children[0]
                    elif node.children[0].op == OR:
                        nota = Node(op=NOT, children=[node.children[0].children[0]], name=name2symb[NOT])
                        notb = Node(op=NOT, children=[node.children[0].children[1]], name=name2symb[NOT])
                        ret =  Node(op = AND, children=[nota, notb], name = name2symb[AND])
                    elif node.children[0].op == AND:
                        nota = Node(op=NOT, children=[node.children[0].children[0]], name=name2symb[NOT])
                        notb = Node(op=NOT, children=[node.children[0].children[1]], name=name2symb[NOT])
                        ret =  Node(op=OR, children=[nota, notb], name=name2symb[OR])
                elif node.op == OR:
                    for i in range(len(node.children)):
                        if node.children[i].op == AND:
                            j = abs(i - 1 )
                            left_or = Node(op=OR, children=[node.children[i].children[0], node.children[j]], name=name2symb[OR])
                            right_or = Node(op=OR, children=[node.children[i].children[1], node.children[j]], name=name2symb[OR])
                            ret =  Node(op=AND, children=[left_or, right_or], name=AND)
                            break
                if ret is not None:
                    # return self._toCNF(ret)
                    return _inner(ret)
                return node
            node = _inner(node)
            post = self._to_string(node)
        return node
    def to_CNF(self):
        return self._to_string(self.cnf_root)


    def _print(self, node, offset=0):
        if node.op == ATOM:
            print(" "*offset + node.name)
        elif node.op == NOT:
            print(" "*offset + node.name)
            self._print(node.children[0], offset+ 4)
        else:
            self._print(node.children[0], offset + 4)
            print(" "*offset + node.name)
            self._print(node.children[1], offset+4)

    def print(self):
        self._print(self.root, 0)

    def _to_string(self, node):
        if node.op == ATOM:
            return node.name
        elif node.op == NOT:
            return "(" + name2symb[NOT] +" "+ self._to_string(node.children[0]) + ")"
        else:
            a = self._to_string(node.children[0])
            b = self._to_string(node.children[1])
            return "("+ a + " " + node.name + " " + b + ")"

    def toString(self):
        return self._to_string(self.root)

    def _merge(self,lst1,lst2):
        L = [l for l in lst1]
        for l in lst2:
            if l not in lst1:
                L.append(l)

        return L

    def _add_evidences(self, evidence_strings, node):
        if node.op == ATOM:
            vars = node.name.split("(")[1].split(")")[0].split(".")
            return node.name, vars
        elif node.op == NOT:
            name = node.children[0].name
            vars = name.split("(")[1].split(")")[0].split(".")
            return "not "+ name, vars
        elif node.op == AND:
            first, first_vars = self._add_evidences(evidence_strings, node.children[0])
            second, second_vars = self._add_evidences(evidence_strings, node.children[1])
            vars = self._merge(first_vars, second_vars)
            self.evidence_count+=1
            evid = EVID+str(self.evidence_count)
            evid = "%s(%s)" % (evid,",".join(vars))
            evidence_strings.append("%s:-%s,%s" % (evid,first,second))
            # evidence_strings.append("evidence(%s, true)." % (evid))
            return evid,vars
        elif node.op == OR:
            first, first_vars = self._add_evidences(evidence_strings, node.children[0])
            second, second_vars = self._add_evidences(evidence_strings, node.children[1])
            vars = self._merge(first_vars, second_vars)
            self.evidence_count += 1
            evid = EVID+str(self.evidence_count)
            evid = ("%s(%s)" % (evid, ",".join(vars)))
            evidence_strings.append("%s:-%s" % (evid, first))
            evidence_strings.append("%s:-%s" % (evid, second))
            # evidence_strings.append("evidence(%s, true)." % (evid))
            return evid,vars

    def to_evidence(self):
        self.evidence_count = 0
        print(self._to_string(self.cnf_root))
        evidence_strings = []
        evid, _ = self._add_evidences(evidence_strings, self.cnf_root)
        evidence_strings.append("evidence(%s, true)" % (evid))
        return sorted(evidence_strings)

    def ground_formula(self, problog_formula, constants, atom_dict):

        map_constants = {}

        for i, (var_name, _) in enumerate(self.variables.items()):
            map_constants[var_name] = constants[i]

        return self._ground(self.root, problog_formula, map_constants, atom_dict)


    def _ground(self, node, problog_formula, map_constants, atom_dict):

        if node.op == ATOM:
            idx = node.name
            constants = []
            for k,v in map_constants.items():
                idx = idx.replace(k,v)
                constants.append(v)
            if idx not in atom_dict:
                atom = problog_formula.get_node(problog_formula.add_atom(identifier = problog_formula.get_next_atom_identifier(),
                                         probability = None,
                                         name = Term(idx.split("("[0], *[Constant(c) for c in constants]))))
                atom_dict[idx] = atom
            return atom_dict[idx]
        elif node.op == NOT:
            atom = self._ground(node.children[0], problog_formula, map_constants, atom_dict)
            return problog_formula.get_node(problog_formula.add_not(atom))
        elif node.op == AND:
            atom1 = self._ground(node.children[0], problog_formula, map_constants, atom_dict)
            atom2 = self._ground(node.children[1], problog_formula, map_constants, atom_dict)
            return problog_formula.get_node(problog_formula.add_and([atom1.identifier,atom2.identifier]))
        elif node.op == OR:
            atom1 = self._ground(node.children[0], problog_formula, map_constants, atom_dict)
            atom2 = self._ground(node.children[1], problog_formula, map_constants, atom_dict)
            return problog_formula.get_node(problog_formula.add_or([atom1.identifier,atom2.identifier]))
        else:
            raise Exception("Operator not yet handled for grounding")


#
# predicates = ["A", "B", "C", "D"]
#
# print(Formula(predicates=predicates, definition="(A(X) and B(X)) -> (C(X) <-> D(X))").to_CNF())
# print(Formula(predicates=predicates, definition="(A(X) and B(X)) -> (C(X) <-> D(X))").to_evidence())
# # print(Formula(predicates=predicates, definition="(A(X) and B(X)) or C(X)").to_CNF())