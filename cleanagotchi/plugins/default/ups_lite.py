# Based on UPS Lite v1.1 from https://github.com/xenDE
#
# functions for get UPS status - needs enable "i2c" in raspi-config
#
# https://github.com/linshuqin329/UPS-Lite
#
# For Raspberry Pi Zero Ups Power Expansion Board with Integrated Serial Port S3U4
# https://www.ebay.de/itm/For-Raspberry-Pi-Zero-Ups-Power-Expansion-Board-with-Integrated-Serial-Port-S3U4/323873804310
# https://www.aliexpress.com/item/32888533624.html
import struct

from cleanagotchi.ui.components import LabeledValue
from cleanagotchi.ui.view import BLACK
import cleanagotchi.ui.fonts as fonts
import cleanagotchi.plugins as plugins


# TODO: add enable switch in config.yml an cleanup all to the best place
class UPS:
    def __init__(self):
        # only import when the module is loaded and enabled
        import smbus
        # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self._bus = smbus.SMBus(1)

    def voltage(self):
        try:
            address = 0x36
            read = self._bus.read_word_data(address, 2)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            return swapped * 1.25 / 1000 / 16
        except:
            return 0.0

    def capacity(self):
        try:
            address = 0x36
            read = self._bus.read_word_data(address, 4)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            return swapped / 256
        except:
            return 0.0


class UPSLite(plugins.Plugin):
    __author__ = 'evilsocket@gmail.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin that will add a voltage indicator for the UPS Lite v1.1'

    def __init__(self):
        self.ups = None

    def on_loaded(self):
        self.ups = UPS()

    def on_ui_setup(self, ui):
        ui.add_element('ups', LabeledValue(color=BLACK, label='UPS', value='0%/0V', position=(ui.width() / 2 - 25, 0),
                                           label_font=fonts.Bold, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        ui.set('ups', "%4.2fV/%2i%%" % (self.ups.voltage(), self.ups.capacity()))
