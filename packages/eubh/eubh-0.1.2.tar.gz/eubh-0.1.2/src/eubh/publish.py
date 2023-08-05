from .utils import check_api_secret_is_correct
from .api import Api


def publish():
    if check_api_secret_is_correct():
        api = Api()
        response = api.project_publish()
