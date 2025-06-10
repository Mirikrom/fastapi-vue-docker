FROM python:3.11-slim

WORKDIR /app

# requirements.txt faylini konteynerga nusxalash
COPY requirements.txt .

# kerakli kutubxonalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# App papkasini konteynerga nusxalash
COPY ./app ./app

# Main faylni konteynerga nusxalash
COPY main.py ./main.py

# 8000 portni ochish
EXPOSE 8000

# Asosiy ilovani ishga tushurish
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
