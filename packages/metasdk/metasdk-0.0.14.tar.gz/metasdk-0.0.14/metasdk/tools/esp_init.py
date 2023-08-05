from os.path import expanduser

import os

from metasdk.tools import exec_cmd, TOOLS_DIR

if __name__ == '__main__':
    """
    Подготавливает машину разработчика к дальнейшей работе.
    Запустить один раз
    """

    exec_cmd('docker run -ti --name gcloud-config google/cloud-sdk:220.0.0-slim gcloud auth login')
