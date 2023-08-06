# System import
import shlex

# Application import
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse

from commandtax.drivers.Driver import Driver
from commandtax.models.Command import Command


# Command is used to distribute the workload amoung a heirarchy of possible handlers
# Command is the 'brain' of the application
class Commandtax(Driver):

    def isDriverCommandable(self) -> bool:
        return True

    def getDriverName(self) -> str:
        return 'commandtax'

    def getDriverDescription(self) -> str:
        return 'Provides a method of executing commands'

    def getDriverHelpEndpoint(self) -> str:
        return 'coming soon'

    def getDriverTips(self) -> str:
        return 'coming soon'

    def handleDriverCommand(self, command: Command) -> ApitaxResponse:
        response: ApitaxResponse = ApitaxResponse()

        driverName = None

        if len(command.command) < 1:
            return response.res_bad_request(body={
                'error': 'Improper command: `blank` command was attempted.'})

        if '--apitax-debug' in command.command:
            command.options.debug = True
            del command.command[command.command.index('--apitax-debug')]

        if '--apitax-sensitive' in command.command:
            command.options.sensitive = True
            del command.command[command.command.index('--apitax-sensitive')]

        if '--apitax-driver' in command.command:
            driverName = command.command[command.command.index('--apitax-driver') + 1]
            del command.command[command.command.index('--apitax-sensitive') + 1]
            del command.command[command.command.index('--apitax-driver')]

        if driverName:
            command.options.driver = LoadedDrivers.getDriver(driverName)
        elif LoadedDrivers.getDriver(command.command[0]):
            command.options.driver = LoadedDrivers.getDriver(command.command[0])
            del command.command[0]
        else:
            command.options.driver = LoadedDrivers.getPrimaryDriver()

        if not command.options.driver:
            return response.res_server_error(body={
                'error': 'Could not find a valid driver to use for command: ' + str(command.command)})

        command.command = Command(command=command.command, request=command.request, parameters=command.parameters,
                                  options=command.options)

        if command.options.driver.isDriverCommandable():
            if command.options.driver.isApiAuthenticated():
                self.authenticate(command)
            response = command.options.driver.handleDriverCommand(command.command)
        else:
            return response.res_server_error(body={
                'error': 'Driver `' + command.options.driver.getDriverName() + '` does not support this operation: ' + str(
                    command.command)})

        return response

    # HELPERS >>>>

    # TODO: dont authenticate if credentials already exist for tokens
    def authenticate(self, command: Command):
        if command.options.driver.isApiAuthenticated():
            if command.options.driver.isApiAuthenticationSeparateRequest():
                if command.options.driver.isApiTokenable():
                    command.credentials.token = command.options.driver.getApiToken(
                        command.options.driver.authenticateApi(command.credentials)).token
            else:
                command.request.headerBuilder = command.options.driver.addApiAuthHeader(command.request.headerBuilder)
                command.request.bodyBuilder = command.options.driver.addApiAuthBody(command.request.bodyBuilder)
