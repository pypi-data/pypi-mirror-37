import shlex

from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.models.State import State
from apitaxcore.models.Options import Options
from apitaxcore.flow.requests.ApitaxRequest import ApitaxRequest
from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse
from apitaxcore.models.Credentials import Credentials
from commandtax.drivers.Driver import Driver
from commandtax.models.Command import Command

from time import time


# The 'heart' of the application
# Connector facilitates the initialization of the connection to an API
# Connector handles setting up the driver, authetnication, headers, and then
# using all of that to execute a command
#
# Additional interfaces to this utility should directly communicate with connector
# and likely nothing else. Connector handles the rest.
class Connector:

    def __init__(self, options=None, credentials=None, command='', parameters={}, request=None):
        self.options: Options = options if options is not None else Options()
        self.parameters = parameters
        self.credentials: Credentials = credentials if credentials is not None else Credentials()
        self.request: ApitaxRequest = request if request is not None else ApitaxRequest()

        self.command: str = command
        self.command = self.command.replace('\\"', '"')
        self.command = self.command.replace('\\\'', '\'')
        self.command: list = shlex.split(self.command.strip())

        self.executionTime = None
        self.commandtax = None
        self.logBuffer = []

        self.options.driver: Driver = LoadedDrivers.getDriver('commandtax')

        self.request.headerBuilder = self.options.driver.addApiHeaders(self.request.headerBuilder)
        self.request.bodyBuilder = self.options.driver.addApiBody(self.request.bodyBuilder)

    def execute(self) -> ApitaxResponse:
        t0 = time()

        self.commandtax = self.options.driver.handleDriverCommand(
            Command(command=self.command, options=self.options, parameters=self.parameters, request=self.request,
                    credentials=self.credentials))

        self.executionTime = time() - t0

        self.logBuffer = State.log.getLoggerDriver().buffer

        State.log.getLoggerDriver().outputLog()

        return self.commandtax
