import json

import sseclient

from ..api import get_eubserver_event

from .sse import SSE


class ClientSSE(SSE):
    def __init__(self, address):
        SSE.__init__(self, address)
        self.client = sseclient.SSEClient(get_eubserver_event())

    def start(self):
        for event in self.client.events():
            event_name = event.event
            data = json.loads(event.data)
            yield event_name, data

    def close(self):
        self.client.close()

    def return_if_request_is_self(self):
        for event_name, data in self.start():
            if event_name == 'request' and data.get('requester') == self.address:
                self.close()
                return data.get('taskId')
