reset;

set A; #assets
set T := {1..12};

param Rets {T, A}; #returns on assets
param mean {j in A} = (sum {i in T} Rets[i, j]) / card(T);
param Diff {i in T, j in A} = Rets[i, j] - mean[j];
param Covar {i in A, j in A} = sum {k in T} (Diff[k, i] * Diff[k, j]) / (card{T}-1);

var X {A} >= 0;
var Mean = sum {j in A} mean[j] * X[j];

minimize Risk: sum {i in A} (X[i] * (sum {j in A} Covar[i, j] * X[j]));

subject to TotalOne: sum {j in A} X[j] = 1;
subject to Reve: Mean >= 0.035;