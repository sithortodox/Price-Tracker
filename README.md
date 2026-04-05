# Price Tracker

Универсальный Python-проект для отслеживания цены и наличия товаров.

Это не привязка к одному магазину, а расширяемый MVP-каркас, который можно адаптировать под публичные страницы магазинов, маркетплейсов и промо-лендингов.

## Что умеет
- отслеживать цену товара по URL;
- фиксировать наличие / отсутствие на складе;
- хранить историю изменений в PostgreSQL;
- отправлять уведомления в Telegram;
- строить график изменения цены;
- настраиваться через `.env`;
- запускаться через Docker Compose;
- использовать конфигурируемые CSS-селекторы для разных страниц.

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
- `app/models.py` — ORM-модели товаров и истории цен
- `app/trackers/base.py` — базовый интерфейс трекеров
- `app/trackers/generic_html.py` — универсальный HTML-трекер по CSS-селекторам
- `app/service.py` — логика цикла проверки и сохранения истории
- `app/notifier.py` — Telegram-уведомления
- `app/plotting.py` — построение графиков
- `app/scheduler.py` — циклический запуск проверки
- `app/main.py` — точка входа
- `scripts/seed_demo_data.py` — создание демо-товара
- `scripts/generate_demo_history.py` — генерация демо-истории и графика
- `scripts/show_history.py` — вывод истории в консоль
- `scripts/run_demo.sh` — быстрый demo flow

## Модель данных
### TrackedProduct
- источник
- название
- URL
- валюта
- целевая цена
- флаг активности
- `selectors` — JSON с CSS-селекторами под конкретную страницу

### PriceHistory
- цена
- наличие
- сырое название
- сырые данные
- время проверки

## Пример selectors
```json
{
  "title": "h1",
  "price": ".price",
  "stock": ".availability",
  "out_of_stock_text": "нет в наличии"
}
```

## Быстрый старт локально
### 1. Подготовить окружение
```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Запустить PostgreSQL
```bash
docker compose up -d postgres
```

### 3. Запустить приложение
```bash
python3 -m app.main
```

## Demo flow
### Подготовить демо-данные
```bash
python3 scripts/seed_demo_data.py
```

### Сгенерировать демо-историю и график
```bash
python3 scripts/generate_demo_history.py
```

### Посмотреть историю в консоли
```bash
python3 scripts/show_history.py
```

### Быстрый сценарий demo
```bash
bash scripts/run_demo.sh
```

После этого график будет сохранён в:
```text
artifacts/demo_price_history.png
```

## Запуск через Docker Compose
```bash
cp .env.example .env
docker compose up --build
```

## Что хорошо показать в GitHub
- `artifacts/demo_price_history.png` как пример графика;
- кусок консольной истории из `show_history.py`;
- пример `.env.example`;
- пример JSON-селекторов;
- GIF/скрин Telegram-уведомления при изменении цены.

## Roadmap
- добавить CLI для управления товарами;
- добавить реальные source adapters под конкретные магазины;
- добавить email-уведомления;
- добавить Alembic-миграции;
- добавить web dashboard / admin UI.

## Статус
Сейчас это MVP-каркас, который уже показывает архитектуру, работу с БД, хранение price history, построение графиков и основу под расширяемые трекеры.
