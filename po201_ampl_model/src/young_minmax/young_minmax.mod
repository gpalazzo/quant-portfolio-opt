reset;

# default values
param u default 1.0; # Upper limit for investing in a single share
param W default 50000.0; # budget
param G default 0.035; # target return of the portfolio
param T default 67; # number of months

# sets definition
set A; #assets

# parameter definition
param n = card(A); # number of shares
param RetMat{1..T, A}; # historic monthly returns for selected shares

param ExpRet{j in A} = sum{i in 1..T} RetMat[i,j]/T; # expected returns of shares
param stdv{j in A} = sqrt((sum{i in 1..T} (RetMat[i,j] - ExpRet[j])^2)/T); # standard deviation of shares
param Mp{j in A} = ExpRet[j]-stdv[j]; # minimum portfolio

# variable definition
var w{A} >= 0;

# objective function
maximize MinimumReturn: sum {j in A} w[j]*Mp[j];

# constraints
subject to TargetReturn: sum {j in A} ExpRet[j]*w[j] >= G;
subject to Budget: sum {j in A} w[j] <= W;
subject to bounds {j in A}: 0 <= w[j] <= u;
subject to TotalOne: sum {j in A} w[j] = 1;

