from apitaxcore.drivers.Driver import Driver as BaseDriver
from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse

from commandtax.catalogs.CommandCatalog import CommandCatalog
from commandtax.models.Command import Command


# Base class for driver plugs
# Defines many customizable properties for interfacing to a new API type
class Driver(BaseDriver):
    # Whether Driver supports a custom command handler
    def isDriverCommandable(self) -> bool:
        return False

    # If driver is commandable, returns the driver command catalog
    def getDriverCommandCatalog(self) -> CommandCatalog:
        return CommandCatalog()

    # Driver command handler
    def handleDriverCommand(self, command: Command) -> ApitaxResponse:
        return ApitaxResponse()

    # Event handler fired before the driver command handler executes
    def onPreHandleDriverCommand(self, command: Command) -> Command:
        return command