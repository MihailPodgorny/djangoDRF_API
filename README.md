Тестовое задание (само задание описано в TASK.MD).
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