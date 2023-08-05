import argparse
from os.path import expanduser

from metasdk import read_developer_settings
from metasdk.tools import exec_cmd, TOOLS_DIR

if __name__ == '__main__':
    """
    Деплой API сервиса в кубернейтс
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--service', help='Name of API Service. Example: hello', type=str, required=True)
    parser.add_argument('--docker_repo', help='Name of docker repo. Example: mycompany/repo', type=str, required=True)
    parser.add_argument('--image_tag', help='Name of docker image_tag. Example: mycompany/repo:lala-latest', type=str, required=False)
    args = parser.parse_args()

    user_dir = expanduser("~")

    gcloud_params = read_developer_settings().get('gcloudDev')
    if not gcloud_params:
        raise ValueError("gcloudDev не установлены в developer_settings")

    grpc_service = args.service
    gcloud_project = gcloud_params['project']
    gcloud_prefix = gcloud_params.get('prefix', '')
    endpoint_service_name = gcloud_prefix + "-" + grpc_service if gcloud_prefix else grpc_service

    if args.image_tag:
        full_image_tag = args.docker_repo + ":" + args.image_tag
    else:
        full_image_tag = args.docker_repo + ":" + endpoint_service_name + "-latest"

    deployment_tpl = TOOLS_DIR + "/apis_deployment.yaml"
    with(open(deployment_tpl, 'r')) as f:
        new_content = f.read().format(
            SERVICE_ID=endpoint_service_name,
            PROJECT_ID=gcloud_project,
            IMAGE_TAG=full_image_tag
        )

    deployment_yaml = "/tmp/" + grpc_service + "_deployment.yaml"
    with(open(deployment_yaml, 'w')) as f:
        f.write(new_content)

    exec_cmd("kubectl delete deployment grpc-{service}".format(service=endpoint_service_name), check=False)
    exec_cmd("kubectl apply -f {deployment_yaml}".format(deployment_yaml=deployment_yaml))
