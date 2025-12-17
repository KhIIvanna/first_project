Веб‑додаток для управління замовленнями транспорту, клієнтами, водіями, маршрутами та авто. Розроблено на **Flask + PostgreSQL**.

Покроковий запуск: 

1.  Репозиторій на GitHub

Завантажити проєкт на GitHub. Структура має містити app.py, шаблони (templates/), стилі (static/), файл requirements.txt та Procfile.

2.	Хостинг на Render

o	Створити акаунт на https://render.com
o	Обрати тип сервісу: Web Service
o	Підключити репозиторій GitHub
o	Указати:
        Start command: gunicorn app:app
        Environment: Python 3.11+
        Build command: pip install -r requirements.txt
        Environment variables:
                        DATABASE_URL — посилання на хмарну базу Neon PostgreSQL
                        SECRET_KEY — довільний ключ для Flask

3.	База даних на Neon

o	Створити акаунт на https://neon.tech
o	Створити нову базу даних
o	Скопіювати DATABASE_URL та вставити у Render
o	Імпортувати структуру таблиць через SQL дамп або вручну

4.	Автоматичний деплой після кожного git push у репозиторій Render автоматично оновлює додаток. Статус можна переглядати у вкладці Logs у Neon.
