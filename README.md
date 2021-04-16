# Alliance Calendar

## Environment

### Container

- python: 3.9.4-slim-buster
- time zone: Asia/Tokyo

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
