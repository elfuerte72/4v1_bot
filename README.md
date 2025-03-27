# AI Therapy Bot

Многоагентный терапевтический бот для Telegram с возможностью онлайн-поиска информации.

## Возможности

- 🤖 Агент-психолог ведет консультации
- 👀 Наблюдатель анализирует ответы и отслеживает ошибки
- ✍️ Корректор обновляет промпт психолога при необходимости
- 🔍 Поиск информации в интернете через Tavily API
- 💾 Сохранение диалогов в SQLite
- 📊 Веб-интерфейс через Streamlit
- 📝 Поддержка LangSmith для анализа

## Команды бота

- `/start` - Начать диалог с психологом
- `/debug` - Включить режим наблюдения
- `/nodebug` - Выключить режим наблюдения
- `/search [запрос]` - Поиск информации в интернете

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/ai_therapy_bot.git
   cd ai_therapy_bot
   ```

2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # для Linux/macOS
   # или
   venv\Scripts\activate  # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` и добавьте необходимые API-ключи:
   ```
   TELEGRAM_TOKEN=your_telegram_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

   Где взять ключи:
   - TELEGRAM_TOKEN: Создайте бота у [@BotFather](https://t.me/BotFather)
   - OPENAI_API_KEY: [OpenAI API](https://platform.openai.com/api-keys)
   - TAVILY_API_KEY: [Tavily API](https://tavily.com/)

## Запуск

1. Запустите Telegram-бота:
   ```bash
   python main.py
   ```

2. Запустите веб-интерфейс (опционально):
   ```bash
   streamlit run webapp.py
   ```

## Структура проекта

```
ai_therapy_bot/
├── agents/
│   ├── __init__.py
│   ├── therapist_agent.py
│   ├── observer_agent.py
│   └── corrector_agent.py
├── search_tool.py
├── main.py
├── webapp.py
├── requirements.txt
└── README.md
```

## Технологии

- Python 3.9+
- OpenAI GPT-4
- LangChain
- Tavily Search API
- SQLite
- Streamlit
- aiogram

## Лицензия

MIT 