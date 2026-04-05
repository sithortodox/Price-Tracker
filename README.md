# Price Tracker

Универсальный каркас сервиса для отслеживания цен и наличия товаров.

## Что умеет
- отслеживать цену товара по URL;
- фиксировать наличие / отсутствие на складе;
- хранить историю изменений в PostgreSQL;
- отправлять уведомления в Telegram;
- строить график изменения цены;
- настраиваться через `.env`;
- запускаться через Docker Compose.

## Стек
- Python 3.12
- SQLAlchemy
- PostgreSQL
- Playwright / BeautifulSoup
- Matplotlib
- Telegram Bot API
- Docker Compose

## Архитектура
- `app/config.py` — настройки
- `app/db.py` — подключение к БД
- `app/models.py` — ORM-модели
- `app/trackers/base.py` — базовый интерфейс трекеров
- `app/notifier.py` — Telegram-уведомления
- `app/plotting.py` — построение графиков
- `app/scheduler.py` — запуск цикла проверки
- `app/main.py` — точка входа

## Статус
Сейчас это MVP-каркас под дальнейшее развитие источников и бизнес-логики.
