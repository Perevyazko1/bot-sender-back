FROM python:3.11-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /usr/src/app

# Копируем файл зависимостей и устанавливаем их
COPY req.txt ./

RUN pip install --upgrade pip
RUN pip install -r req.txt

# Копируем исходный код проекта
COPY . .


# Открываем порт 80
EXPOSE 80

# Запускаем Nginx и Gunicorn
CMD ["sh", "-c", "exec gunicorn senderdjango.wsgi:application --bind 0.0.0.0:8000"]
