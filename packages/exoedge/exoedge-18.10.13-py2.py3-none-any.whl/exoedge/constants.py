# pylint: disable=C0325, C0103, C0111

""" Constants """
import json
import pureyaml
import copy
import os


OPTION_PRECEDENCE = ['cli', 'env', 'ini', 'dft']

OPTION_TYPE_MAP = {
    'debug': str,
    'strategy': str,
    'no_config_cache': bool,
    'no_config_sync': bool,
    'murano_host': str,
    'murano_id': str,
    'no_filesystem': bool,
    'config_io_file': str,
    'ini_file': str,
    'murano_token': str,
    'watchlist': list,
    'http_timeout': int,
    'certfile': str,
    'pkeyfile': str,
    'murano_cacert': str,
    'murano_port': int,
    'no-logrotate': bool,
    'log-filename': str,
    'log-max-bytes': int,
    'log-max-backups': int,
}

OPTION_NAME_MAPPER = {
    'env': lambda d, x: d.get('EDGED_{}'.format(x.upper()), None),
    'cli': lambda d, x: d.get('--{}'.format(x.replace('_', '-')), None),
    'dft': lambda d, x: d.get(x, None),
    'ini': lambda d, x: d.get(x)
}

def _ini_get(I, string):
    try:
        s, o = string.split('.')
        if s in I.sections():
            return I.get(s, o)
        else:
            return None
    except:
        return None


DEFAULTS = {
    'debug': os.environ.get('EDGED_LOG_DEBUG', 'CRITICAL').upper(),
    'strategy': 'local',
    'no_config_cache': False,
    'no_config_sync': False,
    'no_filesystem': False,
    'watchlist': ['config_io'],
    # 'watchlist': ['config_io', 'data_out', 'config_application'],
    'http_timeout': 60*5*1000,
    'ini_file': 'default.ini',
    'no-logrotate': False,
    'log-filename': os.environ.get('EDGED_LOG_FILENAME') or 'stdout',
    'log-max-bytes': int(os.environ.get('EDGED_LOG_MAX_BYTES', 1024*1000)),
    'log-max-backups': int(os.environ.get('EDGED_LOG_MAX_BACKUPS', 3)),
}
