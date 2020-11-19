0.5::a.
0.5::b.
c :- a ; b.
t(0.2)::c_aux.
c_iff :- c, c_aux.
c_iff :- \+c, \+c_aux.

constraint(c_iff).
%mln_constraint(c, t(_)).