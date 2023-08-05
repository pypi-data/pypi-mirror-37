from os.path import expanduser

import os

from metasdk.tools import exec_cmd, TOOLS_DIR

if __name__ == '__main__':
    """
    Подготавливает машину разработчика к дальнейшей работе.
    Запустить один раз
    """
    # Установка зависимостей для работы с gcloud endpoints
    exec_cmd('python3 -m pip install -r ' + TOOLS_DIR + '/apis_requirements.txt')
    googleapis_dir = expanduser("~") + '/grpc-api-common-protos'
    if not os.path.isdir(googleapis_dir):
        exec_cmd('git clone https://github.com/devision-io/api-common-protos ' + googleapis_dir)
