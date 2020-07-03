from pysdd.sdd import SddManager, Vtree, WmcManager
vtree = Vtree(var_count=4, var_order=[2,1,4,3], vtree_type="balanced")
sdd = SddManager.from_vtree(vtree)
a, b, c, d = sdd.vars

# Build SDD for formula
formula = (a & b & c & d)


# Model Counting
wmc1 = formula.wmc(log_mode=False)
print(f"Model Count: {wmc1.propagate()}")
wmc1.set_literal_weight(a, 0.5)
print(f"Weighted Model Count: {wmc1.propagate()}")

