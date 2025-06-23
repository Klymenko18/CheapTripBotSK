# базовий образ
FROM python:3.11-slim

# робоча директорія
WORKDIR /app

# встановлюємо змінну PYTHONPATH щоб працювали імпорти з app.*
ENV PYTHONPATH=/app

# копіюємо файли
COPY . .

# оновлюємо pip
RUN pip install --upgrade pip

# встановлюємо залежності
RUN pip install -r requirements.txt

# команда запуску (зараз для бота)
CMD ["python", "main.py"]
