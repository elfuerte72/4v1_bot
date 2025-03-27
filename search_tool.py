import os
from dotenv import load_dotenv
from langchain.tools import Tool
from tavily import TavilyClient

load_dotenv()

class TavilySearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY не найден в переменных окружения")
        self.client = TavilyClient(api_key=api_key)
    
    def search(self, query: str) -> str:
        """
        Поиск информации в интернете с помощью Tavily Search API.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            str: Результаты поиска в виде текста
        """
        try:
            search_result = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )
            
            if not search_result.get('results'):
                return "Не удалось найти информацию по этому запросу."
            
            results_text = "### Результаты поиска:\n\n"
            for i, result in enumerate(search_result.get('results', []), 1):
                results_text += f"{i}. **{result.get('title', 'Без заголовка')}**\n"
                results_text += f"   {result.get('content', 'Нет содержания')}\n"
                results_text += f"   Источник: {result.get('url', 'Нет источника')}\n\n"
            
            return results_text
        except Exception as e:
            return f"Ошибка при выполнении поиска: {str(e)}"
    
    def run(self, query: str) -> str:
        """
        Метод для совместимости с интерфейсом Tool.
        """
        return self.search(query)


def get_search_tool() -> Tool:
    """
    Создает инструмент LangChain для поиска информации в интернете.
    
    Returns:
        Tool: Инструмент LangChain для поиска
    """
    search_tool = TavilySearchTool()
    
    return Tool(
        name="internet_search",
        description=(
            "Полезен для поиска актуальной информации в интернете. "
            "Используйте этот инструмент, когда клиент просит факты, "
            "ссылается на исследования, спрашивает о методиках или "
            "когда вам нужно проверить информацию."
        ),
        func=search_tool.search,
    ) 