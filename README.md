# Social-network-for-travelers


<div>
  <p>Социальная сеть для путешественников.</p>

  ## Внешние зависимости

Проект использует следующие внешние зависимости:

- **Python 3.10**: Основной язык программирования проекта.
- **Django 5.1.2**: Фреймворк для веб-разработки.
- **Django REST Framework 3.15.2**: Библиотека для создания RESTful API.
- **Django REST Framework Simple JWT 5.3.1**: Библиотека для работы с JWT.
- **Django CORS Headers 4.5.0**: Для настройки CORS.
- **Celery 5.4.0**: Для обработки фоновых задач.
- **Redis 5.1.1**: Используется как брокер сообщений для Celery.
- **PostgreSQL**: Реляционная база данных (настраивается через Docker).
- **Pillow 11.0.0**: Библиотека для работы с изображениями.
- **Pydantic 2.9.2** и **Pydantic Settings 2.6.0**: Для валидации данных и работы с настройками.
- **Gunicorn 23.0.0**: WSGI HTTP сервер для запуска Django приложений.
- **Другие зависимости**: pre-commit, isort, black, flake8, drf-yasg, psycopg2-binary, django-filter, django-jazzmin, requests, coverage.
  
</div>

<div>
  <h1>
    STEP 1
  </h1>
</div>



## Шаг 1: Установка Docker

Если у вас уже установлен Docker, перейдите к следующему шагу . Для подробной информации об установке Docker на Ubuntu, пожалуйста, посетите [документацию Docker](https://docs.docker.com/engine/install/ubuntu/).


Set up Docker's apt repository.
```javascript
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```


Install the Docker packages.


```javascript
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```


Verify that the Docker Engine installation is successful by running the hello-world image.

```javascript
sudo docker run hello-world
```



<div>
  <h1>
    STEP 2
  </h1>
</div>

Для клонирования приложения выполните 

```javascript
 git clone https://github.com/Toxa1899/Social-network-for-travelers.git
```

далее выполните команду 


```javascript
  cd Social-network-for-travelers
```


<div>
  <h1>
    STEP 3
  </h1>
</div

<div>
 <p> для развертывания проекта локально </p>
</div>

Скопируйте файл конфигурации:

```javascript
mv .env.example .env
```

далее 

Откройте файл .env:

```javascript
nano .env
```

Измените параметр DEBUG на True:

![image (1)](https://github.com/user-attachments/assets/3dd46a9c-e6b2-48ab-b1a3-091bae784616)


Запустите проект:
```javascript
docker compose up -d --build
```


<div>
  <h1>
    STEP 4
  </h1>
</div>

<div>
 <p> для развертывания проекта на хостинге выполните </p>
</div>

Скопируйте файл конфигурации:

```javascript
mv .env.example .env
```

Откройте файл .env:
```javascript
nano .env
```
Добавьте IP-адрес вашего хостинга в ALLOWED_HOSTS:

![image](https://github.com/user-attachments/assets/28c3ef5e-cb3a-438d-aea2-7f30dbf2562c)



Запустите проект на хостинге:

```javascript
docker compose -f docker-compose.prod.yml up  --build
```

<div>
  <h1>
    STEP 4
  </h1>
</div>


при успешном  локальном развертывании проекта  , данные url будут доступны
при развертывании на хотсинги замените 127.0.0.1:8000 на ip_адресс_вашего_хостинга


<a href="http://127.0.0.1:8000/redoc/">http://127.0.0.1:8000/redoc/</a>


![Screenshot from 2024-10-26 16-53-57](https://github.com/user-attachments/assets/e40452b1-4d93-4ab1-8ddd-7f52f0be34ae)


<a href="http://127.0.0.1:8000/swagger/">http://127.0.0.1:8000/swagger/</a>

![Screenshot from 2024-10-26 16-54-40](https://github.com/user-attachments/assets/6f968c84-7f7e-4c95-b563-990ca8a88470)


<div>
  <h1>
    Info
  </h1>
</div>



При запуске контейнера автоматически выполняется скрипт initialize_db.py. Этот скрипт отвечает за инициализацию базы данных, включая запуск парсера стран и заполнение базы данных днями недели.

в .env лежит ACCESS_KEY 
пожалуйста замените его на свой данный ключ можно получить на <a href="https://countrylayer.com/">https://countrylayer.com/</a>
