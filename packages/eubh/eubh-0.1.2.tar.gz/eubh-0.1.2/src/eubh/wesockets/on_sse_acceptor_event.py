import json

import websocket
from ..config import Config


class OnSseAcceptorEvent:
    def __init__(self, acceptor_event_all_data, on_acceptor_message=None):
        self.acceptor_event_all_data = acceptor_event_all_data
        self.task_id = acceptor_event_all_data.get('current_task_id')
        self.device_info = acceptor_event_all_data.get('device_info')
        self.unique_id = self.device_info.get('unique_id')
        self.config = Config()
        self.on_acceptor_message = on_acceptor_message

    def start(self):
        def on_message(ws, message):
            if self.on_acceptor_message:
                self.on_acceptor_message(ws, message, self.acceptor_event_all_data)

        def on_error(ws, error):
            print 2, error

        def on_close(ws):
            print 3

        def on_open(ws):
            ws.send(json.dumps({
                'type': 'register',
                'device_info': self.device_info,
                'task_id': self.task_id
            }))
            print 'Register device success'

        ws_on_sse_acceptor_event = websocket.WebSocketApp(self.config.get('WS_ADDRESS'),
                                                          on_message=on_message,
                                                          on_error=on_error,
                                                          on_close=on_close)
        ws_on_sse_acceptor_event.on_open = on_open
        ws_on_sse_acceptor_event.run_forever()
