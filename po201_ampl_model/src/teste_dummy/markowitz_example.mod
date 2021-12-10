set A; #assets
set T := {1..100};

param Rets {T, A}; #returns on assets
param mean {j in A} = (sum {i in T} Rets[i, j]) / card(T);
param Diff {i in T, j in A} = Rets[i, j] - mean[j];
param Covar {i in A, j in A} = sum {k in T} (Diff[k, i] * Diff[k, j]) / (card{T}-1);

var w {A} >= 0;
var Mean = sum {j in A} mean[j] * w[j];

minimize Risk: sum {i in A} (w[i] * (sum {j in A} Covar[i, j] * w[j]));

subject to TotalOne: sum {j in A} w[j] = 1;
subject to LongOnly {j in A}: 0 <= w[j] <= 1;
subject to Reve: Mean >= 0.035;