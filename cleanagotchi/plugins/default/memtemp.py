# memtemp shows memory infos and cpu temperature
#
# mem usage, cpu load, cpu temp
#
###############################################################
#
# Updated 18-10-2019 by spees <speeskonijn@gmail.com>
# - Changed the place where the data was displayed on screen
# - Made the data a bit more compact and easier to read
# - removed the label so we wont waste screen space
# - Updated version to 1.0.1
#
# 20-10-2019 by spees <speeskonijn@gmail.com>
# - Refactored to use the already existing functions
# - Now only shows memory usage in percentage
# - Added CPU load
# - Added horizontal and vertical orientation
#
###############################################################
from cleanagotchi.ui.components import LabeledValue
from cleanagotchi.ui.view import BLACK
import cleanagotchi.ui.fonts as fonts
import cleanagotchi.plugins as plugins
import cleanagotchi
import logging


class MemTemp(plugins.Plugin):
    __author__ = 'https://github.com/xenDE'
    __version__ = '1.0.1'
    __license__ = 'GPL3'
    __description__ = 'A plugin that will display memory/cpu usage and temperature'

    def on_loaded(self):
        logging.info("memtemp plugin loaded.")

    def mem_usage(self):
        return int(cleanagotchi.mem_usage() * 100)

    def cpu_load(self):
        return int(cleanagotchi.cpu_load() * 100)

    def on_ui_setup(self, ui):
        if ui.is_waveshare_v2():
            h_pos = (180, 80)
            v_pos = (180, 61)
        else:
            h_pos = (155, 76)
            v_pos = (180, 61)

        if self.options['orientation'] == "horizontal":
            ui.add_element('memtemp', LabeledValue(color=BLACK, label='', value='mem cpu temp\n - -  -',
                                                   position=h_pos,
                                                   label_font=fonts.Small, text_font=fonts.Small))
        elif self.options['orientation'] == "vertical":
            ui.add_element('memtemp', LabeledValue(color=BLACK, label='', value=' mem:-\n cpu:-\ntemp:-',
                                                   position=v_pos,
                                                   label_font=fonts.Small, text_font=fonts.Small))

    def on_ui_update(self, ui):
        if self.options['orientation'] == "horizontal":
            ui.set('memtemp',
                   " mem cpu temp\n %s%% %s%%  %sc" % (self.mem_usage(), self.cpu_load(), cleanagotchi.temperature()))

        elif self.options['orientation'] == "vertical":
            ui.set('memtemp',
                   " mem:%s%%\n cpu:%s%%\ntemp:%sc" % (self.mem_usage(), self.cpu_load(), cleanagotchi.temperature()))
