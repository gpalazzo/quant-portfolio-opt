from flask_restful import Resource
from flasgger.utils import swag_from
from pathlib import Path


# get the path to the root project directory
project_dir = Path(__file__).resolve().parents[2]


class HealthCheck(Resource):
    @staticmethod
    @swag_from(
        f"{project_dir}/conf/endpoints/health.yml"
    )  # parse swagger docs from file
    def get() -> str:
        """Invoked when endpoint receives HTTP GET method

        Returns:
             string only aiming a HTTP 200 response code
        """

        return "OK"
