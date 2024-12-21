# Задание 3

Запуск решения:

```docker compose up```

Пример конфигурации находится в .env


1) Превышение лимитов volume

В директории storage_limit_proof находятся логи и конфигурация для случая, когда переполняется хранилище, ограниченное в docker-compose.yml.

Запуск теста:
```docker compose --env-file ./storage_limit_proof/.env up```

(или ./storage_limit_test.sh, работает примерно 2 минуты)


1) Превышение квоты

В директории quota_limit_proof находятся логи и конфигурация для случая, когда переполняется квота, которая устанавливается в MinIO.

Запуск теста:
```docker compose --env-file ./quota_limit_proof/.env up```

(или ./storage_limit_test.sh, работает примерно 4 минуты)
