'''CLI extension for the ``gupload`` command.'''

import os
from pathlib import Path
import webbrowser

from cliar import Cliar, set_arg_map, set_metavars, set_help
from foliant.cli.base import BaseCli
from foliant.cli import make
from foliant.utils import spinner

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Cli(BaseCli):
    # @set_arg_map({'project_path': 'path', 'config_file_name': 'config'})
    @set_metavars({'filetype': 'FILETYPE'})
    # @set_help(
    #     {
    #         'filetype': 'filetype: docx, pdf, etc.',
    #         'config_file_name': 'Name of config file of the Foliant project',
    #         'debug': 'Log all events during build. If not set, only warnings and errors are logged'
    #     }
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _gdrive_auth(self):
        if not self._gdoc_config['com_line_auth']:
            self._gdoc_config['com_line_auth'] = False

        gauth = GoogleAuth()

        if self._gdoc_config['com_line_auth']:
            gauth.CommandLineAuth()
            self._gdrive = GoogleDrive(gauth)
        else:
            if True:  # 'False' while debugging to reduce amount of new tabs
                gauth.LocalWebserverAuth()
                self._gdrive = GoogleDrive(gauth)
            else:
                gauth.LoadCredentialsFile('client_creds.txt')

                if gauth.credentials is None:
                    gauth.LocalWebserverAuth()
                elif gauth.access_token_expired:
                    gauth.Refresh()
                else:
                    gauth.Authorize()

                gauth.SaveCredentialsFile('client_creds.txt')
                self._gdrive = GoogleDrive(gauth)

    def _create_gdrive_folder(self):

        if not self._gdoc_config['gdrive_folder_id']:
            folder = self._gdrive.CreateFile({'title': 'Foliant upload', 'mimeType': 'application/vnd.google-apps.folder'})
            folder.Upload()
            self._gdoc_config['gdrive_folder_id'] = folder['id']

    def _upload_file(self, filetype):
        if self._gdoc_config['gdoc_title']:
            title = self._gdoc_config['gdoc_title']
        else:
            title = self._filename

        if filetype == 'docx':
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif filetype == 'pdf':
            mimetype = 'application/pdf'
        elif filetype == 'tex':
            mimetype = 'application/x-latex'
        else:
            mimetype = 'application/vnd.google-apps.document'

        if self._gdoc_config['gdoc_id']:
            upload_file = self._gdrive.CreateFile({'title': title, 'id': self._gdoc_config['gdoc_id'], 'parents': [{'id': self._gdoc_config['gdrive_folder_id']}], 'mimeType': mimetype})
        else:
            upload_file = self._gdrive.CreateFile({'title': title, 'parents': [{'id': self._gdoc_config['gdrive_folder_id']}], 'mimeType': mimetype})

        if self._gdoc_config['convert_file']:
            convert = self._gdoc_config['convert_file']
        else:
            convert = False

        upload_file.SetContentFile('/'.join((os.getcwd(), f'{self._filename}')))
        upload_file.Upload(param={'convert': convert})

        self._gdoc_config['gdoc_id'] = upload_file['id']
        self._gdoc_link = upload_file['alternateLink']

        webbrowser.open(self._gdoc_link)

    def gupload(self, filetype):

        file_upload = make.Cli()
        self._filename = file_upload.make(filetype)

        print('─────────────────────')

        self._gdoc_config = file_upload.get_config(Path('.'), 'foliant.yml')['gupload']

        if self._filename:

            self._gdrive_auth()

            with spinner(f"Uploading '{self._filename}' to Google Drive", self.logger, quiet=False):
                try:
                    self._create_gdrive_folder()
                    self._upload_file(filetype)

                except Exception as exception:
                    raise type(exception)(f'The error occurs: {exception}')

        print('─────────────────────')
        print(f"Result:\n\
Doc link: {self._gdoc_link}\n\
Google drive folder ID: {self._gdoc_config['gdrive_folder_id']}\n\
Google document ID: {self._gdoc_config['gdoc_id']}")

        return self._gdoc_link
