from json import dumps

import docker
from ws4py.client.threadedclient import WebSocketClient
from ..config import Config
from click import echo


class ContainerLog(WebSocketClient):

    def __init__(self, pivot, protocols=None, extensions=None, heartbeat_freq=None, ssl_options=None, headers=None,
                 exclude_headers=None):
        config = Config()
        super(ContainerLog, self).__init__(config.get('WS_ADDRESS'), protocols, extensions, heartbeat_freq, ssl_options,
                                           headers,
                                           exclude_headers)
        self.pivot = pivot
        self.client = docker.from_env()

    def opened(self):
        echo('WebSocket opened')
        try:
            if len(self.client.containers.list()) > 0:
                echo('Docker client containers more than 1')
                for container in self.client.containers.list():
                    for line in container.logs(stream=True):
                        self.send(dumps({
                            'type': 'eubh',
                            'project_machine_id': self.pivot.get('id'),
                            'data': line
                        }))
            else:
                echo('Docker client containers less 1')
                self.close()
        except:
            self.close()
            self.connect()
            echo('Web socket is close')
