import logging

log = logging.getLogger(__name__)

##
# volatile attributes (must persist here for multi-spectrometers)
#
# Note that these should generally not include READOUTS from the 
# spectrometer like temperature, ADC etc...unless that proves convenient.
#
class SpectrometerState(object):

    TRIGGER_SOURCE_INTERNAL = 0
    TRIGGER_SOURCE_EXTERNAL = 1

    BAD_PIXEL_MODE_NONE     = 0
    BAD_PIXEL_MODE_AVERAGE  = 1

    def __init__(self):

        # detector
        self.integration_time_ms = 0

        # TEC
        self.tec_setpoint_degC = 15
        self.tec_enabled = False

        # high gain mode (InGaAs only)
        self.high_gain_mode_enabled = False

        # laser
        self.laser_enabled = False
        self.laser_power_in_mW = False
        self.laser_power = 0
        self.laser_temperature_setpoint_raw = 0
        self.selected_adc = None

        # triggering
        self.trigger_source = self.TRIGGER_SOURCE_INTERNAL

        # area scan mode
        self.area_scan_enabled = False

        # ######################################################################
        # What about "application state", which is never actually set in the
        # hardware?  Move these later to ".software" or ".processing" or whatever?
        #
        # The real line-in-the-sand here is that these are all set by the user 
        # in the GUI via on-screen widgets, and THEREFORE will need somewhere to 
        # retain state when "other" spectrometers have the foreground, and 
        # THEREFORE might as well be in here.  Wasatch.PY might as well make use 
        # of them.
        # ######################################################################

        # scan averaging
        self.scans_to_average = 1

        # boxcar 
        self.boxcar_half_width = 0

        # background subtraction
        self.background_subtraction_half_width = 0

        # bad pixel removal
        self.bad_pixel_mode = self.BAD_PIXEL_MODE_AVERAGE

        # USB comms
        self.min_usb_interval_ms = 0
        self.max_usb_interval_ms = 0

        # secondary ADC
        self.secondary_adc_enabled = False

        # detector inversion (typically applied in Wasatch.PY)
        self.invert_x_axis = False

        # laser power ramping
        self.laser_power_ramping_enabled = False
        self.laser_power_ramp_increments = 100

        # pixel binning
        self.graph_alternating_pixels = False

        # ######################################################################
        # What about truly internal settings like last_applied_laser_power or 
        # detector_tec_setpoint_has_been_set?  It's okay for StrokerProtocolDevice,
        # FeatureIdentificationDevice and control.py to have "some" internal state.
        # Line-in-the-sand is to include here if MULTIPLE files would need to 
        # persist the same information in the same way (providing consistent
        # implementation without copy-paste), OR if the information is actually
        # passed between files in some way (such that verification of internal
        # representation consistency reduces risk of bugs/errors).
        # ######################################################################

    def stringify_trigger_source(self):
        if self.trigger_source == self.TRIGGER_SOURCE_EXTERNAL:
            return "EXTERNAL"
        elif self.trigger_source == self.TRIGGER_SOURCE_INTERNAL:
            return "INTERNAL"
        else:
            return "ERROR"

    def stringify_bad_pixel_mode(self):
        if self.bad_pixel_mode == self.BAD_PIXEL_MODE_AVERAGE:
            return "AVERAGE"
        elif self.bad_pixel_mode == self.BAD_PIXEL_MODE_NONE:
            return "NONE"
        else:
            return "ERROR"

    def dump(self):
        log.info("SpectrometerState:")
        log.info("  Integration Time:       %dms", self.integration_time_ms)
        log.info("  TEC Setpoint:           %.2f degC", self.tec_setpoint_degC)
        log.info("  TEC Enabled:            %s", self.tec_enabled)
        log.info("  High Gain Mode Enabled: %s", self.high_gain_mode_enabled)
        log.info("  Laser Enabled:          %s", self.laser_enabled)
        log.info("  Laser Power:            %.2f", self.laser_power)
        log.info("  Laser Temp Setpoint:    0x%04x", self.laser_temperature_setpoint_raw)
        log.info("  Selected ADC:           %s", self.selected_adc)
        log.info("  Trigger Source:         %s", self.stringify_trigger_source())
        log.info("  Area Scan Enabled:      %s", self.area_scan_enabled)
        log.info("  Scans to Average:       %d", self.scans_to_average)
        log.info("  Boxcar Half-Width:      %d", self.boxcar_half_width)
        log.info("  Background Subtraction: %d", self.background_subtraction_half_width)
        log.info("  Bad Pixel Mode:         %s", self.stringify_bad_pixel_mode())
        log.info("  USB Interval:           (%d, %dms)", self.min_usb_interval_ms, self.max_usb_interval_ms)
        log.info("  Secondary ADC Enabled:  %s", self.secondary_adc_enabled)
        log.info("  Invert X-Axis:          %s", self.invert_x_axis)
        log.info("  Laser Power Ramping:    %s", self.laser_power_ramping_enabled)
        log.info("  Laser Power Ramp Incr:  %d", self.laser_power_ramp_increments)
