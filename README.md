# Alliance Calendar

## Environment

### Container

- python: 3.9.4-slim-buster
- time zone: Asia/Tokyo

### Remote Interpreter

- [Download PyCharm Professional](https://www.jetbrains.com/ja-jp/pycharm/download/)
- [Install Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Configure the interpreter with Docker Compose](https://pleiades.io/help/pycharm/using-docker-compose-as-a-remote-interpreter.html)

## Setup

```shell
# outside container
docker-compose up -d
docker-compose logs app
docker-compose ps
docker-compose exec app bash

# inside container
python main.py
exit
```

## Cleanup

```shell
# outside container 
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
```

## Run app

```shell
docker-compose run app
```
