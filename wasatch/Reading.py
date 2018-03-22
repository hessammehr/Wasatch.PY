import datetime
import logging

log = logging.getLogger(__name__)

class Reading(object):
    """ A single set of data read from a device. This includes spectrum,
        temperature, gain, offset, etc. Essentially a snapshot of the device
        state in time. """

    def __init__(self):
        super(Reading, self).__init__()
        log.debug("%s setup", self.__class__.__name__)

        self.timestamp = datetime.datetime.now()

        # MZ: hardcode
        self.spectrum                  = [0] * 1024
        self.laser_temperature_raw     = 0
        self.laser_temperature_degC    = 0
        self.detector_temperature_raw  = 0
        self.detector_temperature_degC = 0
        self.laser_status              = None
        self.failure                   = None
        self.averaged                  = False