# Async API Sprint 2

## Тестирование
### Способ 1 (только инфра в docker)
1. Запустить `elastic` + `redis` в `Docker`:
   ```shell
   docker-compose -f docker-compose.infra.yaml up -d
   ```
2. Запустить `async-api` через `python`
3. Запуск тестов через `PYTHONPATH=. pytest .`

### Способ 2 (инфра + async_api в docker)
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
1. Запустить все в docker:
   ```shell
   docker-compose -f docker-compose.infra.yaml \
      -f docker-compose.api.yaml \
      -f docker-compose.tests.yaml \
      up -d --build
   ```
