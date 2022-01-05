## Quant Portfolio Optimization Back-end
![alt text](../assets/images/logos/postgresql.png "PostgreSQL Logo")

`PostgreSQL` is acting as the back-end for all data storage in the project.

It interacts with `Apache Airflow`, `Flask API` and `Kedro`. It can be considered the heart
of the entire service given the fact there's no optimization running even if all the other
services are healthy.