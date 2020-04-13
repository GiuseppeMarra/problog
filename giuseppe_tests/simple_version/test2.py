from pysdd.sdd import SddManager, Vtree, WmcManager
from graphviz import Source


vtree = Vtree(var_count=5, var_order=[2,1,4,3,5], vtree_type="balanced")
sdd = SddManager.from_vtree(vtree)
a, b, c, d, e = sdd.vars

# Build SDD for formula
formula = (a & b) | (b & c) | (c & d)
formula = formula & e


# Model Counting
wmc = formula.wmc(log_mode=False)
print(f"Model Count: {wmc.propagate()}")
wmc.set_literal_weight(a, 0.5)
print(f"Weighted Model Count: {wmc.propagate()}")


s = Source(formula.dot(), filename="output/sdd.dot", format="png")
s.view()

s2 = Source(vtree.dot(), filename="output/vtree.dot", format="png")
s2.view()