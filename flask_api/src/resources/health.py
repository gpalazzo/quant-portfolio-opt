from flask_restful import Resource
from flasgger.utils import swag_from
from pathlib import Path


# get the path to the root project directory
project_dir = Path(__file__).resolve().parents[2]


class HealthCheck(Resource):
    """
    Class only used as health check return
    It should return a HTTP 200 response code when invoked
    """

    @staticmethod
    @swag_from(f"{project_dir}/conf/endpoints/health.yml")
    def get() -> str:
        """
        Will be activated when the endpoint receives a HTTP GET method

        Returns:
             string only aiming a HTTP 200 response code
        """

        return "OK"
