# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
import ipaddress
import threading

import requests
import xmltodict

import application
from signals import successful_connection, connection_error

class SkyPlusBox(object):
    def __init__(self, ip_address, skyplay_data):
        self.ip_address = ip_address
        skyplay_data = skyplay_data
        device_data = skyplay_data['root']['device']
        self.model = '{0}/{1}/{2}'.format(
            device_data['modelName'],
            device_data['modelDescription'],
            device_data['modelNumber']
        )
        self.friendly_name = device_data['friendlyName']
        self.manufacturer = device_data['manufacturer']
        self.chip_id = device_data['nds:X_NDS_ChipID']['#text']
        self.udn = device_data['UDN']



class ConnectionThread(threading.Thread):
    def __init__(self, ip_address, *args, **kwargs):
        super(ConnectionThread, self).__init__(*args, **kwargs)
        self.daemon = True
        self.ip_address = ip_address
        self.start()

    def run(self):
        try:
            ip = ipaddress.ip_address(self.ip_address)
        except ValueError:
            connection_error.send(self, error_msg='{0} is not a valid IP address.'.format(self.ip_address))
            return

        session = requests.Session()
        session.headers['User-Agent'] = 'SKY_skyplus'
        port = 49153
        description_file = 'description0.xml'
        url = 'http://{ip}:{port}/{description_file}'.format(ip=self.ip_address, port=port, description_file=description_file)
        try:
            response = session.get(url, timeout=application.config['request_timeout'])
            response.raise_for_status()
        except Exception as e:
            connection_error.send(self, error_msg=str(e))
            return

        xml = response.content
        data = xmltodict.parse(xml)
        application.box = SkyPlusBox(self.ip_address, data)
        successful_connection.send(self)



def connect_to_box(ip_address):
    connection_thread = ConnectionThread(ip_address)
