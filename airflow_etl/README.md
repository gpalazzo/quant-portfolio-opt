## Quant Portfolio Optimization ETL

`Airflow` is acting as the data orchestrator and producer
for the entire project. It's the entrypoint for all data
acquisition processes.

The data acquisition process is divided by data domains. In
this particular use case, data domains are driven by the
data source.

The ETL inside each data domain is divided in 3
parts:

1. `Raw`
2. `Intermediate`
3. `Primary`