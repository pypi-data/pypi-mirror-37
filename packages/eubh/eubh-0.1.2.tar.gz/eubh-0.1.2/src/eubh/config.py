from configparser import ConfigParser
from click import echo
from os.path import expanduser

home = expanduser("~")

VERSION = '0.1.2'
ROOT_DIR = '/root'

HOST_ADDRESS = 'eubflow.eubchain.com'
HTTP_ADDRESS = 'https://{0}'.format(HOST_ADDRESS)
WS_ADDRESS = 'wss://{0}:54188'.format(HOST_ADDRESS)
EUBC_SERVER_ADDRESS = 'http://localhost:8088'
USB_HTTP_ADDRESS = 'https://usb.eubchain.com'

EUBC_LOCAL_ADDRESS = 'http://localhost:8088'

ENABLE_VERBOSE = False
DOCKER_WHITE_LIST = ['rancher_agent', 'eubc_docker_white_list']
CONFIG_FILE_LOCATION = '{0}/.eubc_config.ini'.format(home)

DEFAULT_CONFIG = {
    'USB_HTTP_ADDRESS': USB_HTTP_ADDRESS,
    'HOST_ADDRESS': HOST_ADDRESS,
    'HTTP_ADDRESS': HTTP_ADDRESS,
    'WS_ADDRESS': WS_ADDRESS,
    'EUBC_ADDRESS_PRIVATE': None,
    'EUBC_SERVER_ADDRESS': EUBC_SERVER_ADDRESS,
    'API_SECRET': None
}


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE_LOCATION)

    def set(self, key, value):
        if key in DEFAULT_CONFIG.keys():
            self.config.set('DEFAULT', key.lower(), value)
            with open(CONFIG_FILE_LOCATION, 'w+') as config_file:
                self.config.write(config_file)
        else:
            echo('Unsupported configuration information')

    def get(self, key):
        return self.config.get('DEFAULT', key.lower(), fallback=DEFAULT_CONFIG[key.upper()])
