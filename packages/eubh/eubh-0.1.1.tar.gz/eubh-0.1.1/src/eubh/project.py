# coding=utf-8
import os

import pick
import click
from configparser import ConfigParser
from .api import *
from .utils import get_ifn_exit, get_bool
from .eubc_server_api import EubcServerApi
from .put import Put
from .server import ClientSSE
from .project_client import ProjectClient

current_config_folder = '{0}/.eub'.format(os.path.abspath('.'))
config_path = '{0}/.config'.format(current_config_folder)


class Project:
    def __init__(self):
        if not os.path.exists(current_config_folder):
            os.makedirs(current_config_folder)
        config = ConfigParser()
        config.read('{0}/.config'.format(current_config_folder))
        self.config = config
        self.api = Api()
        self.eubc_server_api = EubcServerApi()

    def init(self):
        global project_name, project_description, azure_account_name, azure_secret, min_lan, project_type, timeout_seconds, task_reward
        get_ifn_exit('API_SECRET')
        address_private = get_ifn_exit('EUBC_ADDRESS_PRIVATE')
        import_private_key_response = response = self.eubc_server_api.import_private_key(address_private)
        if response.get('status') == 'error':
            click.echo(import_private_key_response.get('message'))
            exit(0)

        project_name = self.config.get('DEFAULT', 'project_name', fallback=None)
        if not project_name:
            project_name = raw_input('请输入项目名称:')
            self.config.set('DEFAULT', 'project_name', project_name)
        project_description = self.config.get('DEFAULT', 'project_description', fallback=None)
        if not project_description:
            project_description = raw_input('请输入项目描述:')
            self.config.set('DEFAULT', 'project_description', project_description)
        azure_account_name = self.config.get('DEFAULT', 'azure_account_name', fallback=None)
        if not azure_account_name:
            azure_account_name = raw_input('请输入Azure账号名称(AccountName):')
            self.config.set('DEFAULT', 'azure_account_name', azure_account_name)
        azure_secret = self.config.get('DEFAULT', 'azure_secret', fallback=None)
        if not azure_secret:
            azure_secret = raw_input('请输入Azure密钥(Secret):')
            self.config.set('DEFAULT', 'azure_secret', azure_secret)
        min_lan = self.config.get('DEFAULT', 'min_lan', fallback=None)
        if not min_lan:
            min_lan = raw_input('请输入需要的闲置资源数:')
            self.config.set('DEFAULT', 'min_lan', min_lan)
        project_type = self.config.get('DEFAULT', 'project_type', fallback=None)
        if not project_type:
            project_type, index = pick.pick(['EubFlow', 'EubRending'], 'Project type:')
            self.config.set('DEFAULT', 'project_type', project_type)
        timeout_seconds = self.config.get('DEFAULT', 'timeout_seconds', fallback=None)
        if not timeout_seconds:
            timeout_seconds = raw_input('项目超时时间(分钟):')
            self.config.set('DEFAULT', 'timeout_seconds', str(int(timeout_seconds) * 60000))
        task_reward = self.config.get('DEFAULT', 'task_reward', fallback=None)
        if not task_reward:
            task_reward = raw_input('项目奖励:')
            self.config.set('DEFAULT', 'task_reward', task_reward)
        key = self.config.get('DEFAULT', 'key', fallback=None)
        if not key:
            response = self.api.project_store({
                'project_name': project_name,
                'project_description': project_description,
                'account_name': azure_account_name,
                'account_key': azure_secret,
                'min_lan': min_lan,
                'product_type': project_type,
                'timeout_seconds': timeout_seconds,
                'task_reward': task_reward
            })
            key = response.get('data').get('key')
            self.config.set('DEFAULT', 'key', key)
        with open(config_path, 'w+') as config_file:
            self.config.write(config_file, 'w+')
        client_sse = ClientSSE(import_private_key_response.get('address'))
        # if get_bool("是否上传代码到Azure?[y/n]"):
        #     click.echo('开始上传Code到Azure')
        #     Put(key).put(os.getcwd(), True)
        response = self.eubc_server_api.task_request({
            'timeoutSeconds': timeout_seconds,
            'infoJson': json.dumps({'project_key': key, 'type': project_type}),
            'taskReward': task_reward
        })
        if response.get('status') == 'error':
            click.echo(response.get('message'))
            exit(0)
        elif response.get('status') == 'success':
            click.echo('发布任务成功,等待设备接入')
            task_id = client_sse.return_if_request_is_self()
            project_client = ProjectClient(key, task_id, 10)
            project_client.start()
        else:
            click.echo('发布任务失败')
