import multiprocessing
import platform
import random
import string
from uuid import getnode as get_mac

import json
import tqdm
import docker
import sseclient
import websocket
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from click import echo
from time import sleep

from websocket._exceptions import WebSocketException

from .server import SSE
from .get import *
from .put import *
from .status import *
from .utils import *
from .config import ROOT_DIR, DOCKER_WHITE_LIST, Config
from .logs.container_log import ContainerLog as WriteContainerLog
from .wesockets.container_log import ContainerLog as PushContainerLog
from multiprocessing import Process
from .api import get_chain_sync_progress, get_eubserver_event
from .eubc_server_api import EubcServerApi


def clean_file():
    echo('Remove %s/code and %s/result' % (ROOT_DIR, ROOT_DIR))
    os.popen('rm -rf %s/code %s/result' % (ROOT_DIR, ROOT_DIR))
    echo('Remove files successful')


def create_directories():
    os.makedirs('%s/code' % ROOT_DIR)
    os.makedirs('%s/result' % ROOT_DIR)


def job_write_log(data, verbosity):
    WriteContainerLog(pivot=data, verbosity=verbosity)


def job_real_time_push_log(data, reply=10):
    push_container_log = PushContainerLog(data)
    is_success = False

    while reply > 1 and not is_success:
        try:
            push_container_log.connect()
            is_success = True
        except WebSocketException or KeyboardInterrupt:
            push_container_log.close()
            push_container_log = False
            reply -= 1
            echo('WebSocket connect reply %d' % reply)
    if not is_success:
        echo('WebSocket connect fail')


class Watch:
    def __init__(self, key, time, verbosity):
        config = Config()
        self.config = config
        self.time = time
        self.key = key
        self.api = Api()
        self.host = config.get('HOST_ADDRESS')
        self.webscoket = config.get('WS_ADDRESS')
        echo('Api server:{0} ,Webscoket:{1}'.format(config.get('HTTP_ADDRESS'), config.get('WS_ADDRESS')))
        self.docker_client = docker.from_env()
        self.can_init = True
        self.cache_log = []
        self.jobs = []
        self.is_verbose = True if verbosity else False
        self.eubc_server_api = EubcServerApi()

    def clean_docker(self):
        client = self.docker_client
        for container in client.containers.list():
            if container.attrs['Name'] not in DOCKER_WHITE_LIST:
                container.stop()

    def run_cmd_and_upload_result(self, pivot):
        cmd = pivot.get('cmd')
        if not is_empty(cmd):
            cmd_result_out_put = os.popen(cmd)
            cmd_result_out_put_string = cmd_result_out_put.read()
            self.api.project_machine_update_cmd({"id": pivot.get('id'), "result": cmd_result_out_put_string})
            cmd_result_out_put.close()

    def upload_machine_information(self):
        client = self.docker_client
        current_status = Status.IDLE.value

        client_containers_count = len(client.containers.list())
        if client_containers_count == 0:
            if not is_empty(self.key):
                current_status = Status.COMPLETE.value
        else:
            current_status = Status.IDLE.value

        if client_containers_count > 0:
            if is_empty(self.key):
                self.clean_docker()
            current_status = Status.RUNNING.value

        data = get_device_info()
        data['status_info'] = {
            'key': self.key,
            'status': current_status
        }
        data['mac'] = "machine_%s" % get_mac()
        response = self.api.upload_machine_and_get_task(data)

        if type(response) is not list:
            option = response.get('option')
            project = response.get('project')
            pivot = response.get('pivot')

            key = None
            if project is not None:
                key = project.get('key')

            if not is_empty(key):
                if option == 'init' and self.can_init:
                    self.can_init = False
                    self.clean_current_jobs()
                    clean_file()
                    create_directories()
                    echo('Pull code')
                    Get(key).get(ROOT_DIR, True)
                    echo('Pull code success')
                    self.key = key
                    echo('Creating container.')
                    self.run_cmd_and_upload_result(pivot)
                    echo('Created container.')

                    echo('Creating write log job')
                    write_log = multiprocessing.Process(target=job_write_log,
                                                        args=(pivot, self.is_verbose))
                    write_log.start()
                    echo('Creating real time log')
                    push_log = multiprocessing.Process(target=job_real_time_push_log,
                                                       args=(pivot,))
                    push_log.start()
                    echo('Created real time log')
                    self.jobs.append(write_log)
                    self.jobs.append(push_log)

                elif option == 'cmd':
                    self.run_cmd_and_upload_result(pivot)

            if option == 'clean':
                echo('Cleaning docker')
                self.clean_docker()
                echo('Cleaned docker')
                echo('Cleaning jobs')
                self.clean_current_jobs()
                echo('Cleaned jobs')
                if not is_empty(self.key):
                    echo('Pushing result')
                    Put(self.key, 'result').put('%s/result' % ROOT_DIR, True)
                    echo('Pushed result')
                    self.key = ''
                    self.can_init = True

    def log_is_exist(self, container_id, log):
        cache_logs = self.cache_log
        is_exist_log = False
        for i in cache_logs:
            if cache_logs[i].container_id == container_id and cache_logs[i].log == log:
                is_exist_log = True
                break
        if not is_exist_log:
            self.cache_log.append({
                container_id: container_id,
                log: log
            })
        return is_exist_log

    def watch_upload_docker_log(self):
        client = self.docker_client

        for container in client.containers.list():
            log = container.logs()

            self.api.post_project_container_logs({
                'container_id': container.attrs['Id'],
                'log': log
            })

    def clean_current_jobs(self):
        if len(self.jobs) > 0:
            for job in self.jobs:
                job.terminate()

    def watch(self):
        """start geth ,eubserver in background"""
        # jobs = []
        # try:
        #     jobs = download_and_run_eubchain_eubserver()
        # except (KeyboardInterrupt, SystemExit):
        #     for job in jobs:
        #         if isinstance(job, Process):
        #             job.terminate()
        # sync_is_done = 0
        # with tqdm.tqdm(total=100) as pbar:
        #     temp_position = 0
        #     while sync_is_done <= 5:
        #         try:
        #             sync_progress_data = get_chain_sync_progress()
        #             current_sync_progress = sync_progress_data.get('data')
        #             if current_sync_progress == 100:
        #                 sync_is_done += 1
        #             else:
        #                 pbar.update(current_sync_progress - temp_position)
        #                 temp_position = current_sync_progress
        #         except Exception:
        #             echo('Connection eubserver fail, Reply')
        #         sleep(3)
        echo('Sync Done,wait task')
        echo('Start import privateKey')
        import_private_key_response = self.eubc_server_api.import_private_key()
        echo('Import privateKey success')

        echo('Start sse')
        sse = SSE(import_private_key_response.get('address'))

        sse_thread = threading.Thread(target=sse.start())
        sse_thread.start()
        sse_thread.join()

    # while True:
    #     self.upload_machine_information()
    #     sleep(self.time)
    # scheduler = BlockingScheduler()
    # scheduler.add_job(self.upload_machine_information, 'interval', seconds=self.time, max_instances=1)
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
