0.5::a.
0.5::b.

c1 :- a , b.
c2 :- a ; b.

mln_constraint(c1, t(0.2)).
mln_constraint(c2, t(0.2)).