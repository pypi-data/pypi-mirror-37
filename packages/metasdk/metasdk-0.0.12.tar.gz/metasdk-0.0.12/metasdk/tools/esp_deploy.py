import os

from os.path import expanduser

import argparse

from metasdk import read_developer_settings
from metasdk.tools import exec_cmd

if __name__ == '__main__':
    """
    Заливает конфигурацию в Google Cloud Endpoints
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', help='Name of API Service. Example: hello', type=str, required=True)
    parser.add_argument('--lang', help='For each language generating code. Example: python', type=str, required=True)
    parser.add_argument('--workdir', help='Root of project dir. Default "."', default=".", type=str, required=False)
    args = parser.parse_args()

    gcloud_params = read_developer_settings().get('gcloudDev')
    if not gcloud_params:
        raise ValueError("gcloudDev не установлены в developer_settings")

    user_dir = expanduser("~")
    api_workdir = args.workdir + "/api"
    proto_path = api_workdir + "/proto"
    grpc_service = args.service

    api_descriptor_path = "/tmp/" + grpc_service + "_api_descriptor.pb"

    versions = []
    for entry in os.scandir(proto_path):
        versions.append(entry.name)

    service_protos = []
    for api_version in versions:
        proto_file_path = api_workdir + "/proto/" + api_version + "/" + grpc_service + ".proto"
        service_protos.append(proto_file_path)

        if args.lang == 'python':
            gen_dir = args.workdir + "/src/"
            if not os.path.exists(gen_dir):
                os.makedirs(gen_dir)

            exec_cmd("""
                    python3 -m grpc.tools.protoc \
                        --proto_path={user_dir}/grpc-api-common-protos \
                        --proto_path={proto_path} \
                        --python_out={gen_dir} \
                        --mypy_out={gen_dir} \
                        --grpc_python_out={gen_dir} \
                        {proto_file_path}
                """.format(
                api_version=api_version,
                user_dir=user_dir,
                proto_path=proto_path,
                proto_file_path=proto_file_path,
                gen_dir=gen_dir
            ))
        else:
            raise ValueError("Not supported command argument: language ")

    exec_cmd("""
            python3 -m grpc.tools.protoc \
                --include_imports \
                --include_source_info \
                --proto_path={user_dir}/grpc-api-common-protos \
                --proto_path={proto_path} \
                --descriptor_set_out={api_descriptor_path} \
                {proto_file_paths}
        """.format(
        user_dir=user_dir,
        proto_path=proto_path,
        proto_file_paths=' '.join(service_protos),
        api_descriptor_path=api_descriptor_path
    ))

    conf_path = api_workdir + "/" + grpc_service + ".yaml"
    with open(conf_path, 'r') as f:
        gcloud_project = gcloud_params['project']
        gcloud_prefix = gcloud_params.get('prefix', '')
        endpoint_service_name = gcloud_prefix + "-" + grpc_service if gcloud_prefix else grpc_service

        config_content = f.read().format(
            SERVICE_ID=endpoint_service_name,
            PROJECT_ID=gcloud_project,

            # у гугла в кофиге как раз питоновсие выражения форматирования,
            # приходится их заменять на самих себя
            project="{project}"
        )
        endpoint_conf = "/tmp/out.yaml"
        with open(endpoint_conf, 'w') as f:
            f.write(config_content)

    exec_cmd('gcloud endpoints services deploy {api_descriptor_path} {endpoint_conf} --project {project}'.format(
        endpoint_conf=endpoint_conf,
        api_descriptor_path=api_descriptor_path,
        project=gcloud_project
    ))
