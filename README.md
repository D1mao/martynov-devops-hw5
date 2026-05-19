# DevOps HW5 — Docker Compose

## Задание

2) Напишите docker compose конфиг, для разворачивания двух контейнеров в одной сети (10.10.10.0/28) типа bridge: 
Nginx или Apache + ваше самописное web приложение на выбор (подойдет даже "заглушка" методу get), ему должны передаваться конфигурационные файлы через volume, nginx открыт на 80 порту и должен быть доступен из контейнера на хостовой машине по порту 8080
mysql или postgres, каталог для хранения данных должен монтироваться как docker volume, docker volume должен быть описан в том же конфигурационном файле docker compose. Сервис с БД должен быть доступен из контейнера с веб-сервером по именам new_db, dev_db.
Должна быть задана очередность запуска сервисов

## Структура проекта

```text
.
├── docker-compose.yml
├── README.md
└── web/
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    ├── start.sh
    ├── nginx/
    │   └── default.conf
    └── config/
        └── app.env
```

## Выполнение и результаты:
```
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker compose up -d --build
WARN[0000] Docker Compose is configured to build using Bake, but buildx isn't installed 
[+] Building 2.0s (15/15) FINISHED                                                               docker:default
 => [web internal] load build definition from Dockerfile                                                   0.0s
 => => transferring dockerfile: 419B                                                                       0.0s
 => [web internal] load metadata for docker.io/library/python:3.12-slim                                    1.7s
 => [web internal] load .dockerignore                                                                      0.0s
 => => transferring context: 2B                                                                            0.0s
 => [web 1/9] FROM docker.io/library/python:3.12-slim@sha256:401f6e1a67dad31a1bd78e9ad22d0ee0a3b52154e6bd  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:401f6e1a67dad31a1bd78e9ad22d0ee0a3b52154e6bd30e9  0.0s
 => [web internal] load build context                                                                      0.0s
 => => transferring context: 91B                                                                           0.0s
 => CACHED [web 2/9] RUN apt-get update &&     apt-get install -y nginx curl &&     rm -rf /var/lib/apt/l  0.0s
 => CACHED [web 3/9] RUN rm -f /etc/nginx/sites-enabled/default                                            0.0s
 => CACHED [web 4/9] WORKDIR /app                                                                          0.0s
 => CACHED [web 5/9] COPY requirements.txt /app/requirements.txt                                           0.0s
 => CACHED [web 6/9] RUN pip install --no-cache-dir -r /app/requirements.txt                               0.0s
 => CACHED [web 7/9] COPY app.py /app/app.py                                                               0.0s
 => CACHED [web 8/9] COPY start.sh /start.sh                                                               0.0s
 => CACHED [web 9/9] RUN chmod +x /start.sh                                                                0.0s
 => [web] exporting to image                                                                               0.1s
 => => exporting layers                                                                                    0.0s
 => => exporting manifest sha256:e320ee86713444476365288e2299f8b496556798f84ed5a9f68fccd1a0019fa4          0.0s
 => => exporting config sha256:f62787418497e5cb20624b466a91bf7c8d9ec2583423794b9a90eeee0e28efd1            0.0s
 => => exporting attestation manifest sha256:bc2a667bff68e3f949429336afe098bd8d7c403a62ecfcb75ff9dbd7263f  0.0s
 => => exporting manifest list sha256:0602955daae50c5669234d2a632b8c254c65b4da9c74e8b4ea682bb025474c21     0.0s
 => => naming to docker.io/library/martynov-devops-hw5-web:latest                                          0.0s
 => => unpacking to docker.io/library/martynov-devops-hw5-web:latest                                       0.0s
 => [web] resolving provenance for metadata file                                                           0.0s
[+] Running 4/4
 ✔ web                                      Built                                                          0.0s 
 ✔ Network martynov-devops-hw5_dev_network  Created                                                        0.1s 
 ✔ Container martynov_postgres              Healthy                                                        5.9s 
 ✔ Container martynov_web                   Started                                                        6.0s 
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ curl http://localhost:8080
{"app_name":"Martynov DevOps Web App","available_db_names":["new_db","dev_db"],"db_host":"new_db","message":"Nginx + Flask application is running"}
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ curl http://localhost:8080/api/health
{"service":"Martynov DevOps Web App","status":"ok"}
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ curl http://localhost:8080/api/db-check
{"db_host":"new_db","db_version":"PostgreSQL 16.14 (Debian 16.14-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit","message":"Database connection successful","status":"ok"}
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker network ls
NETWORK ID     NAME                              DRIVER    SCOPE
6c7b52b9a9b0   bridge                            bridge    local
8c0fee345366   host                              host      local
cd6ba9846d3c   martynov-devops-hw5_dev_network   bridge    local
c126c6c2cd86   none                              null      local
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker inspect martynov-devops-hw5_dev_network
[
    {
        "Name": "martynov-devops-hw5_dev_network",
        "Id": "cd6ba9846d3c22e9038208f82ae7f3b507f8120a0acf45ad9f255cf68e9b415c",
        "Created": "2026-05-17T22:34:40.766383725+03:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv4": true,
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.10.10.0/28",
                    "IPRange": "",
                    "Gateway": "10.10.10.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Options": {},
        "Labels": {
            "com.docker.compose.config-hash": "62f2c9e85bf3227b1009573321059d7ff33ccf2a4f13545864a5bc1f34aff956",
            "com.docker.compose.network": "dev_network",
            "com.docker.compose.project": "martynov-devops-hw5",
            "com.docker.compose.version": "2.40.3"
        },
        "Containers": {
            "34c6c6e51fe14d7638bd71741ceaeac55c2a993893e810ce37461886c4173f4d": {
                "Name": "martynov_web",
                "EndpointID": "34a518de466d40ff6fd12be1cb0b071eab71ae24efa341edbcab8487b8647130",
                "MacAddress": "f6:ea:8b:a2:33:ac",
                "IPv4Address": "10.10.10.2/28",
                "IPv6Address": ""
            },
            "cee245056224faa5b7cbb973a7eaeae25b51b0b837bb246327544ced8c253460": {
                "Name": "martynov_postgres",
                "EndpointID": "d85da8335d92ed7b67caf155f8d665e4a24b25dceb1a96f3d46e11977902934c",
                "MacAddress": "aa:87:d6:6b:9e:a7",
                "IPv4Address": "10.10.10.3/28",
                "IPv6Address": ""
            }
        },
        "Status": {
            "IPAM": {
                "Subnets": {
                    "10.10.10.0/28": {
                        "IPsInUse": 5,
                        "DynamicIPsAvailable": 11
                    }
                }
            }
        }
    }
]
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker exec martynov_web getent hosts new_db
10.10.10.3      new_db
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker exec martynov_web getent hosts dev_db
10.10.10.3      dev_db
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker volume ls
DRIVER    VOLUME NAME
local     5d100e0ef2d6c66b7fb08b9ef4f63c998a1c7b9d02c521e685062a8a78de2a19
local     9c3f312b95b8a92461fa38e713b7f979d110512bc0e8306d190802f802fe2013
local     75ce18de7fd47a1a3f0b6e7f99ed04e9e149923df9e8e302065baa609a9cdeb6
local     761d63fabc509c7cc4f65e1d782171868db5378c8b191adbefa35b9b3994aba6
local     d10758c63050927d1a7a168842dd31bcfa1b522523823daf5988ce956896c85e
local     martynov-devops-hw5_postgres_data
d1mao@d1mao-VirtualBox:~/devops/martynov-devops-hw5$ sudo docker volume inspect martynov-devops-hw5_postgres_data
[
    {
        "CreatedAt": "2026-05-17T22:16:48+03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "ba80d8f269eaf4daecd3a856097480ccd21b06d4e50523b8261d6f28aae3e49d",
            "com.docker.compose.project": "martynov-devops-hw5",
            "com.docker.compose.version": "2.40.3",
            "com.docker.compose.volume": "postgres_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/martynov-devops-hw5_postgres_data/_data",
        "Name": "martynov-devops-hw5_postgres_data",
        "Options": null,
        "Scope": "local"
    }
]
```
