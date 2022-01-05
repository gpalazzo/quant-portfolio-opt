## Quant Portfolio Optimization Model
![alt text](../assets/images/logos/kedro_logo.png "Kedro Logo")

`Kedro` is acting as the ML Ops framework for building models.
The only model implemented so far is the `Black-Litterman (BL)`.

It starts consuming data from the `Primary` layer of `Airflow` service. Then it pre-process this data in `Kedro's` 
feature layer by filtering a target lower bound date and also inputting data in Null values.

After having a processed dataset it then starts the optimization process by using the BL methods
of the `PyPortfolioOpt` package.

## Kedro additional information
- Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.
- Package your Kedro project: [Further information about building project documentation and packaging your project](https://kedro.readthedocs.io/en/stable/03_tutorial/05_package_a_project.html)