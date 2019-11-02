from cleanagotchi.ui.hw.inky import Inky
from cleanagotchi.ui.hw.papirus import Papirus
from cleanagotchi.ui.hw.oledhat import OledHat
from cleanagotchi.ui.hw.lcdhat import LcdHat
from cleanagotchi.ui.hw.dfrobot import DFRobot
from cleanagotchi.ui.hw.waveshare1 import WaveshareV1
from cleanagotchi.ui.hw.waveshare2 import WaveshareV2
from cleanagotchi.ui.hw.waveshare27inch import Waveshare27inch
from cleanagotchi.ui.hw.waveshare154inch import Waveshare154inch
from cleanagotchi.ui.hw.waveshare213d import Waveshare213d


def display_for(config):
    # config has been normalized already in utils.load_config
    if config['ui']['display']['type'] == 'inky':
        return Inky(config)

    elif config['ui']['display']['type'] == 'papirus':
        return Papirus(config)

    if config['ui']['display']['type'] == 'oledhat':
        return OledHat(config)

    if config['ui']['display']['type'] == 'lcdhat':
        return LcdHat(config)

    if config['ui']['display']['type'] == 'dfrobot':
        return DFRobot(config)

    elif config['ui']['display']['type'] == 'waveshare_1':
        return WaveshareV1(config)

    elif config['ui']['display']['type'] == 'waveshare_2':
        return WaveshareV2(config)

    elif config['ui']['display']['type'] == 'waveshare27inch':
        return Waveshare27inch(config)

    elif config['ui']['display']['type'] == 'waveshare154inch':
        return Waveshare154inch(config)

    elif config['ui']['display']['type'] == 'waveshare213d':
        return Waveshare213d(config)