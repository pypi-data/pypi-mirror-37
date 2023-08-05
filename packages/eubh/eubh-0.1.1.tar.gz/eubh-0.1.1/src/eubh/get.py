import os
import tqdm
import click
from azure.storage.file.models import FileProperties, DirectoryProperties
from .utils import init_file_server_by_key, remove_folder, un_zip, un_rar, calc_md5


class Get:
    def __init__(self, key, directory='code'):
        self.key = key
        self.directory = directory
        self.origin_path = None

    def recursive_get_file(self, file_service, directory):
        directories = file_service.list_directories_and_files(self.key, directory)
        for file_directory in directories:
            file_or_directory = "%s/%s/%s" % (self.origin_path, directory, file_directory.name)
            if isinstance(file_directory.properties, FileProperties):
                pbar = tqdm.tqdm(total=100)

                def download_file_progress_callback(current, total):
                    pbar.update(current / total * 100)

                file_service.get_file_to_path(self.key, directory, file_directory.name,
                                              file_or_directory, progress_callback=download_file_progress_callback)
                pbar.close()

            elif isinstance(file_directory.properties, DirectoryProperties):
                if not os.path.exists(file_or_directory):
                    os.mkdir(file_or_directory)
                    click.echo("created directory %s success ." % file_or_directory)
                self.recursive_get_file(file_service, os.path.join(directory, file_directory.name))

    def get(self, to_path, unzip=False):
        self.origin_path = to_path
        code_path = "%s/%s" % (to_path, self.directory)
        if not os.path.exists(code_path):
            os.makedirs(code_path)
        file_service = init_file_server_by_key(self.key)
        self.recursive_get_file(file_service, self.directory)
        if unzip:
            input_path = "%s/input" % to_path
            if file_service.exists(self.key, None, 'input.zip'):
                click.echo('input zip exists , start download input.zip')
                file_service.get_file_to_path(self.key, None, 'input.zip', '%s/input.zip' % self.origin_path)
                click.echo('download input.zip complete, start unzip input.zip')
                remove_folder(input_path)
                un_zip('%s/input.zip' % self.origin_path, input_path)
                click.echo('unzip input.zip complete')
            elif file_service.exists(self.key, None, 'input.rar'):
                click.echo('input rar exists , start download input.rar')
                file_service.get_file_to_path(self.key, None, 'input.rar', '%s/input.rar' % self.origin_path)
                click.echo('download input.rar complete, start unrar input.rar')
                remove_folder(input_path)
                un_rar('%s/input.rar' % self.origin_path, input_path)
                click.echo('unrar input.rar complete')
            else:
                click.echo('The input data was not found')
