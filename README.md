# Social-network-for-travelers


<div>
  <p>Социальная сеть для путешественников.</p>
  
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


Запустите проект на хостинге:

```javascript
docker compose -f docker-compose.prod.yml up  --build
```
