# Проект Test Chat

Проект онлайн-чата с авторизацией.

Исползовано:
- Python 3.9
- Django 4.1.3
- Django REST framework 3.14.0
- Channels 4.0.0

## Инструкция по установке

После клонирование репозиторий из github-а вам потребуется [Docker](https://docker.com/) для запуска.

После установки Docker:
1. Переходите на директорию с файлом `docker-compose.yml` внутри репозиторий и запустите следующую команду в камандной страке.
    ```bash
    docker compose up
    ```
После этого у вас должно запустится проект на [localhost:8000](https://localhost:8000)