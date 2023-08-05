from .config import Config
from requests import get, post, put
from jwt import encode
from click import echo


class EubcServerApi:
    def __init__(self):
        config = Config()
        self.config = config
        self.eubc_server_url = config.get('EUBC_SERVER_ADDRESS')

    def get_eubc_server_url(self, url):
        return '{0}{1}'.format(self.eubc_server_url, url)

    def get_eubc_account(self):
        return get(self.get_eubc_server_url('/account')).json()

    def generate_secret_data(self, url, data={}):
        return encode(data, self.get_eubc_account().get('address') + '/' + url)

    def create_eubc_account(self, url='/account/create'):
        return post(self.get_eubc_server_url(url), data={'data': self.generate_secret_data(url)}).json()

    def task_info(self, task_id):
        url = '/tasks/{0}'.format(task_id)
        return get(self.get_eubc_server_url(url)).json()

    def task_accept(self, task_id):
        url = '/tasks/{0}/accept'.format(task_id)
        return put(self.get_eubc_server_url(url), data={'data': self.generate_secret_data(url)}).json()

    def task_request(self, data, url='/tasks/request'):
        return post(self.get_eubc_server_url(url),
                    json={'data': self.generate_secret_data(url, data)}).json()

    def import_private_key(self, address_private_key=None, url='/account/importPrivateKey'):
        if not address_private_key:
            address_private_key = self.config.get('EUBC_ADDRESS_PRIVATE')
        if address_private_key:
            return post(self.get_eubc_server_url(url),
                        data={'data': self.generate_secret_data(url, {'privateKey': address_private_key})}).json()
        else:
            echo('Creating new privateKey')
            account = self.create_eubc_account()
            echo('Eubc address created ,address :{0},privateKey:{1}'.format(account.get('address'),
                                                                            account.get('privateKey')))
            self.config.set('EUBC_ADDRESS_PRIVATE', account.get('privateKey'))
            self.import_private_key()
