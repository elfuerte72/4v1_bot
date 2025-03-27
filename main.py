import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
from dotenv import load_dotenv

# Импорты для работы с LangChain и агентами
from agents.therapist_agent import TherapistAgent
from agents.observer_agent import ObserverAgent
from agents.corrector_agent import CorrectorAgent

# Загрузка переменных окружения
load_dotenv()

# Проверка наличия необходимых ключей API
required_env_vars = ["TELEGRAM_TOKEN", "OPENAI_API_KEY", "TAVILY_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Переменная окружения {var} не найдена")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

dialogue_history = []

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я AI-терапевт. Расскажи, что тебя беспокоит.")

@dp.message()
async def handle_message(message: Message):
    global current_prompt

    client_input = message.text
    current_dialog = {"user_message": client_input}
    dialogue_history.append(current_dialog)

    # Ответ психолога
    psych_response = await psych_chain.generate_response(
        user_message=client_input, 
        dialog_history=dialogue_history
    )
    current_dialog["bot_message"] = psych_response
    await message.answer(psych_response)

    # Наблюдатель
    history_text = []
    for entry in dialogue_history[-6:]:
        if "user_message" in entry:
            history_text.append(f"Клиент: {entry['user_message']}")
        if "bot_message" in entry:
            history_text.append(f"Психолог: {entry['bot_message']}")
    
    dialogue_text = "\n".join(history_text)
    observer_output = await observer_chain.run(dialogue=dialogue_text)

    # Корректор (если есть замечания)
    if "ошибка" in observer_output.lower() or "проблема" in observer_output.lower():
        new_prompt = await rewriter_chain.run(
            old_prompt=current_prompt, 
            analysis=observer_output
        )
        current_prompt = new_prompt
        await message.answer(
            "⚠️ Обнаружены проблемы в ответах. Промпт психолога обновлён."
        )

@dp.message(Command("search"))
async def handle_search_command(message: Message):
    """Обработчик команды /search для прямого запроса поиска в интернете"""
    # Проверяем, есть ли текст после команды
    command_args = message.text.split(maxsplit=1)
    if len(command_args) < 2:
        await message.answer(
            "Пожалуйста, укажите поисковый запрос после команды. "
            "Например: /search методики когнитивно-поведенческой терапии"
        )
        return
    
    search_query = command_args[1]
    await message.answer(f"🔍 Ищу информацию по запросу: '{search_query}'...")
    
    # Используем инструмент поиска напрямую
    from search_tool import get_search_tool
    search_tool = get_search_tool()
    
    try:
        # Создаем корутину для выполнения поиска
        def run_search():
            return search_tool.run(search_query)
        
        # Выполняем поиск асинхронно, чтобы не блокировать бота
        result = await asyncio.to_thread(run_search)
        await message.answer(result)
    except Exception as e:
        logger.error(f"Ошибка при выполнении поиска: {str(e)}")
        await message.answer(f"Произошла ошибка при выполнении поиска: {str(e)}")

async def main():
    # Инициализация агентов
    global psych_chain, observer_chain, rewriter_chain, current_prompt
    
    # Базовый промпт для психолога
    current_prompt = """
    Вы - профессиональный психолог-консультант. Ваша задача - помогать клиентам, 
    проявляя эмпатию и используя научно-обоснованные методы терапии.
    """
    
    # Создание агентов
    therapist = TherapistAgent(logger=logger)
    observer = ObserverAgent(logger=logger)
    corrector = CorrectorAgent(logger=logger)
    
    psych_chain = therapist
    observer_chain = observer
    rewriter_chain = corrector
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())