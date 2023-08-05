# Meta  SDK


Документация: http://metasdk.readthedocs.io

Полный список примеров: https://github.com/devision-io/metasdk/tree/master/metasdk/examples

## Структура каталогов
- doc - Автоматически собираемая документация
- metasdk
  - services - API службы, доступные к управелению через SDK
  - logger - общий и массовый логгер, вызывать стоит **только** через **META.log**  
  - examples - примеры работы с сервисами и прочей функциональостью SDK 
  - tools - скрипты для **только** консольных вызовов через python -m. Например тут вспомогальеные скрипты деплоя и разработки API сервисов

## Tools

### Сбока и деплой контейнера

```bash
# Подготовка машины разработчика
python3 -m metasdk.tools.esp_deploy_init

# Загрузка дескриптора api в google cloud endpoints
python3 -m metasdk.tools.esp_deploy --service=hello --lang=python --workdir=$(CWD)

# Билд docker image и загрузка на docker hub
python3 -m metasdk.tools.build_docker_image --docker_repo=apisgarpun/apis --workdir=$(CWD)

# Деплой в кубер
python3 -m metasdk.tools.kuber_deploy --service=hello --docker_repo=apisgarpun/apis
```