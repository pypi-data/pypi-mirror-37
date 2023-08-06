from apitaxcore.models.Options import Options
from apitaxcore.flow.requests.ApitaxRequest import ApitaxRequest
from apitaxcore.models.Credentials import Credentials


class Command:
    def __init__(self, command: list = None, request: ApitaxRequest = None, parameters: dict = None,
                 options: Options = None, credentials: Credentials = None):
        self.command = command
        self.options = options
        self.request = request
        self.parameters = parameters
        self.credentials = credentials
