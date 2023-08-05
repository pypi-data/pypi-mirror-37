# coding=utf-8
import json
import os
import random
import socket
import string
import zipfile
from ConfigParser import NoOptionError
from json import load
from netifaces import interfaces, ifaddresses, AF_INET
from urllib2 import urlopen
import click
import rarfile
from azure.storage.file import FileService
import hashlib
import multiprocessing
import os
import sys
import psutil
import logging
from .api import Api
from wget import download
from zipfile import ZipFile
from os import path, makedirs, popen
from .config import ROOT_DIR, Config
from .eubc_server_api import EubcServerApi


def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception, e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)


def check_api_secret_is_correct():
    config = Config()
    if not config.get('api_secret'):
        click.echo('Please login before run this command')
        exit(0)
    return True


def un_zip(filename, to_path):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(filename)
    if os.path.exists(to_path):
        os.remove(to_path)
    else:
        os.makedirs(to_path)
    zip_file.extractall(to_path)
    zip_file.close()


def get_project_key_by_task_id(task_id):
    eubc_server_api = EubcServerApi()
    task_info = eubc_server_api.task_info(task_id)
    if task_info.get('status') == 'success':
        data = task_info.get('data')
        info_json = json.loads(data.get('infoJson'))
        return info_json.get('project_key')
    return None


def un_rar(file_name, to_path):
    """unrar rar file"""
    rar = rarfile.RarFile(file_name)
    if os.path.exists(to_path):
        os.remove(file_name)
    else:
        os.makedirs(to_path)
    rar.extractall(to_path)
    rar.close()


def init_environment():
    """init ubuntu nvidia docker environment"""
    os.system('curl https://public-packages.oss-cn-beijing.aliyuncs.com/install_nvidia_docker.sh|sh -')


def init_file_server_by_key(key):
    config = Api(key=key).get_config_by_key().get('data')

    file_service = FileService(account_name=config.get('account_name'),
                               account_key=config.get('account_key'),
                               endpoint_suffix=config.get('endpoint_suffix'))

    # logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)
    # logger = logging.getLogger('azure.storage')
    # handler = logging.StreamHandler()
    # formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-5s %(message)s')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel(logging.INFO)

    return file_service


def get_folder_name_from_path(path):
    return os.path.basename(path)


def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        for link in ifaddresses(interface).get(AF_INET, ()):
            ip_list.append(link['addr'])
    return ip_list


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_public_ip():
    return load(urlopen('http://jsonip.com'))['ip']


def is_empty(key):
    return key == '' or key is None


def get_device_info():
    import platform

    unique_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    gpus = []
    if 'ubuntu' in platform.platform().lower():
        from gpuinfo.nvidia import get_gpus
        try:
            for gpu in get_gpus():
                gpus.append({
                    "Name": gpu.name,
                    "Memory": '{0} GB'.format(round(gpu.total_memory / 1024, 1) + 1)
                })
        except:
            click.echo("get gpu information error ")
    return {
        "hostname": socket.gethostname(),
        "ip_address": get_host_ip(),
        "gpu": gpus,
        "public_ip": get_public_ip(),
        'unique_id': unique_id,
        'benchmark': 10
    }


def get_bool(prompt):
    while True:
        try:
            return {"true": 'y', "false": 'n'}[input(prompt).lower()]
        except KeyError:
            print "Invalid input please enter True or False!"


def remove_folder(folder):
    os.popen('rm -rf %s' % folder)


def calc_md5(file_path):
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


def download_file(url, to_path, md5=None):
    if os.path.exists(to_path):
        os.unlink(to_path)
    download(url, to_path)
    if md5:
        file_md5 = calc_md5(to_path)
        click.echo('\r\nDownload file md5:{0},Remote file md5:{1}'.format(file_md5, md5))
        if md5 != calc_md5(to_path):
            download_file(url, to_path, md5)


def unzip_file(zip_path, to_path):
    z = ZipFile(zip_path, 'r')
    z.extractall(path=to_path)
    z.close()


def get_ifn_exit(key):
    value = None
    config = Config()
    try:
        value = config.get(key)
    except NoOptionError:
        click.echo('未设置 {0}'.format(key))
    if not value:
        click.echo('未设置 {0}'.format(key))
        exit(0)
    return value


def download_and_run_eubchain_eubserver():
    api = Api()
    data = api.get_eubchain()
    save_path = '{0}/.eub'.format(ROOT_DIR)
    jobs = []
    if not path.exists(save_path):
        makedirs(save_path)
    for item in data:
        download_file_name = '{0}/{1}.zip'.format(save_path, item.get('folder'))
        out_put_folder = '{0}/{1}'.format(save_path, item.get('folder'))

        def t(is_download=True):
            if is_download:
                download_file(item.get('url'), download_file_name, item.get('md5'))
            unzip_file(download_file_name, out_put_folder)
            popen('chmod +x {0}/{1}'.format(out_put_folder, item.get('name')))
            if item.get('name') in 'geth':
                background_process = multiprocessing.Process(target=popen,
                                                             args=(
                                                                 '{0}/{1} --identity "eub-light-client" '
                                                                 '--datadir "{0}/eth" --verbosity 0'.format(
                                                                     out_put_folder, item.get('name')),))
                background_process.start()
                jobs.append(background_process)
            elif item.get('name') in 'eubserver':
                background_process = multiprocessing.Process(target=popen,
                                                             args=('{0}/{1} > /dev/null'.format(out_put_folder,
                                                                                                item.get('name')),))
                background_process.start()
                jobs.append(background_process)

        if not path.exists(out_put_folder):
            makedirs(out_put_folder)
        if not path.exists(download_file_name):
            t()
        else:
            if calc_md5(download_file_name) != item.get('md5'):
                t()
            else:
                t(False)
    return jobs
