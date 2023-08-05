from os import system

from eubh import *
import click

_global_options = [
    click.option('--verbose', '-v', 'verbosity', flag_value=2, default=1, help='Enable verbose output'),
]


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


@click.group()
def config_group():
    pass


@config_group.command()
@click.argument('key', required=True)
@click.argument('value', required=False)
def config(key, value):
    current_config = Config()
    if value:
        current_config.set(key, value)
    else:
        echo(current_config.get(key))


@click.group()
def get_group():
    pass


@get_group.command()
@click.argument('key', required=True)
@click.argument('path', required=True)
@click.option('--code/--no-code', default=True, help='Get code source')
@click.option('--result/--no-result', default=True, help='Get result')
@click.option('--unzip/--no-unzip', default=False, help='Unzip input')
def get(key, path, code, result, unzip):
    if code:
        Get(key).get(path, unzip)
    if result:
        Get(key, 'result').get(path, unzip)


@click.group()
def put_group():
    pass


@put_group.command()
@click.argument('key', required=True)
@click.argument('path', required=True)
@click.option('--folder/--no-folder', default=True, help='Upload directory')
@click.option('--code/--no-code', default=False, help='Upload code')
@click.option('--result/--no-result', default=False, help='Put result')
def put(key, path, folder, code, result):
    if code:
        Put(key).put(path, folder)
    if result:
        Put(key, 'result').put(path, folder)


@click.group()
def watch_group():
    pass


@watch_group.command()
@global_options
@click.option('-k', '--key')
@click.option('-t', '--time', default=10, help='Loop time (s)')
@click.option('-v', '--verbosity', default=True, help='Verbose mode')
def watch(key, time, verbosity):
    Watch(key, time, verbosity).watch()


@click.group()
def init_group():
    pass


@init_group.command()
def init():
    from eubh.init import init as project_init
    project_init()


@click.group()
def upgrade_group():
    pass


@upgrade_group.command()
def upgrade():
    system('pip install --upgrade eubh --no-cache-dir')


@click.group()
def user_group():
    pass


@user_group.command()
def login():
    from eubh.user import login as user_login
    user_login()


@user_group.command()
@click.argument('private_key', required=True)
def import_private_key(private_key):
    from eubh.user import import_private_key
    import_private_key(private_key)


@click.group()
def version_group():
    pass


@version_group.command()
def version():
    echo(VERSION)


@click.group()
def container_group():
    pass


cli = click.CommandCollection(
    sources=[
        get_group,
        put_group,
        watch_group,
        init_group,
        upgrade_group,
        version_group,
        config_group,
        user_group
    ])


def main():
    cli()


if __name__ == "__main__":
    cli()
