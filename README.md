Тестовое задание (само задание описано в TASK.MD).
-------------------------------------------------
Установка через docker.
-------------------------------------------------
1. Скопировать дистрибутив
```
git clone https://github.com/MihailPodgorny/djangoDRF_API.git
```
2. Перейти в директории с dockerfile и собрать образ контейнера:
```
cd djangoDRF_API
docker build -t django_api ./
```
3. Запустить контейнер
```
docker run --name new_django_api -p 8000:8000 -d django_api
```
4. Чтобы войти в shell работающего контейнера:
```
docker exec -ti new_django_api bash
```
- для создания административной учетной записи в shell контейнера:
```
python3 manage.py createsuperuser
```
- для запуска тестов:
```
python manage.py test
```
5. При необходимости просмотра документации:
```
http://127.0.0.1:8000/swagger/#
```
6. Чтобы выключить и удалить контейнер:
```
docker stop new_django_api
docker rm new_django_api
```
7. Чтобы удалить образ:
```
docker rmi django_api
```

Установка в виртуальном окружении.
-------------------------------------------------
1. Необходимо настроить виртуальное окружение Python3.8
2. Скопировать дистрибутив
 ```
git clone https://github.com/MihailPodgorny/djangoDRF_API.git
```  
3. Установить все необходимые пакеты:
```
pip install -r requirements.txt
```
4. Собрать статику, выполнить миграции и запустить сервер:
```
cd ./config && mkdir ./config/static
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
5. Для создания административной учетной записи:
```
python manage.py createsuperuser
```
6. При необходимости запуска тестов:
```
python manage.py test
```
7. При необходимости просмотра документации:
```
http://127.0.0.1:8000/swagger/#
```
