import os
import sys
import importlib.util
import subprocess

def check_module(module_name):
    """Проверяет, установлен ли модуль"""
    if importlib.util.find_spec(module_name) is not None:
        print(f"✅ Модуль {module_name} установлен")
        return True
    else:
        print(f"❌ Модуль {module_name} не установлен")
        return False

def check_env_vars():
    """Проверяет наличие необходимых переменных окружения"""
    required_vars = ["TELEGRAM_TOKEN", "OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_vars = []
    
    from dotenv import load_dotenv
    load_dotenv()
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Отсутствуют следующие переменные окружения: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Все необходимые переменные окружения найдены")
        return True

def install_requirements():
    """Устанавливает необходимые зависимости из requirements.txt"""
    print("Установка необходимых зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Все зависимости успешно установлены")
        return True
    except subprocess.CalledProcessError:
        print("❌ Ошибка при установке зависимостей")
        return False

def check_database():
    """Проверяет наличие базы данных и создает её при необходимости"""
    try:
        import sqlite3
        conn = sqlite3.connect("dialogs.db")
        cursor = conn.cursor()
        
        # Проверяем, существует ли таблица диалогов
        cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='dialogs'
        """)
        
        if not cursor.fetchone():
            print("📊 Создание таблицы для диалогов...")
            cursor.execute("""
            CREATE TABLE dialogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                timestamp TEXT,
                user_message TEXT,
                bot_message TEXT
            )
            """)
            conn.commit()
            print("✅ Таблица dialogs создана успешно")
        else:
            print("✅ База данных и таблица dialogs уже существуют")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка при проверке/создании базы данных: {str(e)}")
        return False

def check_api_access():
    """Проверяет доступ к API сервисов"""
    # Проверка OpenAI API
    try:
        import openai
        from openai import OpenAI
        
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=5
        )
        print("✅ Подключение к OpenAI API работает")
    except Exception as e:
        print(f"❌ Ошибка при подключении к OpenAI API: {str(e)}")
    
    # Проверка Tavily API
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        search_result = client.search(query="test query", search_depth="basic", max_results=1)
        print("✅ Подключение к Tavily API работает")
    except Exception as e:
        print(f"❌ Ошибка при подключении к Tavily API: {str(e)}")

def main():
    print("🔍 Проверка настройки проекта AI Therapy MCP")
    print("=" * 50)
    
    # Проверка Python-версии
    print(f"📌 Используется Python {sys.version}")
    
    # Установка зависимостей
    install_requirements()
    
    # Проверка наличия основных модулей
    required_modules = [
        "aiogram", "langchain", "openai", "dotenv", "tavily", 
        "streamlit", "sqlite3", "pydantic", "langsmith"
    ]
    
    all_modules_installed = all(check_module(module) for module in required_modules)
    
    # Проверка переменных окружения
    env_vars_ok = check_env_vars()
    
    # Проверка базы данных
    db_ok = check_database()
    
    # Проверка доступа к API
    check_api_access()
    
    print("=" * 50)
    if all_modules_installed and env_vars_ok and db_ok:
        print("✅ Проект настроен корректно и готов к запуску!")
        print("🚀 Запустите бота командой: python main.py")
        print("🌐 Запустите веб-интерфейс командой: streamlit run webapp.py")
    else:
        print("❌ Проект настроен некорректно. Исправьте указанные ошибки и запустите проверку снова.")

if __name__ == "__main__":
    main() 