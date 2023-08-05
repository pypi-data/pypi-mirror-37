import re

import argparse

import docker

from metasdk import read_developer_settings


def generate_tag(service: str, version: str = "v1") -> str:
    return "{}-latest".format(service, version)


def get_build_num():
    import datetime
    nd = datetime.datetime.now()
    fd = datetime.datetime.strftime(nd, "%Y%m%d%H%M%S")
    return fd


def await_build(build_result, image_tag):
    response = []
    srch = 'Successfully tagged ' + image_tag
    for line in build_result:
        line_get = line.get('stream', '')
        print("Docker build: " + line_get.replace("\n", ""))
        response.append(line_get)

        match = re.search(srch, line_get)
        if match:
            print("Build OK", {"res": response[-10:]})
            return
    raise Exception("Could not build image. {}".format(response[-10:]))


def await_push(push_result):
    response = []
    srch = r'{}: digest: sha256:[0-9a-f]+'.format(service_docker_tag)
    for line in push_result:
        response.append(line.get('stream', ''))
        match = re.search(srch, line.get('status', ''))
        if match:
            print("Push result", {"res": response[-10:]})
            return
    raise Exception("Could not push image. {}".format(response[-10:]))


if __name__ == '__main__':
    """
    Билд и деплой docker image
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', help='Name of API Service. Example: hello', type=str, required=True)
    parser.add_argument('--docker_repo', help='Name of docker repo. Example: mycompany/repo', type=str, required=True)
    parser.add_argument('--workdir', help='Root of project dir. Default "."', default=".", type=str, required=False)
    args = parser.parse_args()

    gcloud_params = read_developer_settings().get('gcloudDev')
    if not gcloud_params:
        raise ValueError("gcloudDev не установлены в developer_settings")

    grpc_service = args.service
    gcloud_prefix = gcloud_params.get('prefix', '')
    endpoint_service_name = gcloud_prefix + "-" + grpc_service if gcloud_prefix else grpc_service

    docker_cli = docker.from_env()
    docker_repo = args.docker_repo

    service_docker_tag = endpoint_service_name + "-latest"
    image_tag = "{}:{}".format(docker_repo, service_docker_tag)

    print("Build start")
    await_build(
        docker_cli.api.build(
            path=args.workdir,
            tag=image_tag,
            rm=True,
            stream=True,
            decode=True
        )
        , image_tag)

    print("Push start")
    await_push(
        docker_cli.api.push(
            repository=docker_repo,
            tag=service_docker_tag,
            stream=True,
            decode=True
        )
    )
