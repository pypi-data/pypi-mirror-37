import os as _os


def _set_credentials():
    try:
        home = _os.path.expanduser("~")
        with open(home + '/.pypi_umihico_env', 'r') as f:
            for line in f.readlines():
                key, password = line.split(':')
                key = 'umihico_' + key
                _os.environ[key] = password
    except Exception as e:
        raise


_set_credentials()

import api

if __name__ == '__main__':
    print(_os.environ['umihico_line_api_key'])
