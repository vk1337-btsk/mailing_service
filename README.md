<h3 align="center">Сервис email рассылки сообщений на Django</h3>

<details>
  <summary>Оглавление</summary>
  <ol>
    <li>О проекте</li>
    <li>Технологии</li>
    <li>Настройка проекта</li>
    <li>Использование</li>
    <li>Контакты</li>
  </ol>
</details>



## О проекте

Сервис email рассылок. После регистрации вы сможете добавить клиентов, сообщение и создать рассылку,
выбрав дату начала и окончания рассылки и с какой периодичностью производить рассылку.
При наступлении даты отправки происходит автоматическая отправка сообщения вашим клиентам.

## Технологии
- Django
- PostgreSQL
- Redis
- Crontab


## Настройка проекта

Для работы с проектом произведите базовые настройки.

### 1. Клонирование проекта

Клонируйте репозиторий используя следующую команду.
  ```sh
  git clone https://github.com/vk1337-btsk/mailing_service
  ```


### 2. Настройка виртуального окружения и установка зависимостей

- Инструкция для работы через виртуальное окружение - poetry: 
```text
poetry init - Создает виртуальное окружение
poetry shell - Активирует виртуальное окружение
poetry install - Устанавливает зависимости
```

- Инструкция для работы через виртуальное окружение - pip:

Создает виртуальное окружение:
```text
python3 -m venv venv
```

Активирует виртуальное окружение:
```text
source venv/bin/activate          # для Linux и Mac
venv\Scripts\activate.bat         # для Windows
```

Устанавливает зависимости:
```text
pip install -r requirements.txt
```

### 3. Редактирование config.ini.sample:

- В корне проекта переименуйте файл config.ini.sample в config.ini и отредактируйте параметры:
    ```text
    [database]
    engine=postgresql_psycopg2 - используем psycopg
    dbname=db_name - название вашей БД
    user=postgres - имя пользователя БД
    password=Qwerty123! - пароль пользователя БД
    host=host - можно указать "localhost" или "127.0.0.1"
    port=port - указываете порт для подключения по умолчанию 5432

  
    [data_admin]
    ADMIN_EMAIL=admin@test.com - email регистрации администратора сайта
    ADMIN_PASSWORD=Qwerty123! - пароль регистрации администратора сайта
    ADMIN_USER_NAME=admin - никнейм администратора сайта
    ADMIN_FIRST_NAME=Алексей - имя администратора сайта
    ADMIN_LAST_NAME=Алебардов - фамилия администратора сайта
    ADMIN_MIDDLE_NAME=Александрович - отчество администратора сайта
  
    [data_email_yandex]
    email_host_user = admin@test.com - email регистрации администратора сайта
    email_host_password = Qwerty123!  - пароль регистрации администратора сайта
  
    [settings_django]
    SECRET_KEY = secret - секретный ключ django проекта
    DEBUG=True - режим DEBUG
    CACHE_ENABLED=True - использование кэша
    LOCATION=redis://host:port - данные местоположения redis
    ```
- О настройке почты smtp: 
[Настройка почтового сервиса SMTP ](https://proghunter.ru/articles/setting-up-the-smtp-mail-service-for-yandex-in-django)

### 4. Настройка БД и кэширования:

- Создать миграции:
  ```text
  python manage.py makemigrations
  ```

- Примените миграции:
  ```text
  python manage.py migrate
  ```

- Если вы хотите чистый сайт без данных и пользователей тогда применять фикстуру ниже не надо, 
для создания суперюзера введите команду: 
  ```text
  python manage.py create_su
  ```
 
- Если вы хотите использовать данные из фикстур этого проекта создавать суперюзера не надо введите команду:
  ```text
  python manage.py fill_db --table all
  ```

- Установите Redis:

  - Linux команда:
   ```text
   sudo apt install redis; 
  или 
  sudo yum install redis;
   ```

  - macOS команда:
   ```text
   brew install redis;
   ```

  Windows инструкция:
  - [Перейти на Redis docs](https://redis.io/docs/install/install-redis/install-redis-on-windows/)


## Использование

- Для запуска проекта наберите в терминале команду:
  ```text
  python manage.py runserver
  ```
  перейдите по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)


- Для запуска автоматической отправки рассылок (происходит проверка раз в минуту), необходимо использовать команду запустив рядом с проектом в новом окне:
  ```text
  python manage.py runapscheduler
  ```

- Для ручного запуска рассылок можно использовать команду:
  ```text
  python manage.py start_mailing
  ```

## Контакты

Ссылка на репозиторий: [https://github.com/vk1337-btsk](https://github.com/vk1337-btsk)