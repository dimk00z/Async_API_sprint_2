# Async API Sprint 2

# Техническое задание

Задание в [тасках](https://github.com/dimk00z/Async_API_sprint_2/tree/main/tasks) и на [Яндекс.Практикуме](https://practicum.yandex.ru/learn/middle-python/courses/c3542626-7807-4495-b198-555e60bfd8a6/sprints/9700/topics/d2fe568d-9bc8-471d-b458-d85e9555eafd/lessons/2f6bc576-886c-4c3c-b645-bf65a4155faf/)

## Тестирование
### Способ 1 (только инфраструктура в docker)
[docker-compose.infra.yaml](https://github.com/dimk00z/Async_API_sprint_2/blob/main/tests/functional/docker-compose.infra.yaml)
1. Запустить `elastic` + `redis` в `Docker` :
   ```shell
   docker-compose -f docker-compose.infra.yaml up -d
   ```
2. Запустить `async-api` через `python main.py` 
3. Запуск тестов через `PYTHONPATH=. pytest .`

### Способ 2 (инфраструктура + async_api в docker) 
[docker-compose.infra.yaml](https://github.com/dimk00z/Async_API_sprint_2/blob/main/tests/functional/docker-compose.infra.yaml)+[docker-compose.api.yaml](https://github.com/dimk00z/Async_API_sprint_2/blob/main/tests/functional/docker-compose.api.yamll)
1. Запустить `elastic` + `redis` + `api` в `Docker`:
   ```shell
   docker-compose \
      -f docker-compose.infra.yaml \
      -f docker-compose.api.yaml \
      up -d --build
   ```
2. Если у `async-api` изменился код, то он перезагрузится автоматически. См. `docker-compose.api.yaml`
3. Запуск тестов через `PYTHONPATH=. pytest .`

### Способ 3 (все в docker) 
[docker-compose.infra.yaml](https://github.com/dimk00z/Async_API_sprint_2/blob/main/tests/functional/docker-compose.infra.yaml)+[docker-compose.api.yaml](https://github.com/dimk00z/Async_API_sprint_2/blob/main/tests/functional/docker-compose.api.yamll)+[docker-compose.tests.yaml](https://github.com/dimk00z/Async_API_sprint_2/blob/main/tests/functional/docker-compose.tests.yamll)
1. Запустить все в docker:
   ```shell
   docker-compose -f docker-compose.infra.yaml \
      -f docker-compose.api.yaml \
      -f docker-compose.tests.yaml \
      up -d --build
   ```

## Выполнили

- [Дмитрий Кузнецов](https://github.com/dimk00z)

- [Арсений Егоров](https://github.com/marchinho11)

- [Дмитрий Мурдашев](https://github.com/di3mus)
