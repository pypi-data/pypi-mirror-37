# -*- coding: utf8 -*-
import os

try:
    # noinspection PyPep8Naming
    import ConfigParser as configparser
except ImportError:
    # noinspection PyUnresolvedReferences
    import configparser


class AzureConfig(object):
    _AZURE_DIRECTORY = '.azure'

    def __init__(self):
        self._parser = None

    @classmethod
    def get_config_path(cls):
        if os.name == 'nt':
            return os.path.join(os.environ['USERPROFILE'], cls._AZURE_DIRECTORY)

        return os.path.join(os.path.expanduser('~'), cls._AZURE_DIRECTORY)

    @classmethod
    def get_default_config_path(cls):
        return os.path.join(cls.get_config_path(), 'config')

    @property
    def storage_account(self):
        return self._read_config('storage', 'account')

    @property
    def storage_key(self):
        return self._read_config('storage', 'key')

    def _create_parser_if_needed(self):
        if self._parser is not None:
            return

        default_config = self.get_default_config_path()
        parser = configparser.ConfigParser()
        parser.read(default_config)

        self._parser = parser

    def _read_config(self, section, name):
        self._create_parser_if_needed()

        env_var_name = 'AZURE_{section}_{name}'.format(section=section, name=name)

        value = os.environ.get(env_var_name.upper())

        if value is not None:
            return value

        try:
            return self._parser.get(section, name)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return None
