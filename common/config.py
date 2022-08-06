# -*- coding: utf-8 -*-
"""
    Configuration
    author: modorigoon
    since: 0.1.0
"""
import json
import os
import sys
import getopt

__env__ = None
__CONFIG__ = None
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_opts():
    """ get executions parameters
    :return: options - value mapping dictionary
    """
    _opts = {}
    opts, args = getopt.getopt(sys.argv[1:], 'e:s:l:')
    for opt, arg in opts:
        if opt == '-e':
            _opts['e'] = arg
        elif opt == '-s':
            _opts['s'] = arg
        elif opt == '-l':
            _opts['l'] = arg
    return _opts


def get_env_mode(nocache=False):
    """ get execution environment mode values and global execution environment variables
    :param nocache: cache flag
    :return: environment mode values
    """
    global __env__
    if nocache is False and __env__ is not None:
        return __env__
    try:
        _opts = get_opts()
        if 'e' in _opts:
            __env__ = _opts['e']
        return __env__
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)


def load_config_resource(mode=None):
    """ load the executions environment file
    :param mode: environment mode value
    :return: void
    """
    global __CONFIG__
    if mode is None:
        mode = get_env_mode()
    if mode is not None:
        with open(os.path.join(ROOT_DIR, 'resource/environment-' + str(mode).lower() + '.json')) as rf:
            __CONFIG__ = json.loads(rf.read())


def get_config_object():
    """ returns config object
    :return: config object
    """
    return __CONFIG__


class ConfigurationProcessException(Exception):
    pass


def get_config(name=None):
    """ returns execution environment variable
    :param name: variable key
    :return: variable value
    """
    if __CONFIG__ is None:
        raise ConfigurationProcessException('[config] invalid executions environment object.')
    if not name:
        return __CONFIG__
    if name not in __CONFIG__:
        raise ConfigurationProcessException('[config] invalid executions environment variable key. (name: {})'
                                            .format(name))
    return __CONFIG__[name]


load_config_resource()
