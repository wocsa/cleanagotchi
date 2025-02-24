import logging
import json
import os
import requests
import cleanagotchi.plugins as plugins
from cleanagotchi.utils import StatusFile

MOZILLA_API_URL = 'https://location.services.mozilla.com/v1/geolocate?key={api}'


class NetPos(plugins.Plugin):
    __author__ = 'zenzen san'
    __version__ = '2.0.0'
    __license__ = 'GPL3'
    __description__ = """Saves a json file with the access points with more signal
                         whenever a handshake is captured.
                         When internet is available the files are converted in geo locations
                         using Mozilla LocationService """

    def __init__(self):
        self.report = StatusFile('/root/.net_pos_saved', data_format='json')
        self.skip = list()
        self.ready = False

    def on_loaded(self):
        if 'api_key' not in self.options or ('api_key' in self.options and self.options['api_key'] is None):
            logging.error("NET-POS: api_key isn't set. Can't use mozilla's api.")
            return

        self.ready = True
        logging.info("net-pos plugin loaded.")

    def _append_saved(self, path):
        to_save = list()
        if isinstance(path, str):
            to_save.append(path)
        elif isinstance(path, list):
            to_save += path
        else:
            raise TypeError("Expected list or str, got %s" % type(path))

        with open('/root/.net_pos_saved', 'a') as saved_file:
            for x in to_save:
                saved_file.write(x + "\n")

    def on_internet_available(self, agent):
        if self.ready:
            config = agent.config()
            display = agent.view()
            reported = self.report.data_field_or('reported', default=list())
            handshake_dir = config['bettercap']['handshakes']

            all_files = os.listdir(handshake_dir)
            all_np_files = [os.path.join(handshake_dir, filename)
                            for filename in all_files
                            if filename.endswith('.net-pos.json')]
            new_np_files = set(all_np_files) - set(reported) - set(self.skip)

            if new_np_files:
                logging.info("NET-POS: Found %d new net-pos files. Fetching positions ...", len(new_np_files))
                display.set('status', f"Found {len(new_np_files)} new net-pos files. Fetching positions ...")
                display.update(force=True)
                for idx, np_file in enumerate(new_np_files):

                    geo_file = np_file.replace('.net-pos.json', '.geo.json')
                    if os.path.exists(geo_file):
                        # got already the position
                        reported.append(np_file)
                        self.report.update(data={'reported': reported})
                        continue

                    try:
                        geo_data = self._get_geo_data(np_file)  # returns json obj
                    except requests.exceptions.RequestException as req_e:
                        logging.error("NET-POS: %s", req_e)
                        self.skip += np_file
                        continue
                    except json.JSONDecodeError as js_e:
                        logging.error("NET-POS: %s", js_e)
                        self.skip += np_file
                        continue
                    except OSError as os_e:
                        logging.error("NET-POS: %s", os_e)
                        self.skip += np_file
                        continue

                    with open(geo_file, 'w+t') as sf:
                        json.dump(geo_data, sf)

                    reported.append(np_file)
                    self.report.update(data={'reported': reported})

                    display.set('status', f"Fetching positions ({idx + 1}/{len(new_np_files)})")
                    display.update(force=True)

    def on_handshake(self, agent, filename, access_point, client_station):
        netpos = self._get_netpos(agent)
        netpos_filename = filename.replace('.pcap', '.net-pos.json')
        logging.info("NET-POS: Saving net-location to %s", netpos_filename)

        try:
            with open(netpos_filename, 'w+t') as net_pos_file:
                json.dump(netpos, net_pos_file)
        except OSError as os_e:
            logging.error("NET-POS: %s", os_e)

    def _get_netpos(self, agent):
        aps = agent.get_access_points()
        netpos = dict()
        netpos['wifiAccessPoints'] = list()
        # 6 seems a good number to save a wifi networks location
        for access_point in sorted(aps, key=lambda i: i['rssi'], reverse=True)[:6]:
            netpos['wifiAccessPoints'].append({'macAddress': access_point['mac'],
                                               'signalStrength': access_point['rssi']})
        return netpos

    def _get_geo_data(self, path, timeout=30):
        geourl = MOZILLA_API_URL.format(api=self.options['api_key'])

        try:
            with open(path, "r") as json_file:
                data = json.load(json_file)
        except json.JSONDecodeError as js_e:
            raise js_e
        except OSError as os_e:
            raise os_e

        try:
            result = requests.post(geourl,
                                   json=data,
                                   timeout=timeout)
            return result.json()
        except requests.exceptions.RequestException as req_e:
            raise req_e
