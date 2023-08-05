import platform
import random
import socket
import string
import threading
from time import sleep

import websocket
import sseclient
import json
import docker
from ..utils import get_host_ip, get_public_ip, get_device_info, get_project_key_by_task_id
from ..api import get_eubserver_event
from ..eubc_server_api import EubcServerApi
from ..config import Config
from ..get import Get
from ..put import Put
from ..wesockets import OnSseAcceptorEvent
from click import echo
from multiprocessing import Process

do_acceptor_event_process = []


def clean_running_process():
    """Terminate old run process"""
    terminate_running_process_by_name('run')


def terminate_all_process():
    for item in do_acceptor_event_process:
        if isinstance(item.get('process'), Process):
            item.get('process').terminate()


def terminate_running_process_by_name(name):
    for item in do_acceptor_event_process:
        if item.get('name') == name and isinstance(item.get('process'), Process):
            item.get('process').terminate()


def clean_docker():
    print 'Start stop containers'
    docker_client = docker.from_env()
    containers = docker_client.containers.list()
    for container in containers:
        container.stop()
    print 'Stop containers'
    return docker_client


def on_acceptor_message(ws, message, data):
    """Send Runtime logs"""
    device_info = data.get('device_info')
    unique_id = device_info.get('unique_id')
    task_id = data.get('current_task_id')

    def send_runtime_log(messages):
        ws.send(json.dumps({
            'type': 'runtime_log',
            'data': messages,
            'task_id': task_id,
            'unique_id': unique_id
        }))

    def do_running(info_json):
        print 'Image:{0},Cmd:{1}'.format(info_json.get('image'), info_json.get('cmd'))
        if info_json.get('pull_code') and info_json.get('key') == 'true':
            print 'Start pull code'
            Get(info_json.get('key')).get('/root', True)
            print 'Pull code success'
        docker_client = clean_docker()

        container = docker_client.containers.run(
            info_json.get('image'),
            info_json.get('cmd'),
            detach=True,
            auto_remove=True,
            runtime='nvidia',
            volumes={
                '/root': {'bind': '/notebooks', 'mode': 'rw'}
            }
        )
        container_id = container.attrs['Id']

        print 'Current container Id:{0}'.format(container_id)
        send_runtime_log(container_id)

        print 'Start transfer logs stream'
        for line in container.logs(stream=True):
            send_runtime_log(line.strip())

        Put(info_json.get('key'), 'result').put('/root/result', True)

    info = json.loads(message)
    if info.get('type') == 'runtime_log':
        print info.get('data')
    elif info.get('type') == 'stop':
        send_runtime_log('Start stop containers')
        terminate_all_process()
        clean_docker()
        send_runtime_log('Stop containers success')
    elif info.get('type') == 'run':
        clean_running_process()
        """Start running process"""
        p = Process(target=do_running, args=(info,), )
        do_acceptor_event_process.append({
            'name': 'run',
            'process': p
        })
        p.start()
    elif info.get('type') == 'upload-result':
        def upload_result():
            send_runtime_log('Start upload result')
            import os
            project_key = get_project_key_by_task_id(task_id=task_id)
            if os.path.exists('/root/result') and project_key:
                Put(project_key, 'result').put('/root/result', True)
            send_runtime_log('Upload result success')

        terminate_running_process_by_name('upload-result')
        upload_result_process = Process(target=upload_result, )
        do_acceptor_event_process.append({
            'name': 'upload-result',
            'process': upload_result_process
        })
        upload_result_process.start()


def do_acceptor_event(acceptor_event_all_data):
    on_sse_acceptor_event = OnSseAcceptorEvent(acceptor_event_all_data=acceptor_event_all_data,
                                               on_acceptor_message=on_acceptor_message)
    on_sse_acceptor_event.start()


class SSE:
    def __init__(self, address):
        self.address = address
        self.eubc_server_api = EubcServerApi()
        self.config = Config()

    def acceptor_task(self, data):
        echo('TensorFlow taskId:{0}'.format(data.get('id')))
        task_accept_response = self.eubc_server_api.task_accept(data.get('id'))
        if task_accept_response.get('status') == 'error':
            echo('Accept taskId:{0} request fail'.format(task_accept_response.get('message')))
        elif task_accept_response.get('status') == 'success':
            echo('Accept taskId:{0} request success'.format(data.get('id')))

    def start(self):
        try:
            can_receive_task = True
            lock_can_task = False
            client = sseclient.SSEClient(get_eubserver_event())
            current_task_id = None

            for event in client.events():
                event_name = event.event
                data = json.loads(event.data)
                task_info = self.eubc_server_api.task_info(data.get('taskId'))
                echo('Task type:{0},Task id:{1}'.format(event_name, data.get('taskId')))

                if task_info.get('status') == 'success':
                    data = task_info.get('data')
                    info_json = json.loads(data.get('infoJson'))

                    if can_receive_task:
                        if event_name == 'request':
                            if info_json.get('type').lower() == 'eubflow':
                                acceptor_task_process = Process(target=self.acceptor_task, args=(data,))
                                do_acceptor_event_process.append({
                                    'name': 'accept-task',
                                    'process': acceptor_task_process
                                })
                                acceptor_task_process.start()

                        elif event_name == 'accept':

                            if data.get('acceptor') == self.address:
                                can_receive_task = False
                                current_task_id = data.get('id')
                                device_info = get_device_info()

                                all_run_data = {
                                    'data': data,
                                    'device_info': device_info,
                                    'current_task_id': current_task_id
                                }

                                p = Process(target=do_acceptor_event, args=(all_run_data,), )
                                do_acceptor_event_process.append({
                                    'name': 'accept',
                                    'process': p
                                })
                                p.start()

                    if event_name == 'cancel':
                        if not lock_can_task and data.get('id') == current_task_id:
                            lock_can_task = True
                            print 'Task cancel'
                            """Terminate all process"""
                            terminate_all_process()
                            """Clean docker"""
                            clean_docker()
                            """Put result to azure"""
                            Put(info_json.get('project_key'), 'result').put('/root/result', True)
                            lock_can_task = False
                            can_receive_task = True
        except(KeyboardInterrupt, SystemExit):
            terminate_all_process()
