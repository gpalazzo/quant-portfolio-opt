from flask import Flask
from flask_restful import Api
from resources import (
    HealthCheck,
    PortfolioOptimizer,
    OptimizationResults,
    AvailableTickers,
)
from waitress import serve
from flasgger import Swagger


# flask app
app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Quant Portfolio Optimizer API",
    "description": "API for optimizing assets allocation",
    "version": "1.0.0",
    "termsOfService": "",
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs",
}

# slash trailing disabled, i.e., it responds to call regardless of having a slash (/) at the end of the URL or not
app.url_map.strict_slashes = False

swagger = Swagger(app, config=swagger_config)

# api structure abstraction from app
api = Api(app)

# endpoints mapping (class name, endpoint)
api.add_resource(HealthCheck, "/health")
api.add_resource(PortfolioOptimizer, "/portfolio_optimize")
api.add_resource(OptimizationResults, "/optimization_results")
api.add_resource(AvailableTickers, "/available_tickers")

# serving for all calls through port 5000
if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
