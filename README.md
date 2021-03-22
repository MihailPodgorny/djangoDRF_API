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
4. Выполнить миграции и запустить сервер:
```
cd .\config
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