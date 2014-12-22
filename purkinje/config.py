# -*- coding: utf-8 -*-


""" Reading and validation of configuration file
"""
from builtins import object, basestring

import yaml
import logging
from voluptuous import Schema  # pylint: disable-msg=W0622
import voluptuous as v

logger = logging.getLogger(__name__)


class ConfigException(Exception):

    """ Raised for configuration-related problems (parsing, consistency)
    """

    def __init__(self, message):
        Exception.__init__(self, message)


class Config(object):

    """ Application configuration (singleton class)
    """
    _instance = None  # singleton instance

    def __init__(self, config_file_name):
        self._config_file_name = config_file_name
        logger.debug(
            'Initializing configuration from file %s',
            self._config_file_name)

        port_spec = v.All(int, v.Range(min=1, max=65535))

        self._validation_schema = Schema({
            'global': {
                v.Required('project-path'): basestring,
                'server-port': port_spec,
                v.Optional('log-level'): basestring
            }
        })

        with open(config_file_name, 'r') as conf_file:
            self._conf = yaml.load(conf_file)
        self._validate(self._conf)

    def _validate(self, conf):
        """ Structural and semantic validation of configuration file contents
        """
        try:
            self._validation_schema(conf)
        except v.Error as error:
            error_message = ('Error in configuration file format: %s',
                             str(error))
            logger.exception(error)
            raise ConfigException(error_message)

    def settings(self):
        """
        :return: raw configuration (as created by *pyaml*)
        """
        return self._conf

    @staticmethod
    def get():
        """ Singleton getter. The configuration must have been initialized
            before calling this method by calling `Config.create`
        """
        if Config._instance is None:
            raise ConfigException("Configuration not initialized")
        return Config._instance

    @staticmethod
    def create(config_file_name):
        """ Initializes singleton instance
        """
        Config._instance = Config(config_file_name)
        return Config._instance