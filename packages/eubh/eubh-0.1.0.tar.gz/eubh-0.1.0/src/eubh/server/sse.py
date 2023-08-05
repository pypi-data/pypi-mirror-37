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
from ..utils import get_host_ip, get_public_ip
from ..api import get_eubserver_event
from ..eubc_server_api import EubcServerApi
from ..config import Config
from ..get import Get
from ..put import Put
from click import echo
from multiprocessing import Process

do_acceptor_event_process = []


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

    def send_runtime_log(messages):
        ws.send(json.dumps({
            'type': 'runtime_log',
            'data': messages,
            'task_id': data.get('id'),
            'unique_id': unique_id
        }))

    def do_running():
        print 'Image:{0},Cmd:{1}'.format(info.get('image'), info.get('cmd'))
        key = info.get('key')
        if info.get('pull_code') and info.get('key') == 'true':
            print 'Start pull code'
            Get(info.get('key')).get('/root', True)
            print 'Pull code success'
        docker_client = clean_docker()

        container = docker_client.containers.run(
            info.get('image'),
            info.get('cmd'),
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

        Put(key, 'result').put('/root/result', True)

    def clean_running_process():
        """Terminate old run process"""
        for item in do_acceptor_event_process:
            if item.get('name') == 'run' and isinstance(item.get('process'), Process):
                item.get('process').terminate()

    info = json.loads(message)
    if info.get('type') == 'runtime_log':
        print info.get('data')
    elif info.get('type') == 'stop':
        send_runtime_log('Start stop containers')
        clean_running_process()
        clean_docker()
        send_runtime_log('Stop containers success')
    elif info.get('type') == 'run':
        clean_running_process()
        """Start running process"""
        p = Process(target=do_running, )
        do_acceptor_event_process.append({
            'name': 'run',
            'process': p
        })
        p.start()
    elif info.get('type') == 'upload-result':
        send_runtime_log('Start upload result')
        key = info.get('key')
        Put(key, 'result').put('/root/result', True)
        send_runtime_log('Upload result success')


class SSE:
    def __init__(self, address):
        self.address = address
        self.eubc_server_api = EubcServerApi()
        self.config = Config()

    def start(self):
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
                            echo('TensorFlow taskId:{0}'.format(data.get('id')))
                            task_accept_response = self.eubc_server_api.task_accept(data.get('id'))
                            if task_accept_response.get('status') == 'error':
                                echo('Accept taskId:{0} request fail'.format(task_accept_response.get('message')))
                            elif task_accept_response.get('status') == 'success':
                                echo('Accept taskId:{0} request success'.format(data.get('id')))

                    elif event_name == 'accept':
                        if data.get('acceptor') == self.address:
                            can_receive_task = False
                            current_task_id = data.get('id')

                            def do_acceptor_event():
                                timout_seconds = int(data.get('timeoutSeconds'))
                                echo('Receive the task successfully and begin execution, taskId:{0}'.format(
                                    current_task_id))

                                def on_message(ws, message):
                                    on_acceptor_message(ws, message, data)

                                    # elif info.get('type') == 'azure_download':
                                    #     send_runtime_log('Start download azure resources')
                                    #     send_runtime_log('Download azure complete')

                                def on_error(ws, error):
                                    print 2, error

                                def on_close(ws):
                                    print 3

                                def on_open(ws):
                                    gpus = []
                                    global unique_id
                                    if 'ubuntu' in platform.platform().lower():
                                        from subprocess import call
                                        # unique_id = call("dmidecode -t 4 | grep ID | sed 's/.*ID://;s/ //g'")
                                        # print unique_id
                                        unique_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                                        print unique_id
                                        from gpuinfo.nvidia import get_gpus
                                        try:
                                            for gpu in get_gpus():
                                                gpus.append({
                                                    "Name": gpu.name,
                                                    "Memory": '{0} GB'.format(round(gpu.total_memory / 1024, 1) + 1)
                                                })
                                        except:
                                            gpus = []
                                    else:
                                        unique_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                                    ws.send(json.dumps({
                                        'type': 'register',
                                        'device_info': {
                                            "hostname": socket.gethostname(),
                                            "ip_address": get_host_ip(),
                                            "gpu": gpus,
                                            "public_ip": get_public_ip(),
                                            'unique_id': unique_id,
                                            'benchmark': 10
                                        },
                                        'task_id': data.get('id')
                                    }))

                                ws = websocket.WebSocketApp(self.config.get('WS_ADDRESS'),
                                                            on_message=on_message,
                                                            on_error=on_error,
                                                            on_close=on_close)
                                ws.on_open = on_open

                                ws_threading = threading.Thread(target=ws.run_forever)
                                ws_threading.start()

                                sleep(timout_seconds)
                                ws.close()
                                can_receive_task = True

                            p = Process(target=do_acceptor_event, )
                            do_acceptor_event_process.append({
                                'name': 'accept',
                                'process': p
                            })
                            p.start()

                if event_name == 'cancel':
                    if not lock_can_task and data.get('id') == current_task_id:
                        lock_can_task = True
                        print 'Task cancel', data
                        """Terminate all process"""
                        for item in do_acceptor_event_process:
                            if isinstance(item.get('process'), Process):
                                item.get('process').terminate()
                        """Clean docker"""
                        clean_docker()
                        """Put result to azure"""
                        Put(info_json.get('project_key'), 'result').put('/root/result', True)
                        lock_can_task = False
                        can_receive_task = True
