#MIT License
#Copyright (c) 2017 Tim Wentzlau

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Hardware abstraction layer"""
import time
from kervi.hal import gpio
#from kervi.hal import i2c
#from kervi.hal import one_wire
from kervi.spine import Spine
from kervi.core.utility.thread import KerviThread
#import pip
import importlib
import os
import kervi.utility
_DRIVER = None
GPIO = None

HAL_DRIVER_ID = None

def _load(hw_platform="auto"):
    global GPIO, _DRIVER, HAL_DRIVER_ID

    if not _DRIVER:
        #installed_packages = pip.get_installed_distributions()
        #kervi_path = os.path.dirname(kervi.utility.__file__)
        #kervi_path = kervi_path[:-8]
        #print("kp", kervi_path )
        #plugin_base = PluginBase(package='kervi.platform.plugins')
        #plugin_source = plugin_base.make_plugin_source(
        #    searchpath=[ kervi_path + "/platforms"]
        #)

        import platform
        #import os
        
        hal_modules = {
            "windows": "kervi.platforms.windows",
            #"linux": "kervi.platforms.linux",
            #"darwin": "kervi.platforms.linux",
            "linux(rpi)": "kervi.platforms.raspberry",
            "generic": "kervi.platforms.generic"
        }
        
        if hw_platform=="auto":
            system = platform.system().lower()
            if system == "linux":
                try:
                    with open('/proc/cpuinfo') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith('Hardware') and line.endswith('BCM2708'):
                                system = "linux(rpi)"
                                break
                            elif line.startswith('Hardware') and line.endswith('BCM2835'):
                                system = "linux(rpi)"
                                break
                            elif line.startswith('Hardware') and line.endswith('BCM2836'):
                                system = "linux(rpi)"
                                break
                            elif line.startswith('Hardware') and line.endswith('BCM2837'):
                                system = "linux(rpi)"
                                break
                except:
                    pass
            if not system in hal_modules.keys():
                system = "generic"
        else:
            system = hw_platform.lower()      
            
        if system in hal_modules.keys():
            module_name = hal_modules[system] 
            _DRIVER = importlib.import_module(module_name)
            HAL_DRIVER_ID = module_name
            GPIO = get_gpio()
            return module_name
        else:
            raise ValueError("Invalid hw_platform. Valid values are: " + str.join(hal_modules.keys()))

        # import pkg_resources
        # installed_packages = pkg_resources.working_set

        # #plugin_list = plugin_source.list_plugins()
        # #print("pl", installed_packages)
        # flat_installed_packages = [package.project_name for package in installed_packages]
        # known_drivers = [
        #     ("kervi-hal-win", "kervi.platforms.windows"),
        #     ("kervi-hal-linux", "kervi.platforms.linux"),
        #     ("kervi-hal-rpi", "kervi.platforms.raspberry"),
        #     ("kervi-hal-generic", "kervi.platforms.generic")
        # ]
        # #print("fip", flat_installed_packages)
        # for driver_name, module_name in known_drivers:
        #     if driver_name in flat_installed_packages:
        #         _DRIVER = importlib.import_module(module_name)
        #         HAL_DRIVER_ID = module_name
        #         GPIO = get_gpio()
        #         return driver_name

def get_user_inputs():
    return _DRIVER.get_user_inputs()

def detect_devices():
    devices = _DRIVER.detect_devices()
    return devices

def get_gpio(gpio_type=None):
    if gpio_type == None:
        return _DRIVER.get_gpio_driver()

def default_i2c_bus():
    if _DRIVER:
        return _DRIVER.default_i2c_bus()
    return 0

def get_i2c(address, bus=default_i2c_bus()):
    return _DRIVER.get_i2c_driver(address, bus)

def get_one_wire(address):
    return _DRIVER.get_one_wire_driver(address)


def get_camera_driver(source = None):
    return _DRIVER.get_camera_driver(source)

def service_commands(commands, app_name, app_id, script_path):
    return _DRIVER.service_commands(commands, app_name, app_id, script_path)


def device_reboot():
    _DRIVER.reboot()

def device_shutdown():
    _DRIVER.shutdown()

#if not _DRIVER:
#    _load()


class SensorDeviceDriver(object):

    @property
    def dimensions(self):
        return 1

    @property
    def dimension_labels(self):
        return []

    @property
    def device_name(self):
        return None

    @property
    def max(self):
        return None

    @property
    def min(self):
        return None

    # @property
    # def sensor_type(self):
    #     raise NotImplementedError

    @property
    def unit(self):
        raise NotImplementedError

    def read_value(self):
        raise NotImplementedError

    @property
    def logger(self):
        return Spine().log

    @property
    def value_type(self):
        return "number"

class I2CaddressOutOfBoundsError(Exception):
    def __init__(self, device_name, address):
        super(I2CaddressOutOfBoundsError, self).__init__(
            '{0} I2C Address Out of Bounds:{1}'.format(device_name, address)
        )

class DeviceChannelOutOfBoundsError(Exception):
    def __init__(self, device_name, channel):
        super(DeviceChannelOutOfBoundsError, self).__init__(
            '{0} Exception: Channel Out of Bounds, channel={1}'.format(device_name, channel)
        )

# Exception class for a DAC value out of bounds
class DACValueOutOfBoundsError(Exception):
    def __init__(self, device_name, channel, value):
        super(DACValueOutOfBoundsError, self).__init__(
            '{0} Exception: DAC Output Value Out of Bounds, channel={1} value={2}'.format(device_name, channel, value)
        )

class I2CSensorDeviceDriver(SensorDeviceDriver):
    def __init__(self, address, bus):
        if address > 0x77:
            raise I2CaddressOutOfBoundsError(self.device_name, address)
        self.i2c = get_i2c(address, bus)

class I2CGPIODeviceDriver(gpio.IGPIODeviceDriver):
    def __init__(self, address, bus, gpio_id):
        gpio.IGPIODeviceDriver.__init__(self, gpio_id)
        if address > 0x77:
            raise I2CaddressOutOfBoundsError(self.device_name, address)
        self.i2c = get_i2c(address, bus)

    @property
    def device_name(self):
        return None

    @property
    def num_gpio(self):
        return 0

    def _bit2(self, src, bit, val):
        bit = 1 << bit
        return (src | bit) if val else (src & ~bit)


    def _validate_channel(self, channel):
        # Raise an exception if pin is outside the range of allowed values.
        if channel < 0 or channel >= self.num_gpio:
            raise DeviceChannelOutOfBoundsError(self.device_name, channel)

class OneWireSensorDeviceDriver(SensorDeviceDriver):
    def __init__(self, address):
        self.one_wire = get_one_wire(address)

class ChannelPollingThread(KerviThread):
    def __init__(self, channel, device, callback, polling_time=.1):
        KerviThread.__init__(self)
        self._callback = callback
        self._channel = channel
        self._device = device
        self._value = None
        self._polling_time = polling_time
        self.alive = False
        self.spine = Spine()
        if self.spine:
            self.spine.register_command_handler("startThreads", self._start_command)
            self.spine.register_command_handler("stopThreads", self._stop_command)

    def _step(self):
        """Private method do not call it directly or override it."""
        try:
            new_value = self._device.get(self._channel)
            if new_value != self._value:
                self._callback(new_value)
                self._value = new_value
            time.sleep(self._polling_time)
        except:
            self.spine.log.exception("_PollingThread")

    def _start_command(self):
        if not self.alive:
            self.alive = True
            KerviThread.start(self)

    def _stop_command(self):
        if self.alive:
            self.alive = False
            self.stop()

