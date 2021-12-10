set A; #ativos
set T; #total de linhas do dataframe

param retorno_ativos {T, A};
param retorno_medio {j in A} = (sum {i in T} retorno_ativos[i, j]) / card(T);
param retorno_desvpad {i in T, j in A} = retorno_ativos[i, j] - retorno_medio[j];
param retorno_covar {i in A, j in A} = sum {k in T} (retorno_desvpad[k, i] * retorno_desvpad[k, j]) / (card{T}-1);

var pesos {A} >= 0;
var media_portfolio = sum {j in A} retorno_medio[j] * pesos[j];

minimize risco_portfolio: sum {i in A} (pesos[i] * (sum {j in A} retorno_covar[i, j] * pesos[j]));

subject to soma_pesos_um: sum {j in A} pesos[j] = 1;
subject to sem_alavancagem {j in A}: 0 <= pesos[j] <= 1;
subject to media_min_esperada: media_portfolio >= 0.05;