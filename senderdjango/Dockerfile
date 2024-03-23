FROM python:3.11-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /usr/src/app

# Копируем файл зависимостей и устанавливаем их
COPY req.txt ./

RUN pip install --upgrade pip
RUN pip install -r req.txt

# Копируем исходный код проекта
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Устанавливаем Nginx
RUN apk update && apk add nginx

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/nginx.conf



# Открываем порт 80
EXPOSE 80

#nginx &&

# Запускаем Nginx и Gunicorn
CMD ["sh", "-c", "nginx -g 'daemon off;' & exec gunicorn senderdjango.wsgi:application --bind 0.0.0.0:8000"]



