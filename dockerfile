FROM python:3.8

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install sqlite3
COPY config ./
COPY .env ./
COPY requirements.txt ./
RUN pip install -U pip -r requirements.txt
RUN cd config
RUN mkdir config/static
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations && python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]