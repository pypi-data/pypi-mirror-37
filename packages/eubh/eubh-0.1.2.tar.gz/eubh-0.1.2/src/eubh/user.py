# coding=utf-8
import webbrowser
from .config import Config
from click import echo
from .eubc_server_api import EubcServerApi


def login():
    webbrowser.open('http://eubflow.eubchain.local/user/admin')
    api_secret = raw_input('输入Api Secret:')
    config = Config()
    config.set('API_SECRET', api_secret)
    echo('Login success')


def import_private_key(private_key):
    api = EubcServerApi()
    api.import_private_key(private_key)
    echo('Import privateKey success')
