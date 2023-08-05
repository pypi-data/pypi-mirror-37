# coding=utf-8
import json
import functools
import urllib
import websocket
import argparse
import tabulate
import requests
from cmd2 import Cmd, with_argparser
from .config import Config

# Format to use with tabulate module when displaying tables
TABLE_FORMAT = 'grid'

# Create a function to format a fixed-width table for pretty-printing using the desired table format
table = functools.partial(tabulate.tabulate, tablefmt=TABLE_FORMAT)


class ProjectClient:
    def __init__(self, key, task_id, need_cal):
        self.need_calc = need_cal
        self.key = key
        self.task_id = task_id
        self.config = Config()

    def start(self):
        project_client_self = self

        def get_task_machines():
            return requests.post(
                url='{0}/project/project/machines'.format(project_client_self.config.get('HTTP_ADDRESS')),
                json={'task_id': project_client_self.task_id},
                headers={'Content-Type': 'application/json'}).json()

        class CmdLineApp(Cmd):
            debug = True
            prompt = 'Eub Cli [>]'
            intro = 'Welcome to Eub Cli !'

            def __init__(self):
                # Set use_ipython to True to enable the "ipy" command which embeds and interactive
                # IPython shell
                Cmd.__init__(self, use_ipython=False)
                del Cmd.do_edit, Cmd.do_alias, Cmd.do_load, Cmd.do_py, \
                    Cmd.do_shell, Cmd.do_unalias, Cmd.do_pyscript, Cmd.do_set, Cmd.do_shortcuts

            azure_parser = argparse.ArgumentParser()
            azure_parser.add_argument('-d', '--download', action='store_true',
                                      help='Download resources to task machine')
            azure_parser.add_argument('id', help='Machine id')

            @with_argparser(azure_parser)
            def do_azure(self, args):
                azure_self = self
                if args.id and args.download:
                    def on_server_message(server_ws, message):
                        info = json.loads(message)
                        if info.get('type') == 'runtime_log':
                            azure_self.poutput(info.get('data'))

                    def on_server_onopen(server_ws):
                        azure_self.poutput('Azure start')

                    def on_server_error(server_ws, err):
                        azure_self.poutput('Server connection error:{0}'.format(err))

                    def on_server_close(server_ws):
                        azure_self.poutput('Server connection close')

                    server_ws = websocket.WebSocketApp(
                        '{0}?type=azure_download&task_id={1}&unique_id={2}&key='.format(
                            project_client_self.config.get('WS_ADDRESS'), project_client_self.task_id, args.id,
                            project_client_self.key
                        ),
                        on_message=on_server_message,
                        on_error=on_server_error,
                        on_close=on_server_close)
                    try:
                        server_ws.on_open = on_server_onopen
                        server_ws.run_forever()
                    except (KeyboardInterrupt,):
                        server_ws.close()

            logs_parser = argparse.ArgumentParser()
            logs_parser.add_argument('id', help='Machine id')

            @with_argparser(logs_parser)
            def do_logs(self, args):
                logs_self = self
                if args.id:
                    def on_server_message(server_ws, message):
                        info = json.loads(message)
                        if info.get('type') == 'runtime_log':
                            logs_self.poutput(info.get('data'))

                    def on_server_onopen(server_ws):
                        logs_self.poutput('Logs start')

                    def on_server_error(server_ws, err):
                        logs_self.poutput('Server connection error:{0}'.format(err))

                    def on_server_close(server_ws):
                        logs_self.poutput('Server connection close')

                    server_ws = websocket.WebSocketApp(
                        '{0}?type=logs&task_id={1}&unique_id={2}'.format(
                            project_client_self.config.get('WS_ADDRESS'),
                            project_client_self.task_id,
                            args.id
                        ),
                        on_message=on_server_message,
                        on_error=on_server_error,
                        on_close=on_server_close)
                    try:
                        server_ws.on_open = on_server_onopen
                        server_ws.run_forever()
                    except (KeyboardInterrupt,):
                        server_ws.close()

            run_parser = argparse.ArgumentParser()
            run_parser.add_argument('id', type=str, help='Machine id')
            run_parser.add_argument('cmd', type=str, help='Run command line')

            @with_argparser(run_parser)
            def do_run(self, args):
                run_self = self

                def on_server_message(server_ws, message):
                    info = json.loads(message)
                    if info.get('type') == 'runtime_log':
                        run_self.poutput(info.get('data'))

                def on_server_onopen(server_ws):
                    run_self.poutput('Task start')

                def on_server_error(server_ws, err):
                    run_self.poutput('Server connection error:{0}'.format(err))

                def on_server_close(server_ws):
                    run_self.poutput('Server connection close')

                request_parameters = {
                    'type': 'run',
                    'task_id': project_client_self.task_id,
                    'unique_id': args.id,
                    'image': 'tensorflow/tensorflow:1.7.0-gpu',
                    'cmd': args.cmd
                }
                server_ws = websocket.WebSocketApp(
                    '{0}?{1}'.format(project_client_self.config.get('WS_ADDRESS'),
                                     urllib.urlencode(request_parameters)),
                    on_message=on_server_message,
                    on_error=on_server_error,
                    on_close=on_server_close)
                try:
                    server_ws.on_open = on_server_onopen
                    server_ws.run_forever()
                except (KeyboardInterrupt,):
                    server_ws.close()

            machine_parser = argparse.ArgumentParser()

            @with_argparser(machine_parser)
            def do_machine(self, args):
                """Repeats what you tell me to."""
                machines = get_task_machines()
                data = machines.get('data')
                table_header = ['Id', 'HostName', 'PublicIp', 'IpAddress', 'Gpu', 'benchmark']
                table_data = []
                for machine in data:
                    gpu_str = ''
                    for card in machine.get('gpu'):
                        gpu_str += '{0}({1})\r\n'.format(card.get('Name'), card.get('Memory'))
                    table_data.append([
                        machine.get('unique_id'),
                        machine.get('host_name'),
                        machine.get('public_ip'),
                        machine.get('ip_address'),
                        gpu_str,
                        machine.get('benchmark')
                    ])
                self.ptable(table_data, table_header)

            def ptable(self, tabular_data, headers=()):
                """Format tabular data for pretty-printing as a fixed-width table and then display it using a pager.

                :param tabular_data: required argument - can be a list-of-lists (or another iterable of iterables), a list of
                                     named tuples, a dictionary of iterables, an iterable of dictionaries, a two-dimensional
                                     NumPy array, NumPy record array, or a Pandas dataframe.
                :param headers: (optional) - to print nice column headers, supply this argument:
                                - headers can be an explicit list of column headers
                                - if `headers="firstrow"`, then the first row of data is used
                                - if `headers="keys"`, then dictionary keys or column indices are used
                                - Otherwise, a headerless table is produced
                """
                formatted_table = table(tabular_data, headers=headers)
                self.ppaged(formatted_table)

            def do_quit(self, _):
                """Exits this application."""
                ws.close()
                self._should_quit = True
                return self._STOP_AND_EXIT

        def on_message(ws, message):
            info = json.loads(message)
            if info.get('type') == 'device_login':
                print 'New device Login in'
                print 'Current Device Benchmark:'
                current_register = info.get('currentRegister')
                total_benchmark = 0
                for register in current_register:
                    data = register.get('data')
                    if data:
                        print '{0} ({1})'.format(data.get('unique_id'), data.get('benchmark'))

                        total_benchmark += data.get('benchmark')
                        if total_benchmark >= self.need_calc:
                            c = CmdLineApp()
                            c.cmdloop()

            elif info.get('type') == 'runtime_log':
                print info.get('data')

        def on_error(ws, error):
            print 2, error

        def on_close(ws):
            print 3

        def on_open(ws):
            print 'Connection server success'

        ws = websocket.WebSocketApp('{0}?type=task_requester&task_id={1}'.format(project_client_self.config.get(
            'WS_ADDRESS'), project_client_self.task_id),
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
