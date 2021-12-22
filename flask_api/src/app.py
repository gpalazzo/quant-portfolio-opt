from flask import Flask
from flask_restful import Api
from resources import HealthCheck, PortfolioOptimizer
from waitress import serve


# flask app
app = Flask(__name__)

# slash trailing disabled, i.e., it responds to call regardless of having a slash (/) at the end of the URL or not
app.url_map.strict_slashes = False

# api structure abstraction from app
api = Api(app)

# endpoints mapping (class name, endpoint)
api.add_resource(HealthCheck, "/health")
api.add_resource(PortfolioOptimizer, "/portfolio_opt")

# serving for all calls through port 5000
if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
