% Duplicate fact. Interpret as two separate facts.
%Expected outcome:
% a(john) 0.90909091
% b(john) 0.090909091

person(john).
likesSoccer(john).
0.5::a(X); 0.5::b(X):-person(X).
0.9::a(X):-likesSoccer(X).

mutually_exclusive(X) :- a(X), \+ b(X).
mutually_exclusive(X) :- b(X), \+ a(X).
constraint(mutually_exclusive(X)).

query(a(john)).
query(b(john)).