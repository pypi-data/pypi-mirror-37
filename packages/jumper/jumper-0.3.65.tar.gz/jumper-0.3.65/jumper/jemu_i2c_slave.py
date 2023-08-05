class JemuI2cSlave(object):
    def __init__(self):
        pass

    def on_read(callback):
        """
        Registers a callback to be called when the master is trying to read from the slave.

        :param callback: A callback function that will be called with the following arguments (device_address, read_index, num_bytes). The callback must return a tuple: (ack, response).
        """
        pass

    def on_write(callback):
        """
        Registers a callback to be called when the master is trying to write to the slave.

        :param callback: A callback function that will be called with the following arguments (device_address, write_index, data). The callback must return the ack as True/False.
        """
        pass

    def on_start(callback):
        """
        Registers a callback to be called when the master is sending a start signal.

        :param callback:
        """
        pass

    def on_stop(callback):
        """
        Registers a callback to be called when the master is sending a stop signal.

        :param callback:
        """
        pass
