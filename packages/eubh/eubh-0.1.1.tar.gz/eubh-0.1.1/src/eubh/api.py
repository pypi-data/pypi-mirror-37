import json
import urllib3
from requests import *
from .config import Config, VERSION, EUBC_LOCAL_ADDRESS


def get_chain_sync_progress():
    return get('{0}/chain/sync-progress'.format(EUBC_LOCAL_ADDRESS)).json()


def get_eubserver_event():
    return urllib3.PoolManager().request('GET', '{0}/sse'.format(EUBC_LOCAL_ADDRESS), preload_content=False)


class Api:
    def __init__(self, key=None):
        config = Config()
        self.key = key
        self.base_url = config.get('HTTP_ADDRESS')
        self.usb_base_url = config.get('USB_HTTP_ADDRESS')
        self.headers = {'Content-Type': 'application/json', 'API-SECRET': config.get('API_SECRET')}

    def get_url(self, url):
        return '{0}/{1}'.format(self.base_url, url)

    def get_usb_base_url(self, url):
        return '%s/%s' % (self.usb_base_url, url)

    def upload_machine_and_get_task(self, data):
        return post(self.get_url('project/machine/%s' % (data.get('mac'))), data=json.dumps(data),
                    headers=self.headers).json()

    def project_machine_update_cmd(self, data):
        return post(self.get_url('project/machine/%s/update-cmd' % data.get('id')), data=data)

    def store_project_container_log(self, data):
        return post(self.get_url('project/container-log'), data=data)

    def get_project_info_by_key(self):
        return get(self.get_url('project/project/%s' % self.key), headers=self.headers).json()

    def get_project_container_lists(self, key):
        return get(self.get_url('project/container/lists/%s' % key), headers=self.headers).json()

    def get_project_container_logs_by_container_id(self, container_id):
        return get(self.get_url('project/container-log/%s/logs-by-container-id' % container_id)).json()

    def post_project_container_logs(self, data):
        return post(self.get_url('project/container-log/%s/set' % data.get('container_id')), data=data)

    def get_config_by_key(self):
        return self.get_project_info_by_key()

    def get_eubchain(self):
        return get(self.get_usb_base_url(
            '/api/base/geteubchain?version=%s&platform=%s&type=server' % (VERSION, 'linux'))).json()

    def project_store(self, data):
        return post(self.get_url('project/project'), json=data, headers=self.headers).json()

    def project_publish(self, project_id):
        return post(self.get_url('project/project/publish/{0}'.format(project_id))).json()
