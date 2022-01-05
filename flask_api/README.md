## Quant Portfolio Optimization API
![alt text](../assets/images/logos/flask_logo.png "Flask Logo")

This API is the entrypoint for external users in the optimization process.

It's compound by 4 endpoints. The endpoints are currently shown as `localhost` but it's just a matter of changing it to
the right host when using the service.

API's endpoints documentation and experimentation can be found in Swagger
at URL: **http://localhost:5000/apidocs**

1. `Health Check`
    - Returns the _OK_ string
    - It's used to see if the service is healthy
    - Endpoint URL: **http://localhost:5000/health**


2. `Available Tickers`
    - Returns a list of available tickers for optimization
    - Endpoint URL: **http://localhost:5000/available_tickers**


3. `Optimization Request`
    - Starts the optimization process
    - Receives a list of assets to be optimized
    - Returns the `uuid` to be used to retrieve optimization results
    - Endpoint URL: **http://localhost:5000/portfolio_optimize**


4. `Optimization Results`
    - Retrieve optimization results
    - Receives an `uuid` representing the optimization
    - Returns the weights for each asset in the portfolio
    - Endpoint URL: **http://localhost:5000/optimization_results**
