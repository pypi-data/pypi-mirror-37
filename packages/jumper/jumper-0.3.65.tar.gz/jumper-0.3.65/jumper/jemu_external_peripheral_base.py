
from jemu_peripheral import JemuPeripheral


class ExternalPeripheralBase(JemuPeripheral):

    def __init__(self, jemu_connection, id, peripheral_type, generators):
        JemuPeripheral.__init__(self, jemu_connection, id, peripheral_type, generators)

    def send_command(self, command):
        return self._jemu_connection.send_command(command, self._id, self._peripheral_type)


